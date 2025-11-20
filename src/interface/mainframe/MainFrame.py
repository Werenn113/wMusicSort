import customtkinter
from src.SpotifyExtractor import SpotifyExtractor
from src.interface.mainframe.PlaylistsListFrame import PlaylistsListFrame
from src.interface.mainframe.SongsListFrame import SongsListFrame


class MainFrame(customtkinter.CTkFrame):
    # Écran principal après authentification : affiche la liste des playlists Spotify.
    def __init__(self, master, spotify: SpotifyExtractor, **kwargs):
        super().__init__(master, **kwargs)
        self.__spotify: SpotifyExtractor = spotify
        self.__spotify.authentication()

        self.__create_widgets()
        self.grid_rowconfigure(0, weight=1)  # Ajuste la hauteur en fonction de l'espace disponible

    def __create_widgets(self) -> None:
        # Frame contenant la liste des playlists de l'utilisateur
        self.playlists_list_frame = PlaylistsListFrame(
            master=self,
            width=250,
            height=450,
            corner_radius=10,
            spotify=self.__spotify,
            on_select=self.__handle_playlist_selection
        )
        self.playlists_list_frame.grid(row=0, column=0, padx=20, pady=0, sticky="")

    def __handle_playlist_selection(self, playlist_id: str) -> None:
        self.songs_list_frame = SongsListFrame(
            master=self,
            width=610,
            height=450,
            corner_radius=10,
            spotify=self.__spotify,
            playlist_id=playlist_id
        )
        self.songs_list_frame.grid(row=0, column=1, padx=20, pady=0, sticky="")
