import requests
from read_config import Settings
from errors import *
import webbrowser


class Authorize:

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.checkToken()
        print("Авторизация закончена.")
        

    def __isTokenExist(self) -> bool:
        self.token = self.settings.access_token
        return True if self.token != None else False
    
    def get_user_info(self) -> tuple[str, int]:
        api_url = "me"
        url = self.settings.base_url + api_url
        print(f"Делаю запрос для получения информации о пользователе: {url}")

        response = requests.request("GET", url, headers=self.settings.headers)
        if response.status_code == 200:
            page_json   = response.json()
            last_name   = page_json.get("last_name")   or ""
            first_name  = page_json.get("first_name")  or ""
            middle_name = page_json.get("middle_name") or ""
            userName    =  f"{last_name} {first_name} {middle_name}"
            return (userName, None)
        else:
            # print(f'Ошибка: {response.status_code} - {response.reason}. {response.json()}')
            return (None, response.status_code)

    def __getAccessToken(self) -> tuple[str, int]:
        api_url = "https://hh.ru/oauth/token"
        authCode = self.__getAuthCode()

        params = {
            "client_id": self.settings.client_id,
            "client_secret": self.settings.client_secret,
            "code": authCode,
            "grant_type": "authorization_code"
        }

        response = requests.request("POST", api_url, params=params)
        if response.status_code == 200:
            page_json = response.json()
            token = page_json["access_token"]
            return (token, None)
        else:
            print(f'Ошибка: {response.status_code} - {response.reason}. {response.json()}')
            return (None, response.status_code)
        
    def __getAuthCode(self) -> str:
        auth_url = f"https://hh.ru/oauth/authorize?response_type=code&client_id={self.settings.client_id}"
        # webbrowser.open_new_tab(auth_url)

        print("Для процесса авторизации перейдите по ссылке (возможно скопировать в адресную строку браузера):")
        print("")
        print(auth_url)
        print("")
        print("После авторизации на ресурсе hh.ru и перенаправления на сайт akbars.ru из адресной строки браузера")
        print("скопируйте буквенно-цифровой код после знака '=' в поле ниже и нажмите Enter.")
        authCode = input("-> ")
        return authCode
    
    def saveToken(self, token):
        self.settings.access_token = token
        self.settings.save()

    def checkToken(self):
        if self.__isTokenExist():
            print("Токен есть.")
            name, error_code = self.get_user_info()

            match error_code:
                case None:
                    print(f"Вы вошли в программу как: {name}.")
                case 403:
                    print("Токен не валидный, нужно получить новый.")
                    self.settings.access_token = None
                    self.checkToken()
                case _:
                    raise AuthenticationError
        else:
            print("Токена нет, нужно его получить")
            token, error_code = self.__getAccessToken()

            match error_code:
                case None:
                    self.saveToken(token)
                    print("Токен получен.")
                    self.checkToken()
                case 400:
                    print("Использован старый код, нужно использовать новый.")
                    self.checkToken()
                case _:
                    raise AuthenticationError



if __name__ == '__main__':
    s = Settings()
    auth = Authorize(s)