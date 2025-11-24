import os
from typing import Optional

import customtkinter
from src.Clients.MusicBrainzClient import MusicBrainzClient
from src.Clients.SpotifyClient import SpotifyClient
from src.interface.mainframe.PlaylistsListFrame import PlaylistsListFrame
from src.interface.mainframe.SongsListFrame import SongsListFrame
from src.interface.mainframe.AnalysisFrame import AnalysisFrame
from src.types.Types import Playlist


class MainFrame(customtkinter.CTkFrame):
    """
    Frame principale de l'application (affichages des playlists, des musiques et de leurs genres)

    Attributes:
        __spotify (SpotifyClient) : client spotify
        __music_brainz (MusicBrainzClient) : client musicbrainz
        __songs_list_frame (customtkinter.CTkFrame) : frame qui gère l'affichage des musiques
    """

    def __init__(self, master: customtkinter.CTk, spotify: SpotifyClient, music_brainz: MusicBrainzClient, **kwargs) -> None:
        """
        Initialise une instance de MainFrame

        Args:
            master (customtkinter.CTk) : fenêtre dans laquelle est affichée cette frame
            spotify (SpotifyClient) : client spotify
            music_brainz (MusicBrainzClient) : client musicbrainz
            **kwargs : autres arguments
        """
        super().__init__(master, **kwargs)
        self.__spotify = spotify
        self.__music_brainz = music_brainz
        self.__songs_list_frame: Optional[SongsListFrame] = None

        self.__spotify.authentication( # TODO : n'a pas de sens
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI')
        )

        self.grid_columnconfigure(0, weight=0) # la colonne zero à est plus petite que la colonne 1
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.__create_sidemenu()
        self.__create_analysis_bar()


    def __create_sidemenu(self) -> None:
        """
        Crée le menu de gauche permettant l'affichage des playlists
        """
        self.__playlists_list_frame = PlaylistsListFrame(
            master=self,
            width=200,
            corner_radius=0,
            spotify=self.__spotify,
            on_select=self.__handle_playlist_selection
        )
        self.__playlists_list_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")


    def __handle_playlist_selection(self, playlist: Playlist) -> None:
        """
        Gère la sélection d'une playlist

        Args:
            playlist (Playlist) : la playlist sélectionnée
        """
        self.__analysis_frame.stop_analysis()

        if hasattr(self, "__songs_list_frame") and self.__songs_list_frame.winfo_exists():
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
        self.__analysis_frame.song_list_frame = self.__songs_list_frame


    def __create_analysis_bar(self) -> None:
        """
        Affiche la bare de progression et le bouton pour l'analyse des genres
        """
        self.__analysis_frame = AnalysisFrame(
            master=self,
            corner_radius=0,
            music_brainz=self.__music_brainz,
        )
        self.__analysis_frame.grid(row=1, column=1, sticky="ew")