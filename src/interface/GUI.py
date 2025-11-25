import json
import os
from typing import Optional
import customtkinter
from src.clients.MusicBrainzClient import MusicBrainzClient
from src.clients.SpotifyClient import SpotifyClient
from src.interface.LoginFrame import LoginFrame
from src.interface.mainframe.MainFrame import MainFrame


def is_already_connected() -> bool:
    """
    Retourne un true si l'utilisateur est connecté (présence d'un access_token dans le fichier .cache), false sinon

    Returns:
        booléen : true si l'utilisateur est connecté, false sinon
    """
    if not os.path.exists('.cache'):
        return False

    with open('.cache', 'r') as f:
        data = json.load(f)

    if 'access_token' in data:
        return True
    else:
        return False


class GUI(customtkinter.CTk):
    """
    Fenêtre principale de l'application et la logique de l'application

    Attributes:
        __spotify (SpotifyClient) : client spotify
        __music_brainz (MusicBrainzClient) : client musicbrainz
        __login_frame (Optional[LoginFrame]) : frame de connexion
        __main_frame (Optional[MainFrame]) : frame principale
    """

    def __init__(self) -> None:
        """
        Initialise une instance de GUI
        """
        super().__init__()

        self.__spotify: SpotifyClient = SpotifyClient()
        self.__music_brainz: MusicBrainzClient = MusicBrainzClient()

        self.__login_frame: Optional[LoginFrame] = None
        self.__main_frame: Optional[MainFrame] = None

        self.__setup_ui()

        if is_already_connected():
            self.__show_main_frame()
        else:
            self.__show_login_frame()


    def __setup_ui(self) -> None:
        """
        Défini les paramètres généraux de l'application (taille, thème, layout)
        """
        self.geometry("1000x550")
        self.title("wMusicSorter")
        self.resizable(width=True, height=True)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")

        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)


    def __show_login_frame(self) -> None:
        """
        Crée et place le LoginFrame
        """
        self.__login_frame = LoginFrame(
            master=self,
            width=340,
            height=420,
            corner_radius=20,
            spotify=self.__spotify,
            on_login_success_callback=self.__show_main_frame
        )

        self.__login_frame.grid(row=0, column=0, padx=20, pady=50, sticky="")


    def __show_main_frame(self) -> None:
        """
        Crée et place le MainFrame
        """
        if self.__login_frame is not None: # détruit le login frame s'il existe
            self.__login_frame.destroy()
            self.__login_frame = None

        MainFrame(
            master=self,
            spotify=self.__spotify,
            music_brainz=self.__music_brainz
        ).grid(row=0, column=0, sticky="nsew")
