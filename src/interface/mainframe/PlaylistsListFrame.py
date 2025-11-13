from collections.abc import Callable

import customtkinter
from src.SpotifyExtractor import SpotifyExtractor


class PlaylistsListFrame(customtkinter.CTkScrollableFrame):
    # Frame scrollable affichant les playlists personnelles de l'utilisateur.
    def __init__(self, master, spotify: SpotifyExtractor, on_select:Callable[[str], None], **kwargs):
        super().__init__(master, **kwargs)
        self.__spotify = spotify
        self.__on_select_callback = on_select

        self.__create_widgets()
        self._scrollbar.grid_remove()  # Masque la scrollbar

    def __create_widgets(self) -> None:
        # Récupère les playlists et affiche uniquement celles de l'utilisateur connecté
        user_id = self.__spotify.get_user_id()
        playlists = self.__spotify.get_playlists()
        for playlist in playlists:
            if playlist['owner']['id'] == user_id:
                self.__create_playlist_button(playlist)

    def __create_playlist_button(self, playlist: dict) -> None:
        # Crée un label pour chaque playlist avec son nom et nombre de titres
        button = customtkinter.CTkButton(
            master=self,
            text=f"{playlist['name']} ({playlist['tracks']['total']})",
            width=200,
            height=30,
            corner_radius=10,
            fg_color=("gray60", "gray75"),  # Couleur de fond alternée (clair/sombre)
            command=lambda pid=playlist['id']: self.__on_select_callback(pid)
        )
        button.grid(padx=10, pady=5, sticky="w")