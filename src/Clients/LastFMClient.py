import re
import urllib.parse

import requests
from src.types.Types import Song, Tag


def clean_title(title):
    # Enlève les parenthèses (versions, remasters, etc.)
    title = re.sub(r"\(.*?\)", "", title)
    # Supprime "feat", "ft", etc.
    title = re.sub(r"(feat\.?|ft\.?).*", "", title, flags=re.IGNORECASE)
    return title.strip()


class LastFMClient:
    """
    Gère la récupération de données auprès de l'API de lastfm

    Attributes:
        __api_key (str) : la clé api de l'utilisateur
        __base_url (str) : l'url de base pour chaque requête vers l'api
    """

    def __init__(self, api_key: str) -> None:
        """
        Initialise une instance de LastFMClient

        Args:
            api_key (str) : la clé api de l'utilisateur
        """
        self.__api_key = api_key # TODO : récupérer ça via un form
        self.__base_url = "http://ws.audioscrobbler.com/2.0/"

        self.compteur = 0


    def get_all_tags(self): # FIXME : obsolète
        """
        Récupère tous les tags de lastfm (obsolète)
        """
        params = {
            'method': 'tag.getTopTags',
            'api_key': self.__api_key,
            'format': 'json'
        }

        response = requests.get(self.__base_url, params=params)
        data = response.json()


    def __get_song_tags(self, song: Song) -> list[Tag]:
        """
        Récupère les tags d'une musique

        Args:
            song (Song) : la musique

        Returns:
            list[Tag] : liste des tags de la musique
        """
        name = clean_title(song.name)
        artist = song.artist

        params = {
            'method': 'track.gettoptags',
            'track': name,
            'artist': artist,
            'autocorrect': 1, # Transform misspelled artist and track names into correct artist and track names
            'api_key': self.__api_key,
            'format': 'json'
        }

        data = requests.get(self.__base_url, params=params).json()

        if 'toptags' in data and 'tag' in data['toptags']:
            tags = data['toptags']['tag']
            return [Tag(name=tag['name'], popularity=int(tag['count'])) for tag in tags]
        else:
            print(f"Erreur lors de la récupération des tags de la musique : {name} - {artist} : {data}")
            return [Tag(name="Musique non trouvée", popularity=1)]


    def get_song_genre(self, song: Song) -> str:
        """
        Retourne le genre d'une musique

        Args:
            song (Song) : la musique

        Returns:
            str : le genre de la musique
        """
        tags = self.__get_song_tags(song=song)

        if len(tags) == 0:
            self.compteur += 1
            return "Inconnue"
        else:
            return tags[0].name
