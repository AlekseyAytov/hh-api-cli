from read_config import Settings
from read_filter import SearchParams
from get_search_results import Search
from authorization import Authorize
from analize_results import Analizer
from save_results import Storage
import os

def main():
    settings = Settings()
    filter = SearchParams(settings).get_filter()

    Authorize(settings=settings)

    searcher = Search(settings=settings, filter=filter)
    search_data = searcher.get_search_results()

    comment = filter.get("comment", None)
    if comment:
        comment = ", ".join(map(str, comment))

    limit = filter.get("open_limit", None)
    if limit:
        limit = int(limit[0])

    saver = Storage(settings)
    analizer = Analizer(settings=settings, storage=saver, comment=comment, open_limit=limit)
    analizer.analize(search_data)


if __name__ == '__main__':
    try:
        main()
        print("Для завершения нажите любую клавишу...")
        os.system("pause")
    except Exception  as e:
        print("Во время выполнения возникла ошибка:")
        print("#########################################")
        print(e.with_traceback)
        print("#########################################")
        print("Для завершения нажите любую клавишу...")
        os.system("pause")