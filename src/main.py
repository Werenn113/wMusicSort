import os
from dotenv import load_dotenv

from src.SpotifyExtractor import SpotifyExtractor
from src.interface.GUI import GUI
from src.interface.classifier.DataLoader import DataLoader
from src.interface.classifier.MusicGenreClassifier import MusicGenreClassifier

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

if __name__ == "__main__":
    #app = GUI()
    #app.mainloop()
    """
    spotify = SpotifyExtractor()
    spotify.authentication(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    spotify.get_extract_from_song_id("4puv2qkav9GQSL02X2pfMO")
    """

    data_loader = DataLoader()
    data_loader.load_dataset()
    model = MusicGenreClassifier()
    model.train(data_loader.getX, data_loader.gety)
    model.test()
