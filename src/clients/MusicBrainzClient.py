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

        retries = Retry(
            total=5,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )
        self.__session.mount('https://', HTTPAdapter(max_retries=retries))

        self.__genre_mapping = {
            # ROCK et ses variantes
            'rock': 'rock',
            'metal': 'rock',  # "alternative metal" deviendra "rock"
            'punk': 'rock',
            'grunge': 'rock',
            'indie': 'rock',

            # RAP et ses variantes
            'rap': 'rap',
            'hip hop': 'rap',  # "hip hop" deviendra "rap"
            'hip-hop': 'rap',
            'trap': 'rap',
            'urban': 'rap',

            # ELECTRO et ses variantes
            'electro': 'electro',
            'house': 'electro',
            'techno': 'electro',
            'dance': 'electro',
            'edm': 'electro',
            'trance': 'electro',

            # POP
            'pop': 'pop',
        }


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
                genre_scores = {genre: 0 for genre in set(self.__genre_mapping.values())}

                for tag in data['tags']:
                    tag_name = tag['name'].lower()
                    tag_count = tag['count']

                    found_genres_for_this_tag = set()

                    for keyword, main_genre in self.__genre_mapping.items():
                        if keyword in tag_name:
                            found_genres_for_this_tag.add(main_genre)

                    # On distribue les points
                    for genre in found_genres_for_this_tag:
                        genre_scores[genre] += tag_count

                # --- DÉCISION FINALE ---

                # On cherche le genre avec le score maximum
                best_genre = max(genre_scores, key=genre_scores.get)
                max_score = genre_scores[best_genre]

                # Si le score est 0, c'est qu'aucun mot clé n'a été trouvé
                if max_score == 0:
                    return "Other"

                # GESTION DES ÉGALITÉS PARFAITES (Optionnel mais recommandé)
                # Si par miracle Pop et Rock ont exactement le même score final, on peut forcer une priorité.
                # Par exemple, si on préfère classer en Rock plutôt qu'en Pop en cas d'égalité :
                if best_genre == 'pop' and genre_scores.get('rock', 0) == max_score:
                    return 'rock'

                return best_genre

            else:
                return "Unknow"
        except (requests.exceptions.RequestException, ValueError):
            return "Unknow"
