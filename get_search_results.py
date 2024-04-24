import requests
from read_config import Settings
from read_filter import SearchParams
from errors import SearchRequestError
import json

class Search:
    PER_PAGE = 100
    MAX_PAGE = int(2000/PER_PAGE) - 1

    all_data: list = []

    def __init__(self, settings: Settings, filter: dict) -> None:
        self.settings = settings
        self.payload = filter
        self.__set_per_page()

    def get_search_results(self):
        self.__do_search()
        return self.all_data
    
    def __make_request(self):
        api_url = "resumes"
        url = self.settings.base_url + api_url
        # print(self.payload)

        response = requests.request("GET", url, headers=self.settings.headers, data=self.payload)

        if response.status_code == 200:
            page_json   = response.json()
            return (page_json, None)
        else:
            print(f'Ошибка: {response.status_code} - {response.reason}. {response.json()}')
            return (None, response.status_code)

    def __do_search(self) -> None:
        while True:
            page_data, error_code = self.__make_request()

            match error_code:
                case None:
                    pages_quantity = page_data["pages"]
                    page_number = page_data["page"]
                    items_found = page_data["found"]
                    # print(f"pages_quantity{pages_quantity} page_number{page_number} items_found{items_found}")
                    print(f"По данным параметрам поиска найдено всего резюме: {items_found}. Подгружено страниц: {page_number+1}")

                    self.all_data.extend(page_data["items"])

                    match page_number:
                        case self.MAX_PAGE:
                            print("Достигнут лимит одновременного просмотра в 2000 резюме.")
                            break
                        case x if x < pages_quantity-1:
                            self.payload["page"] = page_number+1
                        case _:
                            break
                case 400:
                    print("Ошибка в фильтре запроса.")
                    break
                case 403:
                    print("Доступ не разрешен.")
                    break
                case _:
                    raise SearchRequestError
                
    def __set_per_page(self) -> None:
        self.payload["per_page"] = self.PER_PAGE


if __name__ == '__main__':
    
    s = Settings()
    f = SearchParams(s).get_filter()
    searcher = Search(settings=s, filter=f)
    data = searcher.get_search_results()
    if len(data) > 0:
        with open("test_data_2.json", "w", encoding='utf8') as fh:
            json.dump(data, fh, ensure_ascii=False)


