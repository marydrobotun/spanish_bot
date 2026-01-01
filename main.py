import asyncio
import dataclasses
import logging
import sys
from os import getenv

import emoji
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.filters.command import Command
from base import Language
from levelsverbose import LevelsVerbose
from message import MessageGetter
from training_mode import TrainingModeVerbose
from training_generator import TrainingGenerator

@dataclasses.dataclass
class UserInfo:
    base_lang: Language
    level: str | None = None
    mode: str | None = None


TOKEN = getenv('TOKEN')
DEFAULT_LANGUAGE = Language.RU

user_info = {}
current_trainings = {}

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    user_info[message.from_user.id] = UserInfo(base_lang=DEFAULT_LANGUAGE)
    builder = InlineKeyboardBuilder()
    start_buttons = {
        'ru': ':Russia: Русский',
        'en': ':United_Kingdom: English',
    }
    start_buttons = {key: emoji.emojize(value) for key, value in start_buttons.items()}
    for slug, button in start_buttons.items():
        builder.button(text=button, callback_data=slug)
        builder.adjust(1, 1)
    await message.answer(
        MessageGetter.get_start_message(
            username=message.from_user.full_name, lang=user_info[message.from_user.id].base_lang),
        reply_markup=builder.as_markup()
    )


@dp.callback_query(lambda c: c.data in ('ru', 'en'))
async def set_base_language(callback: CallbackQuery):
    user_info[callback.from_user.id].base_lang = Language(callback.data)
    await callback.message.answer(MessageGetter.get_language_chosen_message(Language(callback.data)))
    await choose_level(callback)


async def choose_level(callback: CallbackQuery):
    LevelsVerbose.set_language(user_info[callback.from_user.id].base_lang)
    builder = InlineKeyboardBuilder()
    level_buttons = {
        'easy': LevelsVerbose.easy,
        'medium': LevelsVerbose.medium,
        'hard': LevelsVerbose.hard,
    }
    for slug, button in level_buttons.items():
        builder.button(text=button, callback_data=slug)
        builder.adjust(1, 1)
    await callback.message.answer(
        MessageGetter.get_choose_level_message(lang=user_info[callback.from_user.id].base_lang),
        reply_markup=builder.as_markup()
    )

@dp.callback_query(lambda c: c.data in ('easy', 'medium', 'hard'))
async def set_level(callback: CallbackQuery):
    user_info[callback.from_user.id].level = callback.data
    await callback.message.answer(MessageGetter.get_level_chosen_message(user_info[callback.from_user.id].base_lang))
    await choose_mode(callback)

async def choose_mode(callback: CallbackQuery):
    TrainingModeVerbose.set_language(user_info[callback.from_user.id].base_lang)
    builder = InlineKeyboardBuilder()
    mode_buttons = {
        'numbers_to_words': TrainingModeVerbose.numbers_to_words,
        'words_to_numbers': TrainingModeVerbose.words_to_numbers,
    }
    for slug, button in mode_buttons.items():
        builder.button(text=button, callback_data=slug)
        builder.adjust(1, 1)
    await callback.message.answer(
        MessageGetter.get_choose_mode_message(lang=user_info[callback.from_user.id].base_lang),
        reply_markup=builder.as_markup()
    )

@dp.callback_query(lambda c: c.data in ('numbers_to_words', 'words_to_numbers'))
async def set_mode(callback: CallbackQuery):
    user_info[callback.from_user.id].mode = callback.data
    await callback.message.answer(MessageGetter.get_mode_chosen_message(user_info[callback.from_user.id].base_lang))
    await callback.message.answer(MessageGetter.get_training_prompt_message(user_info[callback.from_user.id].base_lang))

@dp.message(Command('train'))
async def command_start_handler(message: Message) -> None:
    training = TrainingGenerator.generate(mode=user_info[message.from_user.id].mode, level=user_info[message.from_user.id].level)
    current_trainings[message.from_user.id] = training
    await message.answer(MessageGetter.get_training_guess_message(training, user_info[message.from_user.id].mode, user_info[message.from_user.id].base_lang))

@dp.message()
async def text_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    pass



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
