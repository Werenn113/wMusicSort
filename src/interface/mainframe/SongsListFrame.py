import CTkTable
import customtkinter
from src.SpotifyExtractor import SpotifyExtractor


class SongsListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, spotify: SpotifyExtractor, playlist_id: str, **kwargs):
        super().__init__(master, **kwargs)
        self.__spotify = spotify
        self.__playlist_id = playlist_id

        self.__create_widgets()
        #self._scrollbar.grid_remove()  # Masque la scrollbar

        self.grid_columnconfigure(0, weight=1)

    def __create_widgets(self):
        songs = [[song['track']['name'], song['track']['artists'][0]['name']] for song in self.__spotify.get_song_from_playlist(self.__playlist_id)]
        table = CTkTable.CTkTable(
            master=self,
            row=len(songs),
            column=2,
            values=songs
        )
        table.grid(row=0, column=0, sticky="ew", padx=5, pady=5)