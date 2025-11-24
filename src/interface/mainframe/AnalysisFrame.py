import time
from typing import Optional
import customtkinter
import threading
from src.Clients.MusicBrainzClient import MusicBrainzClient
from src.interface.mainframe.SongsListFrame import SongsListFrame
from src.types.Types import Song


class AnalysisFrame(customtkinter.CTkFrame):
    """
    Frame affichant le bouton et la barre de progression pour l'analyse. Elle s'occupe aussi de la lancer

    Attributes:
        __song_list_frame (SongsListFrame) : la frame contenant les musiques
        __music_brainz (MusicBrainzClient) : client music brainz
        __abort_analysis (bool) : true si l'analyse doit être arrêtée
    """
    def __init__(self, master: customtkinter.CTkFrame, music_brainz: MusicBrainzClient, **kwargs) -> None:
        """
        Initialise une instance de AnalysisFrame

        Args:
            master (customtkinter.CTkFrame) : frame qui affiche cette frame (MainFrame)
            on_analysis_finished (Callable[[], None]) : callback vers la fonction qui va activer les boutons
            music_brainz (MusicBrainzClient) : client music brainz
            **kwargs : autres arguments
        """
        super().__init__(master, **kwargs)
        self.__music_brainz = music_brainz
        self.__song_list_frame: Optional[SongsListFrame] = None
        self.__abort_analysis = False
        self.__analysis_thread: Optional[threading.Thread] = None

        self.configure(height=80, fg_color="#1a1a1a")
        self.grid_columnconfigure(index=0, weight=0)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=0)
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=0)

        self.__create_start_button()
        self.__create_progress_bar()
        self.__create_status_label()
        self.__create_time_label()
        self.__create_stop_button()


    @property
    def song_list_frame(self) -> None:
        return self.__song_list_frame
    @song_list_frame.setter
    def song_list_frame(self, new_song_list_frame: customtkinter.CTkFrame) -> None:
        self.__song_list_frame = new_song_list_frame


    def __create_start_button(self) -> None:
        """
        Crée le bouton démarrant l'analyse
        """
        self.__button_start = customtkinter.CTkButton(
            master=self,
            text="Lancer l'analyse",
            command=self.__start_analysis_process,
            font=("Arial", 14, "bold"),
            fg_color="#1DB954",
            hover_color="#1ed760",
            height=40,
            state="disabled"
        )
        self.__button_start.grid(row=0, column=0, rowspan=2, padx=20, pady=10)


    def __create_progress_bar(self) -> None:
        """
        Crée la progress bar affichant la progression de l'analyse
        """
        self.__progress_bar = customtkinter.CTkProgressBar(
            master=self,
            orientation="horizontal",
            mode="determinate",
            height=10
        )
        self.__progress_bar.set(0)
        self.__progress_bar.grid(row=0, column=1, padx=10, sticky="ew")
        self.__progress_bar.configure(progress_color="#BB86FC")


    def __create_status_label(self) -> None: # TODO : avoir une taille fixe
        """
        Crée le label affichant le status de l'analyse
        """
        self.__status_label = customtkinter.CTkLabel(
            master=self,
            text="En attente",
            text_color="gray",
            font=("Arial", 11)
        )
        self.__status_label.grid(row=1, column=1, padx=10, sticky="nw")


    def __create_time_label(self) -> None:
        """
        Crée un label pour afficher le temps restant estimé
        """
        self.__time_label = customtkinter.CTkLabel(
            master=self,
            text="--:--",
            text_color="gray",
            font=("Arial", 11)
        )
        self.__time_label.grid(row=1, column=1, padx=10, sticky="ne")


    def __create_stop_button(self) -> None: # TODO : implémenter (pas forcément un stop button)
        """
        Bouton en plus pour plus tart
        """
        self.__button_stop = customtkinter.CTkButton(
            master=self,
            text="Stop",
            # command=self.stop_analysis,
            width=60,
            fg_color="gray",  # Gris par défaut car inactif
            hover_color="#cf3838",  # Rouge au survol
            state="disabled"
        )
        self.__button_stop.grid(row=0, column=2, rowspan=2, padx=20, pady=10)


    def __start_analysis_process(self) -> None:
        """
        Démarre l'analyse en lançant un thread (pour ne pas bloquer l'interface)
        """
        self.__abort_analysis = False
        self.__button_start.configure(state="disabled", text="Analyse...")
        self.__status_label.configure(text="Connexion à l'API")
        self.__time_label.configure(text="Calcul...")

        self.__analysis_thread = threading.Thread(target=self.__run_real_analysis, daemon=True)
        self.__analysis_thread.start()


    def __run_real_analysis(self) -> None:
        """
        Effectue l'analyse et update les label de genres pour les afficher en temps réel
        """
        songs = self.__song_list_frame.songs
        total_songs = len(songs)
        self.__time_average = 0

        if total_songs == 0:
            self.master.after(0, self.__finish_process)
            return

        analysis_start_time = time.time()
        for i, song in enumerate(songs):
            if self.__abort_analysis:
                return

            loop_start_time = time.time()

            self.__analyze_song(i, song)
            self.master.after(0, self.__update_progress_bar_and_status, i, total_songs, song)

            # 3. Gérer le rate limiting de l'API (1 requête / sec)
            elapsed_loop_time = time.time() - loop_start_time
            if elapsed_loop_time < 1.0:
                time.sleep(1.0 - elapsed_loop_time)
            self.master.after(0, self.__update_time_left, i, total_songs, time.time() - loop_start_time)

        self.master.after(0, self.__finish_process)


    def __analyze_song(self, index: int, song) -> None:
        """
        Récupère le genre d'un morceau et met à jour la liste de manière thread safe.

        Args:
            index (int) : numéro de la musique (pour pouvoir modifier la bonne ligne dans le tableau)
            song (Song) : la musique
        """
        found_genre = self.__music_brainz.get_song_genre(song)
        song.genre = found_genre
        self.master.after(0, self.__song_list_frame.update_song_genre, index)


    def __update_progress_bar_and_status(self, index: int, total_songs: int, song: Song) -> None:
        """
        Met à jour la barre de progression et les labels d'information. Cette méthode est destinée à être appelée via `master.after`

        Args:
            index (int) : le numéro de la musique
            total_songs (int) : nombre de musiques
            song (Song) : la musique
        """
        progress = (index + 1) / total_songs
        self.__progress_bar.set(progress)
        self.__status_label.configure(text=f"Analyse : {song.name}")


    def __update_time_left(self, index: int, total_songs:int, loop_time: float) -> None:
        """
        Met à jour le temps restant.

        Args:
            index (int) : le numéro de la musique
            total_songs (int) : nombre de musiques
            loop_time (float) : durée de l'itération actuelle
        """
        alpha = 0.05
        if self.__time_average == 0:
            self.__time_average = loop_time
        else:
            self.__time_average = (alpha * loop_time) + ((1-alpha) * self.__time_average)
            estimated_seconds_left = self.__time_average * (total_songs - (index + 1))
            mins, secs = divmod(estimated_seconds_left, 60)
            time_str = f"{int(mins):02d}:{int(secs):02d}"
            self.__time_label.configure(text=f"Restant : {time_str}")


    def __finish_process(self) -> None:
        """
        Termine l'analyse et appelle le callback pour afficher les boutons
        """
        self.__status_label.configure(text="Terminé !")
        self.__button_start.configure(text="Analyse terminée", fg_color="gray", state='normal')


    def stop_analysis(self) -> None:
        """
        Arrête l'analyse en cours (par exemple si on sélectionne une autre playlist
        """
        if self.__analysis_thread and self.__analysis_thread.is_alive():
            self.__abort_analysis = True
            self.__status_label.configure(text="Analyse annulée")
        self.__button_start.configure(state="normal", text="Lancer l'analyse", fg_color="#1DB954")
        self.__progress_bar.set(0)