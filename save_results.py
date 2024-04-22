import pandas as pd
import os
import time
import re
from read_config import Settings


class Storage:
    DEFAULT_FILE_FOLDER = "results"
    DEFAULT_FILE_NAME   = "result.xlsx"

    def __init__(self, settings: Settings) -> None:
        self.folder = settings.result_folder if settings.result_folder else self.DEFAULT_FILE_FOLDER
        self.file   = settings.result_file   if settings.result_file   else self.EFAULT_FILE_NAME
        self.final_path = os.path.join(self.folder, self.file)

        self.__add_time_mark()
        self.__check_folder()
        self.__check_file_2()

    def __add_time_mark(self) -> None:
        # timestr = time.strftime("%Y%m%d-%H%M%S")
        timestr = time.strftime("%Y%m%d")
        head, tail = os.path.splitext(self.final_path)
        self.final_path = f"{head}_{timestr}{tail}"

    def __check_folder(self) -> None:
        if not os.path.isdir(self.folder):
            os.makedirs(self.folder)

    def __check_file(self) -> None:
        if os.path.exists(self.final_path):
            head, tail = os.path.splitext(self.final_path)
            count = 1
            while os.path.exists(f"{head}({count}){tail}"):
                count += 1
            self.final_path = f"{head}({count}){tail}"

    def __check_file_2(self) -> None:
        if os.path.exists(self.final_path):
            folder, name = os.path.split(self.final_path)
            head, tail = os.path.splitext(name)
            pattern = r"\([0-9]*\)"
            max_number = 0
            for exist_file in os.listdir(self.folder):
                if exist_file.startswith(head):
                    match = re.search(pattern, exist_file)
                    if match:
                        number = int(match[0][1:-1])
                        if number > max_number:
                            max_number = number
            self.final_path = os.path.join(folder, f"{head}({max_number+1}){tail}")

    def save_to_excel(self, data) -> None:
        if len(data) > 0:
            df = pd.DataFrame.from_dict(data)
            df.to_excel(self.final_path, index=False)

    # TODO: доделать метод
    def append_to_excel(self, data) -> None:
        if len(data) > 0:
            if os.path.exists(self.final_path):
                with pd.ExcelWriter(self.final_path, mode='a') as writer:
                    df = pd.DataFrame.from_dict(data)
                    df.to_excel(writer, index=False)
            else:
                self.save_to_excel(data)


if __name__ == '__main__':

    items = [
        {'id': 1, 'name': "Ilir Meta",            'rating': 0.06},
        {'id': 2, 'name': "Abdelmadjid Tebboune", 'rating': 4.0},
        {'id': 3, 'name': "Alexander Lukashenko", 'rating': 3.1},
        {'id': 4, 'name': "Miguel Díaz-Canel",    'rating': 0.32}
    ]

    s = Settings()
    saver = Storage(s)
    saver.save_to_excel(items)
    # saver.append_to_excel(items)