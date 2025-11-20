import requests
from src.types.Types import Song, Tag


class LastFMExtractor:
    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key
        self.__base_url = "http://ws.audioscrobbler.com/2.0/"

        self.__tags = []
        self.__wanted_genres = ["rock", "pop"]

    def get_all_tags(self):
        params = {
            'method': 'tag.getTopTags',
            'api_key': self.__api_key,
            'format': 'json'
        }

        response = requests.get(self.__base_url, params=params)
        data = response.json()

    def __get_song_tags(self, song: Song) -> list[Tag]:
        params = {
            'method': 'track.gettoptags',
            'track': song.name,
            'artist': song.artist,
            'autocrecct': 0, # Transform misspelled artist and track names into correct artist and track names
            'api_key': self.__api_key,
            'format': 'json'
        }

        data = requests.get(self.__base_url, params=params).json()

        if 'toptags' in data and 'tag' in data['toptags']:
            tags = data['toptags']['tag']
            return [Tag(name=tag['name'], popularity=int(tag['count'])) for tag in tags]
        else:
            raise RuntimeError("Erreur lors de la récupération des tags")

    def get_song_genre(self, song: Song):
        tags = self.__get_song_tags(song=song)

        if len(tags) == 0:
            return "Inconnue"
        else:
            return tags[0].name
