import customtkinter
from src.SpotifyExtractor import SpotifyExtractor
from src.interface.LoginFrame import LoginFrame
from src.interface.mainframe.MainFrame import MainFrame


class GUI(customtkinter.CTk):
    # Fenêtre principale de l'application : initialise Spotify, l'UI et affiche le login.
    def __init__(self) -> None:
        super().__init__()
        self.__spotify = SpotifyExtractor()  # instance pour interagir avec Spotify
        self.__setup_ui()  # configuration de la fenêtre
        self.__show_login_frame()  # afficher l'écran de connexion

    def __setup_ui(self) -> None:
        # Configuration basique de la fenêtre (taille, thème, layout)
        self.geometry("1000x550")
        self.title("wMusicSorter")
        self.resizable(True, True)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def __show_login_frame(self) -> None:
        # Crée et place le LoginFrame
        self.login_frame = (LoginFrame(
            master=self,
            width=340,
            height=420,
            corner_radius=20,
            spotify=self.__spotify,
            on_login_success_callback=self.__show_main_frame
        ))
        self.login_frame.grid(row=0, column=0, padx=20, pady=50, sticky="")

    def __show_main_frame(self) -> None:
        # Supprime l'écran de login et affiche le MainFrame principal.
        self.login_frame.destroy()

        self.main_frame = MainFrame(
            master=self,
            spotify=self.__spotify
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew")