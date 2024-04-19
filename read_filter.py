import pandas as pd
import numpy as np
import os
from read_config import Settings


class SearchParams:
    __params: dict = {}

    def __init__(self, settings: Settings) -> None:
        self.__settings = settings
        self.__filter_file = os.path.join(self.__settings.SETTINGS_FOLDER, self.__settings.filter_file)

    def get_filter(self) -> dict:
        self.__loadFilters()
        self.__adjust_filter()
        self.__substitution_area()
        print("Параметры для поиска загружены.")
        return self.__params

    def __loadAreaCodes(self) -> dict:
        df = pd.read_excel(self.__filter_file, sheet_name=1, dtype={1: np.int64})
        return dict(zip(df[df.columns[0]], df[df.columns[1]]))
    
    def __loadFilters(self) -> None:
        df = pd.read_excel(self.__filter_file, usecols=[0, 2], na_values=" ", dtype=str)
        df = df.dropna()
        keys = df.columns[0]
        values = df.columns[1]
        self.__params =  dict(zip(df[keys], df[values]))

    def __adjust_filter(self) -> None:
        for key, value in self.__params.items():
            self.__params[key] = list(map(lambda x: x.strip(), value.split(",")))

    def __substitution_area(self) -> None:
        areas = self.__params.get("area")
        if areas:
            area_codes = self.__loadAreaCodes()
            self.__params["area"] = list(map(lambda x: area_codes[x], areas))
            

if __name__ == '__main__':

    payload = {
        "text": "визовый центр",
        "area": [
            3,
        ],
        "job_search_status": [
            "active_search",
            # "looking_for_offers"
        ],
        # "age_from": 20,
        # "age_to": 50,
        "employment": [
            "full",
            "part"
        ],
        "schedule": [
            "fullDay",
            "shift",
            "flexible",
            "remote"
        ],
        # "professional_role": [
        #     83
        # ],
        # "salary_to": 50000,
        "citizenship": 113,
        # "period": 3,
        "with_job_search_status": "true", # Параметр для просмотра в резюме статуса поиска кандидата
        "label": [
            "only_with_age", # нужен для того, чтобы искать только с указанием возраста
            "exclude_viewed_by_employer_id", # Скрыть резюме, просмотренные всей компанией
            # "exclude_viewed_by_user_id" # Скрыть резюме, просмотренные мной
         ],
        "search_in_responses": True,
        "page": 0,
        "per_page": 10,
    }
    
    s = Settings()
    params = SearchParams(s)
    print(params.get_filter())