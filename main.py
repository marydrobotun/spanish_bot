import asyncio
import logging
import sys
from os import getenv

import emoji
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from base import Language, UserStats, UserInfo
from buttons import ButtonsVerbose
from levelsverbose import LevelsVerbose
from message import MessageGetter
from training_generator import TrainingGenerator
from training_mode import TrainingModeVerbose
from middleware import UserLanguageMiddleware
from redis.asyncio import Redis
from db.engine import SessionFactory
from repositories.users import UserRepository

TOKEN = getenv("TOKEN")
DEFAULT_LANGUAGE = Language.RU

user_info = {}
current_trainings = {}
user_stats = {}
user_repo = UserRepository(SessionFactory)
redis = Redis.from_url(
    "redis://localhost:6379",
    decode_responses=True
)
dp = Dispatcher()
dp.message.middleware(
    UserLanguageMiddleware(redis, user_repo)
)
dp.callback_query.middleware(
    UserLanguageMiddleware(redis, user_repo)
)

@dp.message(CommandStart())
async def command_start_handler(message: Message, lang: str) -> None:
    """
    This handler receives messages with `/start` command
    """
    print(lang)
    user_info[message.from_user.id] = UserInfo(base_lang=DEFAULT_LANGUAGE)
    builder = InlineKeyboardBuilder()
    start_buttons = {
        "ru": ":Russia: Русский",
        "en": ":United_Kingdom: English",
    }
    start_buttons = {key: emoji.emojize(value) for key, value in start_buttons.items()}
    for slug, button in start_buttons.items():
        builder.button(text=button, callback_data=slug)
        builder.adjust(1, 1)
    await message.answer(
        MessageGetter.get_start_message(
            username=message.from_user.full_name,
            lang=user_info[message.from_user.id].base_lang,
        ),
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(lambda c: c.data in ("ru", "en"))
async def set_base_language(callback: CallbackQuery, lang: str) -> None:
    await user_repo.set_language(callback.from_user.id, callback.data)
    await redis.set(f"user:{callback.from_user.id}:lang", callback.data)
    await callback.message.answer(
        MessageGetter.get_language_chosen_message(Language(callback.data))
    )


@dp.message(Command("train"))
async def command_train_handler(message: Message, lang: str) -> None:
    user_stats[message.from_user.id] = UserStats()
    await choose_level(message, lang)


async def choose_level(message: Message, lang: str):
    LevelsVerbose.set_language(Language(lang))
    builder = InlineKeyboardBuilder()
    level_buttons = {
        "easy": LevelsVerbose.easy,
        "medium": LevelsVerbose.medium,
        "hard": LevelsVerbose.hard,
    }
    for slug, button in level_buttons.items():
        builder.button(text=button, callback_data=slug)
        builder.adjust(1, 1)
    await message.answer(
        MessageGetter.get_choose_level_message(
            lang=Language(lang),
        ),
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(lambda c: c.data in ("easy", "medium", "hard"))
async def set_level(callback: CallbackQuery, lang: str) -> None:
    user_info[callback.from_user.id].level = callback.data
    await callback.message.answer(
        MessageGetter.get_level_chosen_message(
            Language(lang),
        )
    )
    await choose_mode(callback, lang)


async def choose_mode(callback: CallbackQuery, lang: str):
    TrainingModeVerbose.set_language(Language(lang))
    builder = InlineKeyboardBuilder()
    mode_buttons = {
        "numbers_to_words": TrainingModeVerbose.numbers_to_words,
        "words_to_numbers": TrainingModeVerbose.words_to_numbers,
    }
    for slug, button in mode_buttons.items():
        builder.button(text=button, callback_data=slug)
        builder.adjust(1, 1)
    await callback.message.answer(
        MessageGetter.get_choose_mode_message(
            lang=Language(lang),
        ),
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(lambda c: c.data in ("numbers_to_words", "words_to_numbers"))
async def set_mode(callback: CallbackQuery, lang: str) -> None:
    user_info[callback.from_user.id].mode = callback.data
    await callback.message.answer(
        MessageGetter.get_mode_chosen_message(
            Language(lang),
        )
    )
    builder = InlineKeyboardBuilder()
    ButtonsVerbose.set_language(Language(lang))
    builder.button(text=ButtonsVerbose.start, callback_data="start")
    builder.adjust(1, 1)
    await callback.message.answer(
        MessageGetter.get_training_prompt_message(
            Language(lang),
        ),
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(lambda c: c.data in ("start", "next"))
async def start_training(callback: CallbackQuery, lang: str):
    builder = InlineKeyboardBuilder()
    ButtonsVerbose.set_language(Language(lang))
    builder.button(text=ButtonsVerbose.finish, callback_data="finish")
    builder.adjust(1, 1)
    training = TrainingGenerator.generate(
        mode=user_info[callback.from_user.id].mode,
        level=user_info[callback.from_user.id].level,
    )
    current_trainings[callback.from_user.id] = training
    await callback.message.answer(
        MessageGetter.get_training_guess_message(
            training=training,
            mode=user_info[callback.from_user.id].mode,
            lang=Language(lang),
        ),
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(lambda c: c.data == "finish")
async def finish_training(callback: CallbackQuery, lang: str):
    current_trainings.pop(callback.from_user.id, None)
    await callback.message.answer(
        MessageGetter.get_finish_training_message(
            total=user_stats[callback.from_user.id].total,
            right=user_stats[callback.from_user.id].right,
            lang=Language(lang),
        ),
    )


@dp.message()
async def text_handler(message: Message, lang: str) -> None:
    builder = InlineKeyboardBuilder()
    ButtonsVerbose.set_language(Language(lang))
    builder.button(text=ButtonsVerbose.finish, callback_data="finish")
    builder.button(text=ButtonsVerbose.next, callback_data="next")
    builder.adjust(1, 1)

    if message.from_user.id in current_trainings.keys():
        user_stats[message.from_user.id].total += 1
        if message.text.strip() == current_trainings[message.from_user.id][1]:
            user_stats[message.from_user.id].right += 1
            await message.answer(
                MessageGetter.get_right_answer_message(
                    lang=Language(lang)
                ),
                reply_markup=builder.as_markup(),
            )
        else:
            await message.answer(
                MessageGetter.get_wrong_answer_message(
                    right_answer=current_trainings[message.from_user.id][1],
                    lang=Language(lang),
                ),
                reply_markup=builder.as_markup(),
            )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
