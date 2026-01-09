import emoji
from aiogram import html

from base import Language
from settings import DEFAULT_LANGUAGE
from typing import Literal, TypedDict
from enum import Enum

class TrainingMode(Enum):
    NUMBERS_TO_WORDS = "numbers_to_words"
    WORDS_TO_NUMBERS = "words_to_numbers"


# ===== Message keys =====

MessageKey = Literal[
    "start",
    "language_chosen",
    "choose_level",
    "level_chosen",
    "choose_mode",
    "mode_chosen",
    "training_prompt",
    "guess_numbers_to_words",
    "guess_words_to_numbers",
    "right",
    "wrong",
    "finish",
]


# ===== TypedDict for language messages =====

class LanguageMessages(TypedDict):
    start: str
    language_chosen: str
    choose_level: str
    level_chosen: str
    choose_mode: str
    mode_chosen: str
    training_prompt: str
    guess_numbers_to_words: str
    guess_words_to_numbers: str
    right: str
    wrong: str
    finish: str


# ===== Messages storage =====

MESSAGES: dict[Language, LanguageMessages] = {
    Language.RU: {
        "start": (
            "Hola, {username}! Давай тренировать испанские числительные :Spain:\n"
            "Выбери базовый язык:"
        ),
        "language_chosen": (
            "Базовый язык установлен. Используй /train чтобы начать тренировку."
        ),
        "choose_level": "Выбери уровень сложности:",
        "level_chosen": "Уровень сложности установлен.",
        "choose_mode": "Выбери режим тренировки:",
        "mode_chosen": "Режим тренировки установлен.",
        "training_prompt": (
            "Отлично, нажми на кнопку, чтобы начать тренировку, когда будешь готов."
        ),
        "guess_numbers_to_words": "Как по-испански будет {value}?",
        "guess_words_to_numbers": 'Что означает "{value}"? Напиши число.',
        "right": ":check_mark_button: Правильно!",
        "wrong": (
            ":cross_mark: Не совсем! Правильный ответ: {answer}"
        ),
        "finish": (
            ":waving_hand: ¡Hasta pronto!\n\n"
            ":bar_chart: Вот статистика текущей тренировки:\n"
            "Общее число ответов: {total}\n"
            "Число правильных ответов: {right}\n"
            "Процент правильных ответов: {percent}%"
        ),
    },
    Language.EN: {
        "start": (
            "Hola, {username}! Lets train spanish numbers together :Spain:\n"
            "Please choose a base language:"
        ),
        "language_chosen": (
            "Base language has been set. Start a new training by using /train."
        ),
        "choose_level": "Please choose a difficulty level:",
        "level_chosen": "The difficulty level has been set.",
        "choose_mode": "Please choose a training mode:",
        "mode_chosen": "The training mode has been set.",
        "training_prompt": (
            "Great! Now press the button below whenever you are ready to train."
        ),
        "guess_numbers_to_words": "How to say {value} in Spanish?",
        "guess_words_to_numbers": 'What does "{value}" mean? Write a number.',
        "right": ":check_mark_button: Right!",
        "wrong": (
            ":cross_mark: Wrong answer! The right answer is: {answer}"
        ),
        "finish": (
            ":waving_hand: ¡Hasta pronto!\n\n"
            ":bar_chart: Here is your training stats:\n"
            "Total answers: {total}\n"
            "Right answers: {right}\n"
            "Right answers percentage: {percent}%"
        ),
    },
}


class MessageGetter:
    @classmethod
    def get_start_message(
        cls, username: str, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return emoji.emojize(
                f'Hola, {html.bold(username)}! Давай тренировать испанские числительные :Spain:'
                f'\n Выбери базовый язык:'
            )
        if lang == Language.EN:
            return emoji.emojize(
                f'Hola, {html.bold(username)}! Lets train spanish numbers together :Spain:'
                f'\n Please choose a base language:'
            )
        else:
            raise NotImplemented

    @classmethod
    def get_language_chosen_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return 'Базовый язык установлен. Используй /train чтобы начать тренировку.'
        if lang == Language.EN:
            return 'Base language has been set. Start a new training by using /train.'
        else:
            raise NotImplementedError

    @classmethod
    def get_choose_level_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return 'Выбери уровень сложности:'
        if lang == Language.EN:
            return 'Please choose a difficulty level:'
        else:
            raise NotImplementedError

    @classmethod
    def get_level_chosen_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return 'Уровень сложности установлен.'
        if lang == Language.EN:
            return 'The difficulty level has been set.'
        else:
            raise NotImplementedError

    @classmethod
    def get_choose_mode_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return 'Выбери режим тренировки:'
        if lang == Language.EN:
            return 'Please choose a training mode:'
        else:
            raise NotImplementedError

    @classmethod
    def get_mode_chosen_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return 'Режим тренировки установлен.'
        if lang == Language.EN:
            return 'The training mode has been set.'
        else:
            raise NotImplementedError

    @classmethod
    def get_training_prompt_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return (
                'Отлично, нажми на кнопку, чтобы начать тренировку, когда будешь готов.'
            )
        if lang == Language.EN:
            return 'Great! Now press the button below whenever you are ready to train.'
        else:
            raise NotImplementedError

    @classmethod
    def get_training_guess_message(
        cls,
        training: tuple[str | int, int | str],
        mode: str,
        lang: Language = Language(DEFAULT_LANGUAGE),
    ) -> str:
        if lang == Language.RU and mode == 'numbers_to_words':
            return f'Как по-испански будет {training[0]}?'
        elif lang == Language.EN and mode == 'numbers_to_words':
            return f'How to say {training[0]} in Spanish?'
        elif lang == Language.RU and mode == 'words_to_numbers':
            return f'Что означает "{training[0]}"? Напиши число.'
        elif lang == Language.EN and mode == 'words_to_numbers':
            return f'What does "{training[0]}" mean? Write a number.'
        else:
            raise NotImplementedError

    @classmethod
    def get_right_answer_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return emoji.emojize(':check_mark_button: Правильно!')
        if lang == Language.EN:
            return emoji.emojize(':check_mark_button: Right!')
        else:
            raise NotImplementedError

    @classmethod
    def get_wrong_answer_message(
        cls, right_answer: str, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return emoji.emojize(
                f':cross_mark: Не совсем! Правильный ответ: {html.bold(right_answer)}'
            )
        if lang == Language.EN:
            return emoji.emojize(
                f':cross_mark: Wrong answer! The right answer is: {html.bold(right_answer)}'
            )
        else:
            raise NotImplementedError

    @classmethod
    def get_finish_training_message(
        cls, right: int, total: int, lang: Language = Language(DEFAULT_LANGUAGE)
    ):
        if lang == Language.RU:
            return emoji.emojize(
                f':waving_hand: ¡Hasta pronto!\n\n'
                f':bar_chart: Вот статистика текущей тренировки:\n'
                f'Общее число ответов: {total}\n'
                f'Число правильных ответов: {right}\n'
                f'Процент правильных ответов: {html.bold(right / total * 100)}%'
            )
        if lang == Language.EN:
            return emoji.emojize(
                f':waving_hand: ¡Hasta pronto!\n\n'
                f':bar_chart: Here is your training stats:\n'
                f'Total answers: {total}\n'
                f':bullseye: Right answers: {right}\n'
                f'Right answers percentage: {html.bold(right / total * 100)}%'
            )
        else:
            raise NotImplementedError
