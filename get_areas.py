import requests
from read_config import Settings

def get_areas(settings: Settings):
    api_url = "areas"
    url = settings.base_url + api_url
    print(f"Делаю запрос для получения информации о регионах: {url}")
    response = requests.request("GET", url, headers=settings.headers)
    if response.status_code == 200:
        page_json   = response.json()
        return (page_json, None)
    else:
        print(f'Ошибка: {response.status_code} - {response.reason}. {response.json()}')
        return (None, response.status_code)
        
if __name__ == '__main__':
    s = Settings()
    res, err = get_areas(s)
    if err == None:
        for country in res:
            if country["name"] == "Россия":
                regions = country["areas"]
                for area in regions:
                    print(area["name"], ":", area["id"])