import emoji
from settings import DEFAULT_LANGUAGE
from base import Language
from aiogram import html


class MessageGetter:
    @classmethod
    def get_start_message(
        cls, username: str, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return emoji.emojize(
                f"Hola, {html.bold(username)}! Давай тренировать испанские числительные :Spain:"
                f"\n Выбери базовый язык:"
            )
        if lang == Language.EN:
            return emoji.emojize(
                f"Hola, {html.bold(username)}! Lets train spanish numbers together :Spain:"
                f"\n Please choose a base language:"
            )
        else:
            raise NotImplemented

    @classmethod
    def get_language_chosen_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return "Базовый язык установлен. Используй /train чтобы начать тренировку."
        if lang == Language.EN:
            return "Base language has been set. Start a new training by using /train."
        else:
            raise NotImplemented

    @classmethod
    def get_choose_level_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return "Выбери уровень сложности:"
        if lang == Language.EN:
            return "Please choose a difficulty level:"
        else:
            raise NotImplemented

    @classmethod
    def get_level_chosen_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return "Уровень сложности установлен."
        if lang == Language.EN:
            return "The difficulty level has been set."
        else:
            raise NotImplemented

    @classmethod
    def get_choose_mode_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return "Выбери режим тренировки:"
        if lang == Language.EN:
            return "Please choose a training mode:"
        else:
            raise NotImplemented

    @classmethod
    def get_mode_chosen_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return "Режим тренировки установлен."
        if lang == Language.EN:
            return "The training mode has been set."
        else:
            raise NotImplemented

    @classmethod
    def get_training_prompt_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return (
                "Отлично, нажми на кнопку, чтобы начать тренировку, когда будешь готов."
            )
        if lang == Language.EN:
            return "Great! Now press the button below whenever you are ready to train."
        else:
            raise NotImplemented

    @classmethod
    def get_training_guess_message(
        cls,
        training: tuple[str | int, int | str],
        mode: str,
        lang: Language = Language(DEFAULT_LANGUAGE),
    ) -> str:
        if lang == Language.RU and mode == "numbers_to_words":
            return f"Как по-испански будет {training[0]}?"
        elif lang == Language.EN and mode == "numbers_to_words":
            return f"How to say {training[0]} in Spanish?"
        elif lang == Language.RU and mode == "words_to_numbers":
            return f'Что означает "{training[0]}"? Напиши число.'
        elif lang == Language.EN and mode == "words_to_numbers":
            return f'What does "{training[0]}" mean? Write a number.'
        else:
            raise NotImplemented

    @classmethod
    def get_right_answer_message(
        cls, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return emoji.emojize(":check_mark_button: Правильно!")
        if lang == Language.EN:
            return emoji.emojize(":check_mark_button: Right!")
        else:
            raise NotImplemented

    @classmethod
    def get_wrong_answer_message(
        cls, right_answer: str, lang: Language = Language(DEFAULT_LANGUAGE)
    ) -> str:
        if lang == Language.RU:
            return emoji.emojize(
                f":cross_mark: Не совсем! Правильный ответ: {html.bold(right_answer)}"
            )
        if lang == Language.EN:
            return emoji.emojize(
                f":cross_mark: Wrong answer! The right answer is: {html.bold(right_answer)}"
            )
        else:
            raise NotImplemented

    @classmethod
    def get_finish_training_message(
        cls, right: int, total: int, lang: Language = Language(DEFAULT_LANGUAGE)
    ):
        if lang == Language.RU:
            return emoji.emojize(f'¡Hasta pronto! Вот статистика текущей тренировки:\n'
                                 f'Общее число ответов: {total}\n'
                                 f'Число правильных ответов: {right}\n'
                                 f'Процент правильных ответов: {html.bold(right/total*100)}%')
        if lang == Language.EN:
            return emoji.emojize(f'¡Hasta pronto! Here is your training stats:\n'
                                 f'Total answers: {total}\n'
                                 f'Right answers: {right}\n'
                                 f'Right answers percentage: {html.bold(right/total*100)}%')
        else:
            raise NotImplemented