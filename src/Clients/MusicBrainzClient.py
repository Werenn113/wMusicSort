import requests
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

        data = requests.get(self.__base_url + "recording", params=params, timeout=10).json()

        if data['count'] > 0:
            return data['recordings'][0]['id']
        else:
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

        data = requests.get(url, params).json()

        if 'tags' in data and data['tags']:
            sorted_tags = sorted(data['tags'], key=lambda tag: tag['count'], reverse=True)

            # Le genre est le 'name' du tag le plus populaire
            most_popular_genre = sorted_tags[0]['name']
            return most_popular_genre
        else:
            # Si aucun tag n'est trouvé
            return "Unknow"
