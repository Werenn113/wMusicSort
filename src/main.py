import os
from dotenv import load_dotenv
from src.interface.GUI import GUI

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

if __name__ == "__main__":
    app = GUI()
    app.mainloop()

    # data_loader = DataLoader("src/classifier/data/dataset.csv")
    # classifier = Classifier(data_loader.X, data_loader.y, epochs=2000, batch_size=32)
    # classifier.train()
    # classifier.test()

