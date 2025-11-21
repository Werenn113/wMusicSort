import customtkinter
from src.Clients.SpotifyClient import SpotifyClient
from src.Clients.MusicBrainzClient import MusicBrainzClient
from src.types.Types import Playlist, Song


class SongsListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, spotify: SpotifyClient, music_brainz: MusicBrainzClient, playlist: Playlist, **kwargs):
        super().__init__(master, **kwargs)
        self.__spotify = spotify
        self.__music_brainz = music_brainz
        self.__playlist = playlist
        self.__songs = self.__spotify.get_song_from_playlist(playlist=self.__playlist)
        self.__genre_buttons = []

        # Configuration colonnes
        self.grid_columnconfigure(0, weight=3)  # Titre
        self.grid_columnconfigure(1, weight=2)  # Artiste
        self.grid_columnconfigure(2, weight=1)  # Durée (Todo)
        self.grid_columnconfigure(3, weight=2)  # Genre (Bouton)

        self.__create_header()
        self.__populate_songs()


    @property
    def songs(self) -> list[Song]:
        return self.__songs


    def __create_header(self):
        headers = ["TITRE", "ARTISTE", "DURÉE", "GENRE"]
        for i, h in enumerate(headers):
            customtkinter.CTkLabel(
                master=self,
                text=h,
                text_color="gray",
                font=("Arial", 12, "bold"),
                anchor="w"
            ).grid(row=0, column=i, sticky="ew", pady=(0, 10), padx=5)


    def __populate_songs(self):
        row = 0
        for song in self.__songs:
            row += 1

            # Titre
            customtkinter.CTkLabel(
                master=self,
                text=song.name,
                font=("Arial", 13, "bold"),
                anchor="w"
            ).grid(row=row, column=0, sticky="ew", pady=5, padx=5)

            # Artiste
            customtkinter.CTkLabel(
                master=self,
                text=song.artist,
                anchor="w"
            ).grid(row=row, column=1, sticky="ew", pady=5, padx=5)

            # Durée (Todo)
            customtkinter.CTkLabel(
                master=self,
                text="--:--",
                text_color="gray",
                anchor="w"
            ).grid(row=row, column=2, sticky="ew", pady=5, padx=5)

            # Bouton Genre
            btn_reveal = customtkinter.CTkButton(
                master=self,
                text="?",
                width=60,
                height=24,
                fg_color="#333333",
                hover_color="#444444",
                state="disabled"
            )

            # --- CORRECTION CRUCIALE ---
            # On passe 'song' (l'objet) et pas 'song.genre' (qui est vide pour l'instant)
            btn_reveal.configure(command=lambda b=btn_reveal, s=song: self.__reveal_genre(b, s))

            btn_reveal.grid(row=row, column=3, sticky="w", pady=5, padx=5)
            self.__genre_buttons.append(btn_reveal)

    def __reveal_genre(self, btn, song_object):
        """Affiche le genre stocké dans l'objet song"""
        # On récupère le genre maintenant (après le calcul)
        genre_text = song_object.genre

        if not genre_text:
            genre_text = "Inconnu"

        btn.configure(
            text=genre_text,
            fg_color="transparent",
            state="disabled",
            text_color="#1DB954",
            width=60
        )

    def enable_reveal_buttons(self):
        for btn in self.__genre_buttons:
            btn.configure(state="normal", text="Révéler", fg_color="#6A0DAD")