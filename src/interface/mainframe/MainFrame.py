import os
import customtkinter
# Plus besoin de threading ni de time ici !

from src.Clients.MusicBrainzClient import MusicBrainzClient
from src.Clients.SpotifyClient import SpotifyClient
from src.interface.mainframe.PlaylistsListFrame import PlaylistsListFrame
from src.interface.mainframe.SongsListFrame import SongsListFrame
from src.interface.mainframe.AnalysisFrame import AnalysisFrame
from src.types.Types import Playlist


class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTk, spotify: SpotifyClient, music_brainz: MusicBrainzClient, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.__spotify: SpotifyClient = spotify
        self.__music_brainz = music_brainz

        self.__spotify.authentication(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI')
        )

        self.grid_columnconfigure(0, weight=0) # la colonne zero à est plus petite que la colonne 1
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.__songs_list_frame = None

        self.__create_sidebar()
        self.__create_analysis_bar()


    def __create_sidebar(self) -> None:
        self.__playlists_list_frame = PlaylistsListFrame(
            master=self,
            width=200,
            corner_radius=0,
            spotify=self.__spotify,
            on_select=self.__handle_playlist_selection
        )
        self.__playlists_list_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")


    def __handle_playlist_selection(self, playlist: Playlist) -> None:
        if self.__songs_list_frame is not None:
            self.__songs_list_frame.destroy()

        self.__songs_list_frame = SongsListFrame(
            master=self,
            width=600,
            corner_radius=0,
            fg_color="transparent",
            spotify=self.__spotify,
            music_brainz=self.__music_brainz,
            playlist=playlist
        )
        self.__songs_list_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.__analysis_frame.set_song_list_frame(self.__songs_list_frame)


    def __create_analysis_bar(self) -> None:
        self.__analysis_frame = AnalysisFrame(
            master=self,
            on_analysis_finished=self.__handle_analysis_finished,  # <--- LE LIEN IMPORTANT
            corner_radius=0,
            music_brainz=self.__music_brainz,
        )
        self.__analysis_frame.grid(row=1, column=1, sticky="ew")


    def __handle_analysis_finished(self):
        """Cette fonction est appelée automatiquement quand AnalysisFrame a fini le travail"""
        print("MainFrame: Analyse terminée, activation des boutons.")
        if self.__songs_list_frame:
            self.__songs_list_frame.enable_reveal_buttons()