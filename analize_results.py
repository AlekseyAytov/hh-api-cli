import json
import csv
import os
from datetime import datetime
import requests
import pandas as pd
from read_config import Settings
from read_filter import SearchParams


class Analizer:

    def __init__(self, settings: Settings, filter: SearchParams) -> None:
        self.settings = settings
        self.filter = filter
        self.all_data = []


    # resume_url - url для запроса
    def get_resume_info(self, resume_url):

        response = requests.request("GET", resume_url, headers=self.settings.header)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def analize(self, items) -> None:
        for item in items:
            self.all_data.append({"hh_id": item["id"]})

    # # contacts - array of dicts with contacts information
    # def get_phone_number(contacts):
    #     for i in contacts:
    #         if i["type"]["id"] == "cell":
    #             country_code = i["value"]["country"]
    #             city_code = i["value"]["city"]
    #             number = i["value"]["number"]
    #             return country_code + city_code + number
        

    def get_info_from_resume(resume):
        resume_id = resume["id"]

        last_name = resume["last_name"] if resume["last_name"] else "н/д"
        first_name = resume["first_name"] if resume["first_name"] else "н/д"
        middle_name = resume["middle_name"] if resume["middle_name"] else "н/д"
        name = last_name + ' ' + first_name + ' ' + middle_name

        area = resume["area"]["name"] if resume["area"]["name"] else "н/д"
        age = resume["age"] if resume["age"] else "н/д"
        title = resume["title"] if resume["title"] else "н/д"

        cell_phone = get_phone_number(resume["contact"])
        # return f'{resume_id}: {name}, {area}, {age}, {title}, {cell_phone}'
        return {
            "ID": resume_id,
            "Phone": cell_phone,
            "Name": name,
            "Area": area,
            "Age": age,
            "Source": source,
            "Title": title
        }


csv_file_path = ''
csv_file_name = "search_data.csv"
abs_csv_file_name = os.path.join(csv_file_path, csv_file_name)

# "data" must be a dictionary with keys in headers_list
def write_to_csv(data):
    headers_list = ['ID', 'Phone', 'Name', 'Area', 'Age', 'Source', 'Date', 'Title']
    is_file_exist = os.path.exists(abs_csv_file_name)
    with open(abs_csv_file_name, 'a') as file:
        csv_writer = csv.DictWriter(file, fieldnames=headers_list, delimiter=';', restval='NoData', extrasaction='ignore',escapechar='')
        # если файл создан впервые, добавить header
        if not is_file_exist:
            csv_writer.writeheader()
        # get timestamp for csv file
        # data['Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['Date'] = datetime.now().strftime('%d.%m.%Y')
        csv_writer.writerow(data)


if __name__ == '__main__':
    with open("data_2.json", "r") as fh:
        data = json.load(fh)

    s = Settings()
    sf = SearchParams(s)
    analizer = Analizer(settings=s, filter=sf)
    analizer.analize(data)
    print(analizer.all_data)

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


