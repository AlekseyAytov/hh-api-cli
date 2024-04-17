import json
import time
import requests
from read_config import Settings
from read_filter import SearchParams


class Analizer:

    __all_data: list[dict] = []

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_data(self):
        return self.__all_data

    # resume_url - url для запроса
    def get_resume(self, resume_url):
        response = requests.request("GET", resume_url, headers=self.settings.header)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def analize(self, items) -> None:
        for item in items:
            self.all_data.append({"hh_id": item["id"]})

    # распарсить номер мобльного
    def __parse_phone_number(contacts) -> str:
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

        self.__all_data.append({
            "Date":  timestr,
            "ID":    resume_id,
            "Phone": cell_phone,
            "Name":  name,
            "Area":  area,
            "Age":   age,
            "Title": wish_title,
        })


if __name__ == '__main__':
    with open("data_2.json", "r") as fh:
        data = json.load(fh)

    s = Settings()
    analizer = Analizer(settings=s)
    analizer.analize(data)
    print(analizer.get_data())

    # print(f'Поисковая выдача составляет: {len(data)}')

    # for item in data:
    #     # если контакты доступны к просмотру
    #     if item["can_view_full_info"]:
    #         # получить резюме по url
    #         response = get_resume_info(item["url"])
    #     else:
    #         if input(f'Открыть контакты резюме? {item["title"]}, возраст {item["age"]} (да-Enter)') == '':
    #             response = get_resume_info(item["actions"]["get_with_contact"]["url"])
    #     if response.status_code == 200:
    #         resume = response.json()
    #         data_dict = get_info_from_resume(resume)
    #         write_to_csv(data_dict)
    #         print(f'{data_dict["ID"]}: {data_dict["Name"]}, {data_dict["Area"]}, {data_dict["Age"]}, {data_dict["Title"]}, {data_dict["Phone"]}')
    #     else:
    #         print(f'Ошибка: {response.status_code} - {response.text}')


