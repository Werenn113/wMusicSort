import numpy
import seaborn
from keras import Input
from matplotlib import pyplot as plt
from pandas.core.interchange.dataframe_protocol import DataFrame
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from src.classifier.utils.LossGraph import LossGraph
from src.classifier.utils.ProgressBar import ProgressBar


class Classifier:
    def __init__(self, X: DataFrame, y: DataFrame, epochs = 5, batch_size = 32, split_ratio = 0.2, random_state = 42) -> None:
        self.__epochs = epochs
        self.__batch_size = batch_size

        # Normalisation
        self.__scaler = StandardScaler()
        X = self.__scaler.fit_transform(X)

        # Split
        self.__X_train, self.__X_test, self.__y_train, self.__y_test = train_test_split(
            X, y, test_size=split_ratio, random_state=random_state
        )

        # Encodage des labels texte en entiers
        self.__label_encoder = LabelEncoder()
        self.__y_train = self.__label_encoder.fit_transform(self.__y_train)
        self.__y_test = self.__label_encoder.transform(self.__y_test)

        self.__genres = numpy.unique(self.__y_train)
        self.__n_classes = len(self.__genres)

        # Conversion en one-hot
        self.__y_train_oh = tensorflow.keras.utils.to_categorical(self.__y_train, num_classes=self.__n_classes)
        self.__y_test_oh = tensorflow.keras.utils.to_categorical(self.__y_test, num_classes=self.__n_classes)

        # Modèle Keras équivalent à MLPClassifier
        self.__model = Sequential([
            Input(shape=(self.__X_train.shape[1],)),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(self.__n_classes, activation='softmax')
        ])
        self.__model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

    def train(self) -> None:
        callbacks = [
            ProgressBar(batch_size=self.__batch_size, dataset_size=len(self.__X_train), epochs=self.__epochs),
            LossGraph(epochs=self.__epochs, show_graph=False)
        ]

        self.__model.fit(
            self.__X_train,
            self.__y_train_oh,
            epochs=self.__epochs,
            batch_size=self.__batch_size,
            verbose=0,
            callbacks=callbacks
        )

    def test(self) -> None:
        y_pred_probs = self.__model.predict(self.__X_test)
        y_pred = numpy.argmax(y_pred_probs, axis=1)
        accuracy = accuracy_score(self.__y_test, y_pred)
        print(f"\n🎯 Précision globale: {accuracy:.2%}")
        f = open(f"src/classifier/results/{self.__epochs}_epochs_accuracy_{accuracy:.2%}", "w")
        self.__plot_confusion_matrix(self.__y_test, y_pred)

    def __plot_confusion_matrix(self, y_true: DataFrame, y_pred: DataFrame) -> None:
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(16, 14))
        seaborn.heatmap(cm,
                    annot=False,
                    fmt='d',
                    cmap='Blues',
                    xticklabels=self.__label_encoder.classes_,
                    yticklabels=self.__label_encoder.classes_,
                    cbar_kws={'label': 'Nombre de prédictions'},
                    linewidths=0.5,
                    linecolor='gray',
                    square=True)
        plt.title('Matrice de Confusion', fontsize=16, fontweight='bold', pad=20)
        plt.ylabel('Vrai Genre', fontsize=12, fontweight='bold')
        plt.xlabel('Genre Prédit', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.yticks(rotation=0, fontsize=9)
        plt.tight_layout()
        plt.savefig(f"src/classifier/results/{self.__epochs}_confusion_matrix_epochs.png")
        print(f"📁 Matrice de confusion sauvegardé dans : src/classifier/results/{self.__epochs}_epochs_confusion_matrix.png")