import json
import time
import requests
from read_config import Settings
from read_filter import SearchParams
from typing import NamedTuple
from errors import OpenResumeError

class ItemsCounter(NamedTuple):
    opened:   int
    closed:   int
    can_open: int


class Analizer:

    __parsed_data: list[dict] = []
    __raw_data:    list[dict] = []

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_data(self, from_data):
        self.__analize(from_data)
        return self.__parsed_data
        
    def __make_request(self, resume_url):
        response = requests.request("GET", resume_url, headers=self.settings.headers)

        if response.status_code == 200:
            page_json   = response.json()
            return (page_json, None)
        else:
            print(f'Ошибка: {response.status_code} - {response.reason}. {response.json()}')
            return (None, response.status_code)
        
    def __open_resume(self, url):
        page_data, error_code = self.__make_request(url)
        match error_code:
            case None:
                print("Резюме открыто.")
                self.__raw_data.append(page_data)
                self.__parse_resume(page_data)
            case 403:
                print("Требуется авторизация пользователя")
            case 404:
                print("Резюме не существует или недоступно для текущего пользователя")
            case 429:
                print("Для работодателя превышен лимит просмотров резюме в сутки")
            case _:
                raise OpenResumeError
    
    def __analize(self, items) -> list[dict]:
        counter = self.__items_count(items)
        print(f"Результаты поиска: загружено {len(items)} из них {counter.opened} открыто, {counter.closed} закрыто для просмотра контактов.")
        print(f"Возможны к открытию: {counter.can_open} резюме.")
        for item in items:
            open_url = item["actions"]["get_with_contact"]["url"] if item.get("actions", False) and item["actions"].get("get_with_contact", False) else None
            if open_url:
                title = item.get("title", "")
                age = item.get("age", "")
                area = item["area"]["name"] if item.get("area", False) else ""

                while True:
                    question = input(f'Открыть контакты резюме: {title}, возраст {age}, регион {area}? (y/n)')
                    if question == 'y':
                        print("Открываем...")
                        self.__open_resume(open_url)
                        break
                    elif question == "n":
                        print("Пропускаем...")
                        break
                    else:
                        print("Некорректный ввод...")

        self.__save_raw_data()
    
    def __items_count(self, items) -> ItemsCounter:
        opened = 0
        closed = 0
        can_open = 0
        for item in items:
            if item.get("can_view_full_info", False):
                opened += 1
            else:
                closed += 1
            
            if item.get("actions", False) and item["actions"].get("get_with_contact", False):
                can_open += 1

        return ItemsCounter(opened=opened, closed=closed, can_open=can_open)


    # распарсить номер мобльного
    def __parse_phone_number(self, contacts) -> str:
        for i in contacts:
            if i["type"]["id"] == "cell":
                country_code = i["value"]["country"]
                city_code = i["value"]["city"]
                number = i["value"]["number"]
                return country_code + city_code + number
        
    # распарсить каждое резюме
    def __parse_resume(self, resume):
        resume_id = resume["id"]

        last_name   = resume["last_name"]   if resume["last_name"]   else "н/д"
        first_name  = resume["first_name"]  if resume["first_name"]  else "н/д"
        middle_name = resume["middle_name"] if resume["middle_name"] else "н/д"
        name = last_name + ' ' + first_name + ' ' + middle_name

        area = resume["area"]["name"] if resume["area"] else "н/д"
        age = resume["age"] if resume["age"] else "н/д"
        wish_title = resume["title"] if resume["title"] else "н/д"

        cell_phone = self.__parse_phone_number(resume["contact"])
        timestr = time.strftime('%d.%m.%Y')

        link = resume["alternate_url"]

        self.__parsed_data.append({
            "Date":  timestr,
            "ID":    resume_id,
            "Phone": cell_phone,
            "Name":  name,
            "Area":  area,
            "Age":   age,
            "Title": wish_title,
            "url":   link,
        })

    def __save_raw_data(self):
        if len(self.__raw_data) > 0:
            with open("raw_data_of_last_analize.json", "w", encoding='utf8') as fh:
                json.dump(data, fh, ensure_ascii=False)



if __name__ == '__main__':
    with open("test_data_2.json", "r") as fh:
        data = json.load(fh)

    s = Settings()
    analizer = Analizer(settings=s)
    data = analizer.get_data(data)

    if len(data) > 0:
        with open("test_data_resume.json", "w", encoding='utf8') as fh:
            json.dump(data, fh, ensure_ascii=False)


