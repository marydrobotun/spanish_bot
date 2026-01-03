from base import Language
from settings import DEFAULT_LANGUAGE


class ButtonsVerbose:
    language: Language = Language(DEFAULT_LANGUAGE)

    @classmethod
    def set_language(cls, lang: Language):
        cls.language = lang

    @classmethod
    @property
    def start(cls) -> str:
        if cls.language == Language.RU:
            return "Начать тренировку"
        if cls.language == Language.EN:
            return "Start"
        else:
            raise NotImplemented

    @classmethod
    @property
    def finish(cls) -> str:
        if cls.language == Language.RU:
            return "Закончить тренировку"
        if cls.language == Language.EN:
            return "Finish"
        else:
            raise NotImplemented

    @classmethod
    @property
    def next(cls) -> str:
        if cls.language == Language.RU:
            return 'Следующее задание'
        if cls.language == Language.EN:
             return 'Next'
        else:
            raise NotImplemented