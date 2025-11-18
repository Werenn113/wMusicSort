import numpy as np
import seaborn
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

from src.classifier.utils.LossGraph import LossGraph
from src.classifier.utils.ProgressBar import ProgressBar


class MLP(nn.Module):
    def __init__(self, input_dim, n_classes):
        super().__init__()
        self.__fc1 = nn.Linear(input_dim, 32)
        self.__fc2 = nn.Linear(32, 32)
        self.__fc3 = nn.Linear(32, n_classes)

    def forward(self, x):
        x = nn.functional.relu(self.__fc1(x))
        x = nn.functional.relu(self.__fc2(x))
        output = self.__fc3(x)
        return output


class Classifier:
    def __init__(self, X, y, epochs=5, batch_size=32):
        self.__epochs = epochs

        # Normalisation
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Encode labels
        self.__label_encoder = LabelEncoder()
        y_train = self.__label_encoder.fit_transform(y_train)
        y_test = self.__label_encoder.transform(y_test)

        self.__n_classes = len(np.unique(y_train))

        # Convert to tensors
        self.__X_train = torch.tensor(X_train, dtype=torch.float32)
        self.__X_test = torch.tensor(X_test, dtype=torch.float32)
        self.__y_train = torch.tensor(y_train, dtype=torch.long)
        self.__y_test = torch.tensor(y_test, dtype=torch.long)

        # Dataloader
        train_dataset = TensorDataset(self.__X_train, self.__y_train)
        self.__train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

        # Modèle PyTorch
        self.__model = MLP(self.__X_train.shape[1], self.__n_classes)

        # Optim & loss
        self.__criterion = nn.CrossEntropyLoss()
        self.__optimizer = optim.Adam(self.__model.parameters(), lr=0.001)

        self.__progress = ProgressBar(epochs, batch_size, len(self.__X_train))
        self.__loss_graph = LossGraph(epochs, refresh_rate=50, show_graph=False)

    def train(self):
        self.__model.train()
        batch_index = 0

        for epoch in range(self.__epochs):
            for X_batch, y_batch in self.__train_loader:
                self.__optimizer.zero_grad()
                outputs = self.__model(X_batch)
                loss = self.__criterion(outputs, y_batch)
                loss.backward()
                self.__optimizer.step()

                # ----------- CALLBACKS ----------
                self.__progress.on_batch_end()

                self.__loss_graph.on_batch_end(
                    batch=batch_index,
                    logs={"loss": loss.item()}
                )
                batch_index += 1
                # --------------------------------

        # fin d'entraînement
        self.__progress.on_train_end()
        self.__loss_graph.on_train_end()

    def test(self):
        self.__model.eval()
        with torch.no_grad():
            outputs = self.__model(self.__X_test)
            y_pred = torch.argmax(outputs, dim=1).numpy()

        accuracy = accuracy_score(self.__y_test.numpy(), y_pred)

        print(f"\n🎯 Précision globale: {accuracy:.2%}")

        # plot confusion matrix
        self._plot_confusion_matrix(self.__y_test.numpy(), y_pred)

    def _plot_confusion_matrix(self, y_true, y_pred):
        cm = confusion_matrix(y_true, y_pred)

        plt.figure(figsize=(16, 14))
        seaborn.heatmap(
            cm,
            annot=False,
            fmt="d",
            cmap="Blues",
            xticklabels=self.__label_encoder.classes_,
            yticklabels=self.__label_encoder.classes_,
            cbar_kws={"label": "Nombre de prédictions"},
            linewidths=0.5,
            linecolor="gray",
            square=True,
        )

        plt.title("Matrice de Confusion", fontsize=16, fontweight='bold', pad=20)
        plt.ylabel("Vrai Genre", fontsize=12, fontweight='bold')
        plt.xlabel("Genre Prédit", fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.yticks(rotation=0, fontsize=9)
        plt.tight_layout()

        plt.savefig(f"src/classifier/results/{self.__epochs}_confusion_matrix.png")
        print("📁 Matrice de confusion sauvegardée.")

