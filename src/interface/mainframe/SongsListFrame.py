import customtkinter
from src.clients.SpotifyClient import SpotifyClient
from src.clients.MusicBrainzClient import MusicBrainzClient
from src.types.Types import Playlist, Song


class SongsListFrame(customtkinter.CTkScrollableFrame):
    """
    Frame affichant la liste des musiques d'une playlist

    Attributes:
        __spotify (SpotifyClient) : client spotify
        __music_brainz (MusicBrainzClient) : client musicbrainz
        __playlist (Playlist) : la playlist à afficher
        __songs (list[Song]) : la liste des musiques de la playlist
        __genre_labels (list[customtkinter.CTkLabel]) : liste des boutons pour pouvoir les activer lorsque l'analyse est fini
    """
    def __init__(self, master: customtkinter.CTkFrame, spotify: SpotifyClient, music_brainz: MusicBrainzClient, playlist: Playlist, **kwargs) -> None:
        """
        Initialise une instance de SongsListFrame

        Args:
            master (customtkinter.CTkFrame) : frame qui affiche cette frame (MainFrame)
            spotify (SpotifyClient) : client spotify
            music_brainz (MusicBrainzClient) : client musicbrainz
            playlist (Playlist) : la playlist
            **kwargs : autres arguments
        """
        super().__init__(master, **kwargs)
        self.__spotify = spotify
        self.__music_brainz = music_brainz
        self.__playlist = playlist
        self.__songs: list[Song] = self.__spotify.get_song_from_playlist(playlist=self.__playlist)
        self.__genre_labels: list[customtkinter.CTkLabel] = []

        self.grid_columnconfigure(index=0, weight=3)  # Titre
        self.grid_columnconfigure(index=1, weight=2)  # Artiste
        self.grid_columnconfigure(index=2, weight=1)  # Durée
        self.grid_columnconfigure(index=3, weight=2)  # Genre

        self.__create_header()
        self.__populate_songs()


    @property
    def songs(self) -> list[Song]:
        return self.__songs


    def __create_header(self) -> None:
        """
        Crée les headers du tableau
        """
        headers = ["#", "TITRE", "ARTISTE", "DURÉE", "GENRE"]
        for i, h in enumerate(headers):
            customtkinter.CTkLabel(
                master=self,
                text=h,
                text_color="gray",
                font=("Arial", 12, "bold"),
                anchor="w"
            ).grid(row=0, column=i, sticky="ew", pady=(0, 10), padx=5)


    def __populate_songs(self) -> None:
        """
        Rempli le tableau avec les données des musiques
        """
        for i in range(1, len(self.__songs)):
            song = self.__songs[i-1]

            # Numéro
            customtkinter.CTkLabel(
                master=self,
                text=str(i),
                font=("Arial", 13, "bold"),
                anchor="w"
            ).grid(row=i, column=0, sticky="ew", pady=5, padx=5)

            # Titre
            customtkinter.CTkLabel(
                master=self,
                text=song.name,
                font=("Arial", 13, "bold"),
                anchor="w"
            ).grid(row=i, column=1, sticky="ew", pady=5, padx=5)

            # Artiste
            customtkinter.CTkLabel(
                master=self,
                text=song.artist,
                anchor="w"
            ).grid(row=i, column=2, sticky="ew", pady=5, padx=5)

            # Durée
            customtkinter.CTkLabel(
                master=self,
                text=song.duree,
                text_color="gray",
                anchor="w"
            ).grid(row=i, column=3, sticky="ew", pady=5, padx=5)

            # Label Genre
            genre_label = customtkinter.CTkLabel(
                master=self,
                text="?",
                text_color="gray50",
                anchor="w"
            )
            genre_label.grid(row=i, column=4, sticky="w", pady=5, padx=5)
            self.__genre_labels.append(genre_label)


    def update_song_genre(self, index: int) -> None:
        """
        Update le genre d'une musique dans le tableau __genre_labels

        Args:
            index (int) : l'index de la musique dans le tableau __genre_labels
        """
        if 0 <= index < len(self.__genre_labels):
            self.__genre_labels[index].configure(text=self.__songs[index].genre, text_color='#1DB954')