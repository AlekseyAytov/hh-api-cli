import requests
from read_config import Settings
from read_filter import SearchParams
from errors import SearchRequestError
import json
from models import PageResults, Item

class SearchTyped:
    PER_PAGE = 100
    MAX_PAGE = int(2000/PER_PAGE) - 1

    __data_from_network: list[Item] = []

    def __init__(self, settings: Settings, filter: dict) -> None:
        self.settings = settings
        self.payload = filter
        self.__set_per_page()

    def get_search_results(self) -> list[Item]:
        self.__do_search()
        return self.__data_from_network
    
    def __make_request(self):
        api_url = "resumes"
        url = self.settings.base_url + api_url
        # print(self.payload)
        response = requests.request("GET", url, headers=self.settings.headers, data=self.payload)

        if response.status_code == 200:
            page_json = response.json()
            return (page_json, None)
        else:
            print(f'Ошибка: {response.status_code} - {response.reason}. {response.json()}')
            return (None, response.status_code)

    def __do_search(self) -> None:
        while True:
            page_data, error_code = self.__make_request()

            match error_code:
                case None:
                    parsed_data: PageResults = self.__parse_page_text(page_data)
                    pages_quantity = parsed_data.pages
                    page_number = parsed_data.page
                    items_found = parsed_data.found
                    # print(f"pages_quantity{pages_quantity} page_number{page_number} items_found{items_found}")
                    print(f"По данным параметрам поиска найдено всего резюме: {items_found}. Подгружено страниц: {page_number+1}")

                    self.__data_from_network.extend(parsed_data.items)

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
                
    def __parse_page_text(self, data: str) -> PageResults:
        # try:
        # return PageResults.model_validate_json(data)
        return PageResults(**data)
        # except ValidationError:
        #     raise SearchRequestError
                
    def __set_per_page(self) -> None:
        self.payload["per_page"] = self.PER_PAGE


if __name__ == '__main__':
    
    s = Settings()
    f = SearchParams(s).get_filter()
    searcher = SearchTyped(settings=s, filter=f)
    data = searcher.get_search_results()

    # для сохранения списка с объетами Item преобразуем их в json
    data = list(map(lambda x: x.model_dump(), data))
    if len(data) > 0:
        with open("debug_data/test_data_5.json", "w", encoding='utf8') as fh:
            json.dump(data, fh, ensure_ascii=False)


