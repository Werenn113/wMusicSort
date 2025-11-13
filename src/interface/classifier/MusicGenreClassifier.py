import numpy
import seaborn
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier


class MusicGenreClassifier:
    """Classificateur de genres musicaux basé sur Random Forest"""

    def __init__(self, n_estimators=100, max_depth=20, random_state=42):
        """
        Args:
            n_estimators: nombre d'arbres
            max_depth: profondeur maximale des arbres
            random_state: seed pour la reproductibilité
        """
        self.model = MLPClassifier(
            solver='lbfgs',
            alpha=1e-5,
            hidden_layer_sizes=(5, 2),
            random_state=1
        )
        self.__genres = None
        self.__X_train = None
        self.__X_test = None
        self.__y_train = None
        self.__y_test = None

    def train(self, X, y):
        self.__X_train, self.__X_test, self.__y_train, self.__y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )
        self.model.fit(self.__X_train, self.__y_train)
        self.__genres = numpy.unique(self.__y_train)

    def test(self):
        y_pred = self.model.predict(self.__X_test)
        accuracy = accuracy_score(self.__y_test, y_pred)
        print(f"\n🎯 Précision globale: {accuracy:.2%}")
        print("\n📋 Rapport détaillé:")
        print(classification_report(self.__y_test, y_pred))

        self.__plot_confusion_matrix(self.__y_test, y_pred)

    def __plot_confusion_matrix(self, y_true, y_pred):
        """Affiche la matrice de confusion"""
        cm = confusion_matrix(y_true, y_pred)

        plt.figure(figsize=(10, 8))
        seaborn.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=self.__genres,
                    yticklabels=self.__genres)
        plt.title('Matrice de Confusion')
        plt.ylabel('Vrai Genre')
        plt.xlabel('Genre Prédit')
        plt.tight_layout()
        plt.show()