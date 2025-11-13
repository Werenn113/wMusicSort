import os
import librosa
import pandas
from tqdm import tqdm
import numpy as np


class DataLoader:
    def __init__(self):
        self.__dataset_path = 'data/genres_original'
        self.__dataset_file_name = 'dataset_features.csv'
        self.__genres = self.__get_genres()
        self.__X = []
        self.__y = []
        self.__file_name = []

    @property
    def getX(self) -> list:
        return self.__X

    @property
    def gety(self) -> list:
        return self.__y

    def __get_genres(self) -> list[str]:
        return [d for d in os.listdir(self.__dataset_path) if os.path.isdir(os.path.join(self.__dataset_path, d))]

    def load_dataset(self):
        if os.path.exists(self.__dataset_file_name):
            self.__load_from_csv(self.__dataset_file_name)
        else:
            # Compter le nombre total de fichiers
            total_files = 0
            files_by_genre = {}

            for genre in self.__genres:
                genre_path = os.path.join(self.__dataset_path, genre)
                files = [f for f in os.listdir(genre_path) if f.endswith('.wav')]
                files_by_genre[genre] = files
                total_files += len(files)

            # Créer une seule barre de progression pour tous les fichiers
            with tqdm(total=total_files, desc="🎵 Chargement du dataset", unit="fichier") as pbar:
                for genre in self.__genres:
                    genre_path = os.path.join(self.__dataset_path, genre)
                    files = files_by_genre[genre]

                    for file in files:
                        # Mettre à jour la description avec le genre actuel
                        pbar.set_postfix({"Genre": genre, "Fichier": file[:20]})

                        complete_path = os.path.join(genre_path, file)

                        try:
                            # Extraire les features
                            features = self.__extract_features(complete_path)

                            # Ajouter aux listes
                            self.__X.append(features)
                            self.__y.append(genre)
                            self.__file_name.append(file)

                        except Exception as e:
                            tqdm.write(f"❌ Erreur avec {file}: {e}")

                        # Avancer la barre de progression
                        pbar.update(1)
            self.__save_to_csv()

    def __extract_features(self, path):
        # Charger le fichier audio (30 secondes max)
        y, sr = librosa.load(path, duration=30)

        # 1. MFCC (13 coefficients) - timbre du son (différencie une voix d'une batterie)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)

        # 2. Chroma (12 notes) - (détecte les notes de musique)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)

        # 3. Spectral Centroid - centre de gravité (indique si le son est brillant ou aigu)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_centroid_mean = np.mean(spectral_centroid)

        # 4. Spectral Rolloff - (distingue les sons mous des sons criads - metal = rolloff eleve et folk acoustique rolloff bas)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        spectral_rolloff_mean = np.mean(spectral_rolloff)

        # 5. Zero Crossing Rate - (différencie les sons percussifs des sons harmoniques)
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_mean = np.mean(zcr)

        # 6. Tempo
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Combiner toutes les features
        features = np.hstack([
            mfcc_mean,  # 13 valeurs
            chroma_mean,  # 12 valeurs
            spectral_centroid_mean,  # 1 valeur
            spectral_rolloff_mean,  # 1 valeur
            zcr_mean,  # 1 valeur
            tempo  # 1 valeur
        ])

        return features

    def __save_to_csv(self, filename='dataset_features.csv'):
        """Sauvegarde les données dans un fichier CSV"""

        # Créer les noms de colonnes
        columns = []

        # MFCC (13 colonnes)
        for i in range(1, 14):
            columns.append(f'mfcc_{i}')

        # Chroma (12 colonnes)
        for i in range(1, 13):
            columns.append(f'chroma_{i}')

        # Autres features
        columns.extend([
            'spectral_centroid',
            'spectral_rolloff',
            'zero_crossing_rate',
            'tempo'
        ])

        # Créer le DataFrame
        df = pandas.DataFrame(self.__X, columns=columns)
        df['genre'] = self.__y
        df['filename'] = self.__file_name

        # Réorganiser les colonnes pour mettre filename et genre au début
        cols = ['filename', 'genre'] + columns
        df = df[cols]

        # Sauvegarder
        df.to_csv(filename, index=False)

    def __load_from_csv(self, filename='dataset_features.csv'):
        """Charge les données depuis un fichier CSV"""

        df = pandas.read_csv(filename)

        # Extraire les features (toutes les colonnes sauf filename et genre)
        feature_cols = [col for col in df.columns if col not in ['filename', 'genre']]
        self.__X = df[feature_cols].values.tolist()
        self.__y = df['genre'].tolist()
        self.__file_name = df['filename'].tolist()

        return True