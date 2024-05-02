import json
import time
import requests
from read_config import Settings
from typing import NamedTuple
from errors import OpenResumeError
from save_results import Storage
from models import Item, Contact

class ItemsCounter(NamedTuple):
    amount  : int
    opened  : int
    closed  : int
    can_open: int
class AnalizerTyped:

    __parsed_data: list[dict] = []
    # __raw_data:    list[dict] = []

    def __init__(self, settings: Settings, storage: Storage, comment: str = None, open_limit: int = None) -> None:
        self.settings = settings
        self.storage = storage
        self.comment = comment
        self.open_limit = open_limit
    
    def analize(self, from_data):
        self.__analize(from_data)
        
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
                # self.__raw_data.append(page_data)
                self.__parse_resume(page_data)
            case 403:
                print("Требуется авторизация пользователя")
                # raise OpenResumeError
            case 404:
                print("Резюме не существует или недоступно для текущего пользователя")
            case 429:
                print("Для работодателя превышен лимит просмотров резюме в сутки")
                # raise OpenResumeError
            case _:
                raise OpenResumeError
    
    def __analize(self, items: list[Item]) -> list[dict]:
        counter: ItemsCounter = self.__make_items_counter(items)
        print(f"Результаты поиска: загружено {counter.amount} из них {counter.opened} открыто, {counter.closed} закрыто для просмотра контактов.")
        print(f"Возможны к открытию: {counter.can_open} резюме.")

        interruption_flag = False
        continue_flag = False
        open_counter = 0
        for count, item in enumerate(items):
            if interruption_flag:
                print("Прерывание...")
                break

            if  self.open_limit and open_counter >=  self.open_limit:
                print(f"Достигнут лимит открытий резюме - {self.open_limit}.")
                break
            
            if item.actions.get_with_contact:
                while True:
                    if not continue_flag:
                        question = input(f'Открыть контакты резюме-{count+1}: {item.title}, возраст {item.age}, регион {item.area.name}? (y-yes/n-no/s-stop/all-open all): ')
                    else:
                        print(f"{count+1}")
                        question = "y"

                    match question:
                        case "y":
                            print("Открываем...")
                            try:
                                open_counter += 1
                                self.__open_resume(item.actions.get_with_contact.url)
                            except Exception as err:
                                self.storage.save_to_excel(self.__parsed_data)
                                raise err
                            break
                        case "n":
                            print("Пропускаем...")
                            break
                        case "s":
                            interruption_flag = True
                            break
                        case "all":
                            continue_flag = True
                        case _:
                            print("Некорректный ввод...")
        
        self.storage.save_to_excel(self.__parsed_data)
        # self.__save_raw_data()
    
    def __make_items_counter(self, items: list[Item]) -> ItemsCounter:
        opened = 0
        closed = 0
        can_open = 0
        for item in items:
            if item.can_view_full_info:
                opened += 1
            else:
                closed += 1
            
            if item.actions.get_with_contact:
                can_open += 1

        return ItemsCounter(amount=len(items), opened=opened, closed=closed, can_open=can_open)

    # распарсить номер мобльного
    def __parse_phone_number(self, contacts: list[Contact]) -> str:
        for i in contacts:
            if i.contact_type.id == "cell":
                country_code = i.value.country
                city_code    = i.value.city
                number       = i.value.number
                return country_code + city_code + number
        
    # распарсить каждое резюме
    def __parse_resume(self, resume_json):
        resume_object: Item = Item(**resume_json)

        last_name   = resume_object.last_name   if resume_object.last_name   else "н/д"
        first_name  = resume_object.first_name  if resume_object.first_name  else "н/д"
        middle_name = resume_object.middle_name if resume_object.middle_name else "н/д"
        name = last_name + ' ' + first_name + ' ' + middle_name

        area = resume_object.area.name if  resume_object.area else "н/д"
        age = resume_object.age if resume_object.age else "н/д"
        wish_title = resume_object.title if resume_object.title else "н/д"

        cell_phone = self.__parse_phone_number(resume_object.contact)
        timestr = time.strftime('%d.%m.%Y')

        self.__parsed_data.append({
            "Date"   : timestr,
            "ID"     : resume_object.id,
            "Phone"  : cell_phone,
            "Name"   : name,
            "Area"   : area,
            "Age"    : age,
            "Title"  : wish_title,
            "url"    : resume_object.alternate_url,
            "comment": self.comment,
        })

    def __save_raw_data(self):
        if len(self.__raw_data) > 0:
            with open("raw_data_of_last_analize.json", "w", encoding='utf8') as fh:
                json.dump(self.__raw_data, fh, ensure_ascii=False)


if __name__ == '__main__':
    # Для тестирования класса AnalizerTyped забрать json из файла
    with open("debug_data/test_data_2.json", "r", encoding='utf8') as fh:
        data = json.load(fh)
    # и преобразовать его в список из объектов Item
    network_data: list[Item] = list(map(lambda x: Item(**x), data))

    s = Settings()
    storage = Storage(settings=s)
    comment = ", ".join(["one", "1", "two"])
    analizer = AnalizerTyped(settings=s, storage=storage, comment=comment, open_limit=2)
    analizer = analizer.analize(network_data)