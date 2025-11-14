import pandas
from pandas.core.interchange.dataframe_protocol import DataFrame


class DataLoader:
    def __init__(self, dataset_path: str) -> None:
        self.__dataset_path = dataset_path
        self.__datas = pandas.read_csv(self.__dataset_path)

        features = self.__get_features_names()
        self.__X = self.__datas[features]
        self.__y = self.__datas["track_genre"]

    @property
    def datas(self) -> DataFrame:
        return self.__datas

    @property
    def X(self) -> DataFrame:
        return self.__X

    @property
    def y(self) -> DataFrame:
        return self.__y

    def __get_features_names(self) -> list[str]:
        return self.__datas.columns.values[5:-1] # la popularité est prise en compte
