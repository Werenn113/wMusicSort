import numpy
from tensorflow.keras.callbacks import Callback
from tqdm import tqdm


class ProgressBar(Callback):
    def __init__(self, epochs: int, batch_size: int, dataset_size: int) -> None:
        super().__init__()
        self.__total_batches = epochs * int(numpy.ceil(dataset_size / batch_size))
        self.__pbar = tqdm(total=self.__total_batches, desc="Entraînement", unit="batch")

    def on_batch_end(self, batch, logs=None) -> None:
        self.__pbar.update(1)

    def on_train_end(self, logs=None) -> None:
        self.__pbar.close()