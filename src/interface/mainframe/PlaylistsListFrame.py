from functools import partial
import customtkinter
from src.Clients.SpotifyClient import SpotifyClient
from src.types.Types import Playlist


class PlaylistsListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, spotify: SpotifyClient, on_select, **kwargs):
        super().__init__(master, **kwargs)
        self.__spotify = spotify
        self.__on_select_callback = on_select
        self.configure(label_text="MES PLAYLISTS")  # Titre en haut

        self.__populate_playlists()


    def __populate_playlists(self):
        # Récupération des playlists (Simulation ou appel API)
        # playlists = self.spotify.get_user_playlists()
        user_id = self.__spotify.get_user_id()
        playlists = self.__spotify.get_playlists()
        for playlist in playlists:
            if playlist.owner_id == user_id:
                self.__create_playlist_button(playlist=playlist)


    def __create_playlist_button(self, playlist: Playlist) -> None:
        button = customtkinter.CTkButton(
            master=self,
            text=playlist.name,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray25"),
            anchor = "w",
            command=partial(self.__on_select_callback, playlist)
        )
        button.pack(fill="x", pady=2, padx=5)