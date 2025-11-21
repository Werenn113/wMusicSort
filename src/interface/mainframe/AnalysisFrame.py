import time

import customtkinter
import threading
from src.Clients.MusicBrainzClient import MusicBrainzClient


class AnalysisFrame(customtkinter.CTkFrame):
    # Ajout de on_analysis_finished dans les arguments
    def __init__(self, master, on_analysis_finished, music_brainz: MusicBrainzClient, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(height=80, fg_color="#1a1a1a")
        self.grid_columnconfigure(1, weight=1)

        self.__song_list_frame = None
        self.__music_brainz = music_brainz

        self.on_analysis_finished_callback = on_analysis_finished  # Le signal de fin

        # --- UI (Identique à ton code) ---
        self.btn_calculate = customtkinter.CTkButton(
            self, text="Lancer l'analyse IA", command=self.__start_analysis_process,
            font=("Arial", 14, "bold"), fg_color="#1DB954", hover_color="#1ed760", height=40
        )
        self.btn_calculate.grid(row=0, column=0, padx=20, pady=20)

        self.progress_bar = customtkinter.CTkProgressBar(self, orientation="horizontal", mode="determinate", height=10)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=0, column=1, padx=(0, 20), sticky="ew")
        self.progress_bar.configure(progress_color="#BB86FC")

        self.status_label = customtkinter.CTkLabel(self, text="En attente", text_color="gray")
        self.status_label.grid(row=0, column=2, padx=20)

    def set_song_list_frame(self, song_list_frame):
        self.__song_list_frame = song_list_frame

    def __start_analysis_process(self):
        # 1. On prévient que ça commence (visuel)
        self.btn_calculate.configure(state="disabled", text="Analyse...")
        self.status_label.configure(text="Connexion à l'IA...")

        # 2. On lance le vrai travail dans un Thread pour ne pas bloquer l'interface
        threading.Thread(target=self.__run_real_analysis, daemon=True).start()

    def __run_real_analysis(self):
        """C'est ici que le vrai calcul se fait"""
        songs = self.__song_list_frame.songs
        total_songs = len(songs)

        if total_songs == 0:
            self.__finish_process()
            return

        for i, song in enumerate(songs):
            # 1. Calcul du genre via l'API
            # Note: Assure-toi que get_song_genre retourne une string
            found_genre = self.__music_brainz.get_song_genre(song)
            song.genre = found_genre  # On met à jour l'objet Song directement

            # 2. Mise à jour de la barre (i + 1 car on commence à 0)
            progress = (i + 1) / total_songs
            self.progress_bar.set(progress)
            self.status_label.configure(text=f"Analyse : {song.name}")

            time.sleep(4)

        self.__finish_process()

    def __finish_process(self):
        """Nettoyage et signalement de fin"""
        self.status_label.configure(text="Terminé !")
        self.btn_calculate.configure(text="Analyse terminée", fg_color="gray")

        # C'est ici qu'on sonne la cloche pour le MainFrame !
        if self.on_analysis_finished_callback:
            self.on_analysis_finished_callback()