import spotipy
from spotipy import SpotifyOAuth, SpotifyException


class SpotifyExtractor:
    # Gère l'authentification et la récupération de données depuis l'API Spotify.
    def __init__(self) -> None:
        self.__scope = "user-library-read playlist-read-private playlist-read-collaborative"
        self.__sp = None  # Client Spotify (initialisé lors de l'authentification)

    def authentication(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        # Authentifie l'utilisateur avec les identifiants fournis
        self.__sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=self.__scope
        ))

    def get_user_id(self) -> str:
        # Retourne l'ID de l'utilisateur connecté
        return self.__sp.current_user()['id']

    def get_playlists(self) -> list:
        # Retourne la liste des playlists de l'utilisateur
        return self.__sp.current_user_playlists()['items']

    def get_song_from_playlist(self, playlist_id: str) -> list:
        """Retourne la liste de TOUTES les musiques de la playlist en gérant la pagination"""
        all_songs = []
        offset = 0
        limit = 100  # Limite maximale de l'API Spotify

        while True:
            results = self.__sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
            all_songs.extend(results['items'])
            if results['next'] is None:
                break
            offset += limit

        return all_songs