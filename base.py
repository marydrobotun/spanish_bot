import dataclasses
from enum import Enum


class Language(Enum):
    RU = 'ru'
    EN = 'en'


@dataclasses.dataclass
class UserInfo:
    base_lang: Language
    level: str | None = None
    mode: str | None = None


@dataclasses.dataclass
class UserStats:
    total: int = 0
    right: int = 0
