import os
from threading import Thread
from typing import Callable, Optional
import customtkinter
from src.clients.SpotifyClient import SpotifyClient


class LoginFrame(customtkinter.CTkFrame):
    """
    Fenêtre de connexion à l'API spotify

    Attributes:
        __spotify (SpotifyClient) : client spotify
        __on_login_success_callback (Callable[[], None]) : callback vers la fonction pour afficher la page suivante (mainframe)
        __client_id_entry: Optional[customtkinter.CTkEntry] : entrée pour le client id
        __client_secret_entry: Optional[customtkinter.CTkEntry] : entrée pour le client secret
        __redirect_uri_entry: Optional[customtkinter.CTkEntry] : entrée pour le uri de redirection
    """

    def __init__(self, master: customtkinter.CTk, spotify: SpotifyClient, on_login_success_callback: Callable[[], None], **kwargs) -> None:
        """
        Initialise une instance de LoginFrame

        Args:
            master (customtkinter.CTk) : fenêtre qui appelle cette fenêtre
            spotify (SpotifyClient) : client spotify
            on_login_success_callback (Callable[[], None]) : callback vers la fonction pour afficher la page suivante (mainframe)
            **kwargs: autres arguments (taille, corner_radius, ...)
        """
        super().__init__(master, **kwargs)
        self.__spotify: SpotifyClient = spotify
        self.__on_login_success_callback = on_login_success_callback

        self.__client_id_entry: Optional[customtkinter.CTkEntry] = None
        self.__client_secret_entry: Optional[customtkinter.CTkEntry] = None
        self.__redirect_uri_entry: Optional[customtkinter.CTkEntry] = None

        self.__create_login_form()


    def __create_login_form(self) -> None:
        """
        Crée tous les éléments du login form
        """
        # Logo
        customtkinter.CTkLabel(
            master=self,
            text='👤',
            font=('Arial', 100)
        ).grid(row=0, column=0, pady=(30, 20), padx=20)

        # Champ de saisie du client_id (récupéré depuis les variables d'environnement)
        self.__client_id_entry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Spotify Client ID",
            width=280,
            height=40,
            corner_radius=10, font=('Arial', 12)
        )
        self.__client_id_entry.grid(row=1, column=0, pady=10, padx=30)
        self.__client_id_entry.insert(0, os.getenv('SPOTIFY_CLIENT_ID'))

        # Champ de saisie du client_secret (récupéré depuis les variables d'environnement)
        self.__client_secret_entry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Spotify Client Secret",
            width=280,
            height=40,
            corner_radius=10,
            font=('Arial', 12),
            show="•"  # Masque le texte
        )
        self.__client_secret_entry.grid(row=2, column=0, pady=10, padx=30)
        self.__client_secret_entry.insert(0, os.getenv('SPOTIFY_CLIENT_SECRET'))

        # Champ de saisie du lien de redirection (récupéré depuis les variables d'environnement)
        self.__redirect_uri_entry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Redirect URI (ex: http://localhost:8888)",
            width=280,
            height=40,
            corner_radius=10,
            font=('Arial', 12)
        )
        self.__redirect_uri_entry.grid(row=3, column=0, pady=10, padx=30)
        self.__redirect_uri_entry.insert(0, os.getenv('SPOTIFY_REDIRECT_URI'))

        # Bouton de connexion
        customtkinter.CTkButton(
            master=self,
            text="Login",
            width=200,
            height=40,
            corner_radius=20,
            font=('Arial', 16, 'bold'),
            command=self.__login_event,
            hover_color="#037bfc"
        ).grid(row=4, column=0, pady=(20, 30), padx=20)


    def __login_event(self) -> None:
        """
        Récupère les identifiants et lance l'authentification dans un thread séparé pour ne pas bloquer l'interface
        graphique pendant le process
        """
        client_id = self.__client_id_entry.get()
        client_secret = self.__client_secret_entry.get()
        redirect_uri = self.__redirect_uri_entry.get()

        Thread(
            target=self.__authenticate_spotify,
            args=(client_id, client_secret, redirect_uri),
            daemon=True
        ).start()


    def __authenticate_spotify(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        """
        Authentifie avec Spotify puis appelle le callback vers la fonction pour afficher la page suivante (mainframe)
        sur le thread principal

        Args:
            client_id (str) : id du client
            client_secret (str) : secret du client
            redirect_uri (str) : lien de redirection du client
        """
        self.__spotify.authentication(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
        self.after(0, self.__on_login_success_callback)