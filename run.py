from read_config import Settings
from read_filter import SearchParams
from get_search_results import Search
from authorization import Authorize
from analize_results import Analizer
from save_results import Storage

def main():
    settings = Settings()
    search_params = SearchParams(settings)

    Authorize(settings=settings)

    searcher = Search(settings=settings, filter=search_params)
    search_data = searcher.get_search_results()

    saver = Storage(settings)
    analizer = Analizer(settings=settings, storage=saver)
    analizer.analize(search_data)


if __name__ == '__main__':
    main()