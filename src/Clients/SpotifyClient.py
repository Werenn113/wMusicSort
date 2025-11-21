from typing import Optional
import spotipy
from spotipy import SpotifyOAuth, Spotify
from src.types.Types import Song, Playlist


class SpotifyClient:
    """
    Gère l'authentification et la récupération de données via l'API Spotify

    Attributes:
        __scope (str) : Les scopes garantissent que seules les infos choisies par l’utilisateur sont partagées avec l’appli
        __spotify (Spotify) : Client spotify
    """

    def __init__(self) -> None:
        """
        Initialise un nouveau SpotifyClient
        """
        self.__scope = "user-library-read playlist-read-private playlist-read-collaborative"
        self.__spotify: Optional[Spotify] = None


    def authentication(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        """
        Gère l'authentification du client spotify

        Args:
            client_id (str) : id du client (fourni par spotify
            client_secret (str) : secret du client (fourni par spotify)
            redirect_uri (str) : lien de redirection (à définir dans spotify)
        """
        self.__spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=self.__scope
            )
        )


    def get_user_id(self) -> str:
        """
        Retourne l'id de l'utilisateur courant

        Returns:
            str : id du client
        """
        return self.__spotify.current_user()['id']


    def get_playlists(self) -> list[Playlist]:
        """
        Retourne la liste des playlists de l'utilisateur courant

        Returns:
            list[Playlist] : liste des playlists de l'utilisateur
        """
        return [
            Playlist(
                id=playlist['id'],
                name=playlist['name'],
                owner_id=playlist['owner']['id'],
                number_of_track=playlist['tracks']['total']
            ) for playlist in self.__spotify.current_user_playlists()['items']
        ]


    def get_song_from_playlist(self, playlist: Playlist) -> list[Song]: # TODO : mieux gérer la pagination
        """
        Retourne la liste de toutes les musiques de la playlist en gérant la pagination

        Args:
            playlist (Playlist) : la playlist

        Returns:
            list[Song] : liste de toutes les musiques de la playlist
        """
        all_songs = []
        offset = 0
        limit = 100  # Limite maximale de l'API Spotify

        while True:
            results = self.__spotify.playlist_items(playlist_id=playlist.id, limit=limit, offset=offset)
            for song in results['items']:
                all_songs.append(
                    Song(
                        name=song['track']['name'],
                        artist=song['track']['artists'][0]['name'],
                        isrc=song['track']['external_ids']['isrc']
                    )
                )
            if results['next'] is None:
                break
            offset += limit

        return all_songs