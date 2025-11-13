import spotipy
from spotipy import SpotifyOAuth


class SpotifyExtractor:
    def __init__(self) -> None:
        self.__scope = "user-library-read playlist-read-private playlist-read-collaborative"

        self.__sp = None

    def authentication(self, client_id, client_secret, redirect_uri) -> bool:
        self.__sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=self.__scope
        ))
        return True

    def print_user_data(self) -> None:
        user = self.__sp.current_user()
        print(f"Utilisateur : {user['display_name']}")
        print(f"ID : {user['id']}")

    def get_playlist(self) -> None:
        playlists = self.__sp.current_user_playlists()
        print("\n=== MES PLAYLISTS ===")
        for playlist in playlists['items']:
            print(f"- {playlist['name']} ({playlist['tracks']['total']} morceaux)")
            print(f"  ID: {playlist['id']}")