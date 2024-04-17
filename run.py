from read_config import Settings
from read_filter import SearchParams
from get_search_results import Search
from authorization import Authorize

def main():
    settings = Settings()
    search_params = SearchParams(settings)
    Authorize(search_params)
    result = Search(settings=settings, filter=search_params)


if __name__ == '__main__':
    main()