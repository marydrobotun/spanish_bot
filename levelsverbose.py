from base import Language
from settings import DEFAULT_LANGUAGE


class LevelsVerbose:
    language: Language = Language(DEFAULT_LANGUAGE)

    @classmethod
    def set_language(cls, lang: Language):
        cls.language = lang

    @classmethod
    @property
    def easy(cls) -> str:
        if cls.language == Language.RU:
            return 'Легкий'
        if cls.language == Language.EN:
            return 'Easy'
        else:
            raise NotImplemented

    @classmethod
    @property
    def medium(cls) -> str:
        if cls.language == Language.RU:
            return 'Средний'
        if cls.language == Language.EN:
            return 'Medium'
        else:
            raise NotImplemented

    @classmethod
    @property
    def hard(cls) -> str:
        if cls.language == Language.RU:
            return 'Сложный'
        if cls.language == Language.EN:
            return 'Hard'
        else:
            raise NotImplemented
