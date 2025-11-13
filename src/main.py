import os
from dotenv import load_dotenv

from src.GUI import GUI
from src.SpotifyExtractor import SpotifyExtractor

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

if __name__ == "__main__":
    app = GUI()
    app.mainloop()