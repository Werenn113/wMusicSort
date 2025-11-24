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
    duree: str
    isrc: str
    genre: Optional[str] = None


@dataclass
class Playlist:
    id: str
    name: str
    owner_id: str
    number_of_track: int