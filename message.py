import emoji
from settings import DEFAULT_LANGUAGE
from base import Language
from aiogram import html

class MessageGetter:

    @classmethod
    def get_start_message(cls, username: str, lang: Language = Language(DEFAULT_LANGUAGE)) -> str:
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
    def get_language_chosen_message(cls, lang: Language = Language(DEFAULT_LANGUAGE)) -> str:
        if lang == Language.RU:
            return 'Базовый язык установлен.'
        if lang == Language.EN:
            return 'Base language has been set.'
        else:
            raise NotImplemented

    @classmethod
    def get_choose_level_message(cls, lang: Language = Language(DEFAULT_LANGUAGE)) -> str:
        if lang == Language.RU:
            return 'Выбери уровень сложности:'
        if lang == Language.EN:
            return 'Please choose a difficulty level:'
        else:
            raise NotImplemented

    @classmethod
    def get_level_chosen_message(cls, lang: Language = Language(DEFAULT_LANGUAGE)) -> str:
        if lang == Language.RU:
            return 'Уровень сложности установлен.'
        if lang == Language.EN:
            return 'The difficulty level has been set.'
        else:
            raise NotImplemented

    @classmethod
    def get_choose_mode_message(cls, lang: Language = Language(DEFAULT_LANGUAGE)) -> str:
        if lang == Language.RU:
            return 'Выбери режим тренировки:'
        if lang == Language.EN:
            return 'Please choose a training mode:'
        else:
            raise NotImplemented

    @classmethod
    def get_mode_chosen_message(cls, lang: Language = Language(DEFAULT_LANGUAGE)) -> str:
        if lang == Language.RU:
            return 'Режим тренировки установлен.'
        if lang == Language.EN:
            return 'The training mode has been set.'
        else:
            raise NotImplemented

    @classmethod
    def get_training_prompt_message(cls, lang: Language = Language(DEFAULT_LANGUAGE)) -> str:
        if lang == Language.RU:
            return 'Отлично, теперь используй команду /train, чтобы начать тренировку, когда будешь готов.'
        if lang == Language.EN:
            return 'Great! Now you can use /train whenever you are ready to train.'
        else:
            raise NotImplemented

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
            raise NotImplemented