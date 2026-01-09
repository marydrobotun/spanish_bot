from base import Language
from settings import DEFAULT_LANGUAGE


class TrainingModeVerbose:
    language: Language = Language(DEFAULT_LANGUAGE)

    @classmethod
    def set_language(cls, lang: Language):
        cls.language = lang

    @classmethod
    @property
    def numbers_to_words(cls) -> str:
        if cls.language == Language.RU:
            return 'Число -> Слово'
        if cls.language == Language.EN:
            return 'Number -> Word'
        else:
            raise NotImplemented

    @classmethod
    @property
    def words_to_numbers(cls) -> str:
        if cls.language == Language.RU:
            return 'Слово -> Число'
        if cls.language == Language.EN:
            return 'Word -> Number'
        else:
            raise NotImplemented
