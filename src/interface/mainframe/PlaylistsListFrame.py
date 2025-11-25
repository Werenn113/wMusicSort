from functools import partial
from typing import Callable
import customtkinter
from src.clients.SpotifyClient import SpotifyClient
from src.types.Types import Playlist


class PlaylistsListFrame(customtkinter.CTkScrollableFrame):
    """
    Frame affichant la liste des playlists de l'utilisateur

    Attributes:
        __spotify (SpotifyClient) : client spotify
        __on_select_callback (Callable[[Playlist], None]) : callback vers la fonction qui affiche le contenu de la playlist
    """
    def __init__(self, master: customtkinter.CTkFrame, spotify: SpotifyClient, on_select: Callable[[Playlist], None], **kwargs) -> None:
        """
        Initialise une instance de PlaylistsListFrame

        Args:
            master (customtkinter.CTkFrame) : frame qui affiche cette frame (MainFrame)
            spotify (SpotifyClient) : client Spotify
            on_select (Callable[[Playlist], None]) : callback vers la fonction qui affiche le contenu de la playlist
            **kwargs : autres arguments
        """
        super().__init__(master, **kwargs)
        self.__spotify = spotify
        self.__on_select_callback = on_select
        self.configure(label_text="MES PLAYLISTS")

        self.__get_playlists()


    def __get_playlists(self) -> None:
        """
        Récupère les playlists de l'utilisateur et crée un bouton par playlist (uniquement celles créées par l'utilisateur)
        """
        user_id = self.__spotify.get_user_id()
        playlists = self.__spotify.get_playlists()
        for playlist in playlists:
            if playlist.owner_id == user_id:
                self.__create_playlist_button(playlist=playlist)


    def __create_playlist_button(self, playlist: Playlist) -> None:
        """
        Crée un bouton pour une playlist. Lors du click du bouton, appelle le callback avec la playlist comme argument
        afin d'afficher le contenu de la playlist.

        Args:
            playlist (Playlist) : la playlist
        """
        customtkinter.CTkButton(
            master=self,
            text=playlist.name,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray25"),
            anchor = "w",
            command=partial(self.__on_select_callback, playlist)
        ).pack(fill="x", pady=2, padx=5)