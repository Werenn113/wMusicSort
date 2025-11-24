import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.types.Types import Song


class MusicBrainzClient:
    """
    Gère la récupération de données via l'API de musicbrainz

    Attributes:
        __base_url (str) : url de base pour toutes les requêtes
    """

    def __init__(self) -> None:
        """
        Initialise une instance de MusicBrainzClient
        """
        self.__base_url = "https://musicbrainz.org/ws/2/"
        self.__session = requests.Session()
        self.__session.headers.update({'User-Agent': 'wMusicSort/1.0 ( b.marchand@gmail.com )'})

        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        self.__session.mount('https://', HTTPAdapter(max_retries=retries))

    def __get_song_mbid(self, song: Song) -> str:
        """
        Récupère l'id musicbrainz d'une musique

        Args:
            song (Song) : song

        Returns:
            str : l'id de la musique ou Unknow s'il n'est pas trouvé
        """
        params = {
            "query": f"isrc:{song.isrc}",
            "fmt": "json"
        }

        try:
            response = self.__session.get(self.__base_url + "recording", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('count', 0) > 0:
                return data['recordings'][0]['id']
            else:
                return "Unknow"
        except (requests.exceptions.RequestException, ValueError):
            return "Unknow"

    def get_song_genre(self, song: Song) -> str:
        """
        Récupère le genre de la musique

        Args:
            song (Song) : la musique

        Returns:
            str : le genre de la musique
        """
        mbid = self.__get_song_mbid(song=song)

        if mbid == "Unknow":
            return "mbid not found"

        url = self.__base_url + f"recording/{mbid}"

        params = {
            "fmt": "json",
            "inc": "tags"  # Demande d'inclure les tags (genres)
        }

        try:
            response = self.__session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'tags' in data and data['tags']:
                sorted_tags = sorted(data['tags'], key=lambda tag: tag['count'], reverse=True)

                # Le genre est le 'name' du tag le plus populaire
                most_popular_genre = sorted_tags[0]['name']
                return most_popular_genre
            else:
                # Si aucun tag n'est trouvé
                return "Unknow"
        except (requests.exceptions.RequestException, ValueError):
            return "Unknow"
