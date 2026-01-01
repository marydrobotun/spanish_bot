from random import randint

from spanum.numbers_to_words import number_to_words


class TrainingGenerator:

    @classmethod
    def generate(cls, mode: str, level: str) -> tuple[int | str, str | int]:
        if level == 'easy':
            number = randint(0, 100)
        elif level == 'medium':
            number = randint(0, 1000)
        elif level == 'hard':
            number = randint(0, 1_000_000)
        else:
            raise NotImplemented

        if mode == 'numbers_to_words':
            return number, number_to_words(number)
        elif mode == 'words_to_numbers':
            return number_to_words(number), number
        else:
            raise NotImplemented