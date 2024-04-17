import requests
from read_config import Settings
from read_filter import SearchParams
from errors import SearchRequestError
import json

class Search:
    all_data: list = []

    def __init__(self, settings: Settings, filter: SearchParams) -> None:
        self.settings = settings
        self.filter = filter

    def get_search_results(self):
        self.__do_search()
        return self.all_data
    
    def __make_request(self):
        api_url = "resumes"
        url = self.settings.base_url + api_url
        payload = self.filter.get_filter()
        response = requests.request("GET", url, headers=self.settings.headers, data=payload)
        if response.status_code == 200:
            page_json   = response.json()
            return (page_json, None)
        else:
            print(f'Ошибка: {response.status_code} - {response.reason}. {response.json()}')
            return (None, response.status_code)

    def __do_search(self) -> None:
        page_data, error_code = self.__make_request()

        match error_code:
            case None:
                pages_quantity = page_data["pages"]
                page_number = page_data["page"]
                # items_found = page_data["found"]
                # print(f"Всего резюме {items_found}")
                self.all_data.extend(page_data["items"])

                if page_number+1 < pages_quantity:
                    self.filter.payload["page"] += 1
                    self.do_search(self)
            case 403:
                print("Доступ не разрешен.")
            case _:
                raise SearchRequestError


if __name__ == '__main__':
    
    s = Settings()
    f = SearchParams(s)
    result = Search(settings=s, filter=f)
    data = result.get_search_results()
    print(len(data))

    with open("data_2.json", "w", encoding='utf8') as fh:
        json.dump(data, fh, ensure_ascii=False)


