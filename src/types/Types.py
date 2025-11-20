from dataclasses import dataclass
from typing import Optional


@dataclass
class Tag:
    name: str
    popularity: int


@dataclass
class Song:
    name: str
    artist: str
    genre: Optional[str] = None