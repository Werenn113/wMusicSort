import os
from threading import Thread
import customtkinter

from src.SpotifyExtractor import SpotifyExtractor


class LoginFrame(customtkinter.CTkFrame):
    # Écran de connexion : récupère les identifiants Spotify et lance l'authentification.
    def __init__(self, master, spotify: SpotifyExtractor, on_login_success_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.__spotify: SpotifyExtractor = spotify
        self.__on_login_success_callback = on_login_success_callback

        self.__create_widgets()

    def __create_widgets(self) -> None:
        # Logo utilisateur
        self.logo = customtkinter.CTkLabel(
            self,
            text='👤',
            font=('Arial', 100)
        )
        self.logo.grid(row=0, column=0, pady=(30, 20), padx=20)

        # Champs de saisie pour les identifiants Spotify (récupérés depuis les variables d'environnement)
        self.client_id_entry = customtkinter.CTkEntry(
            self,
            placeholder_text="Spotify Client ID",
            width=280,
            height=40,
            corner_radius=10, font=('Arial', 12)
        )
        self.client_id_entry.grid(row=1, column=0, pady=10, padx=30)
        self.client_id_entry.insert(0, os.getenv('SPOTIFY_CLIENT_ID'))

        self.client_secret_entry = customtkinter.CTkEntry(
            self,
            placeholder_text="Spotify Client Secret",
            width=280,
            height=40,
            corner_radius=10,
            font=('Arial', 12),
            show="•"  # Masque le texte pour la sécurité
        )
        self.client_secret_entry.grid(row=2, column=0, pady=10, padx=30)
        self.client_secret_entry.insert(0, os.getenv('SPOTIFY_CLIENT_SECRET'))

        self.redirect_uri_entry = customtkinter.CTkEntry(
            self,
            placeholder_text="Redirect URI (ex: http://localhost:8888)",
            width=280,
            height=40,
            corner_radius=10,
            font=('Arial', 12)
        )
        self.redirect_uri_entry.grid(row=3, column=0, pady=10, padx=30)
        self.redirect_uri_entry.insert(0, os.getenv('SPOTIFY_REDIRECT_URI'))

        # Bouton de connexion
        self.login_button = customtkinter.CTkButton(
            self,
            text="Login",
            width=200,
            height=40,
            corner_radius=20,
            font=('Arial', 16, 'bold'),
            command=self.__login_event,
            hover_color="#037bfc"
        )
        self.login_button.grid(row=4, column=0, pady=(20, 30), padx=20)

    def __login_event(self) -> None:
        # Récupère les identifiants et lance l'authentification dans un thread séparé
        client_id = self.client_id_entry.get()
        client_secret = self.client_secret_entry.get()
        redirect_uri = self.redirect_uri_entry.get()

        Thread(
            target=self.__authenticate_spotify,
            args=(client_id, client_secret, redirect_uri),
            daemon=True
        ).start()  # Ne pas bloquer l'interface graphique

    def __authenticate_spotify(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        # Authentifie avec Spotify puis appelle le callback sur le thread principal (requis pour Tkinter)
        self.__spotify.authentication(client_id, client_secret, redirect_uri)
        self.after(0, self.__on_login_success_callback)