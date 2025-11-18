import matplotlib.pyplot as plt
import numpy as np

class LossGraph:
    def __init__(self, epochs: int, refresh_rate=50, show_graph=False):
        super().__init__()
        self.__losses = []
        self.__refresh_rate = refresh_rate
        self.__save_path = f"src/classifier/results/{epochs}_epochs_loss_graph.png"
        self.__show_graph = show_graph

        if self.__show_graph:
            plt.ion()
            self.__fig, self.__ax = plt.subplots(figsize=(8, 4))
            self.__line, = self.__ax.plot([], [], 'b-', label="Loss")
            self.__text = self.__ax.text(
                0.65, 0.9, "", transform=self.__ax.transAxes, fontsize=10, color="red"
            )
            self.__bg = self.__fig.canvas.copy_from_bbox(self.__ax.bbox)
            self.__config_graph()

    def __config_graph(self) -> None:
        self.__ax.set_xlabel("Batch")
        self.__ax.set_ylabel("Loss")
        self.__ax.set_title("Loss")
        self.__ax.grid(True)
        self.__ax.legend()
        self.__fig.canvas.draw()

    def on_batch_end(self, batch, logs=None) -> None:
        loss = logs["loss"]
        self.__losses.append(loss)

        if batch % self.__refresh_rate != 0:
            return

        if self.__show_graph:
            self.__text.set_text(f"Loss actuelle : {loss:.4f}")
            self.__line.set_data(np.arange(len(self.__losses)), self.__losses)
            self.__ax.relim()
            self.__ax.autoscale_view()

            self.__fig.canvas.restore_region(self.__bg)
            self.__ax.draw_artist(self.__line)
            self.__ax.draw_artist(self.__text)
            self.__fig.canvas.blit(self.__ax.bbox)
            self.__fig.canvas.flush_events()

    def on_train_end(self, logs=None):
        plt.ioff()
        plt.figure(figsize=(10, 5))
        plt.plot(np.arange(len(self.__losses)), self.__losses, label="Loss", color="blue")
        plt.xlabel("Batch")
        plt.ylabel("Loss")
        plt.title("Évolution de la Loss pendant l'entraînement")
        plt.grid(True)
        plt.legend()
        plt.savefig(self.__save_path)
        plt.close()

        print(f"📁 Graphe de loss sauvegardé dans : {self.__save_path}")
