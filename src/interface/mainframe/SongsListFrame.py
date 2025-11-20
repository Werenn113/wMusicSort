import os

import CTkTable
import customtkinter

from src.LastFMExtractor import LastFMExtractor
from src.SpotifyExtractor import SpotifyExtractor


class SongsListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, spotify: SpotifyExtractor, playlist_id: str, **kwargs):
        super().__init__(master, **kwargs)
        self.__spotify = spotify
        self.__playlist_id = playlist_id
        self.__songs = self.__spotify.get_song_from_playlist(self.__playlist_id)
        self.__lastfm_extractor = LastFMExtractor(os.getenv('LAST_FM_API_KEY'))

        self.__create_widgets()
        #self._scrollbar.grid_remove()  # Masque la scrollbar

        self.grid_columnconfigure(0, weight=1)

    def __create_widgets(self):
        songs = [[song.name, song.artist, song.genre] for song in self.__songs]
        self.__table = CTkTable.CTkTable(
            master=self,
            row=len(songs),
            column=3,
            values=songs
        )
        self.__table.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Bouton en dessous de la liste
        self.action_button = customtkinter.CTkButton(
            master=self,
            text="Get genres",
            width=250,
            command=self.__button_action
        )
        self.action_button.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="")


    def __button_action(self):
        for song in self.__songs:
            song.genre = self.__lastfm_extractor.get_song_genre(song)

        # Détruire l'ancienne table
        if self.__table:
            self.__table.destroy()

        # Recréer la table avec les nouvelles données
        songs = [[song.name, song.artist, song.genre] for song in self.__songs]
        self.__table = CTkTable.CTkTable(
            master=self,
            row=len(songs),
            column=3,
            values=songs
        )
        self.__table.grid(row=0, column=0, sticky="ew", padx=5, pady=5)