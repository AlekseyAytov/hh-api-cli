from configparser import ConfigParser
import os


class Settings:
    SETTINGS_FOLDER = "settings"
    SETTINGS_FILE   = "settings.ini"
    setting_file_path = os.path.join(SETTINGS_FOLDER, SETTINGS_FILE)

    def __init__(self) -> None:
        self.__parse_config()
        print("Настройки загружены.")

    def __parse_config(self) -> None:
        config = ConfigParser()
        config.read(self.setting_file_path)

        self.base_url      = config.get("main",   "base_url",      fallback=None)
        self.user_agent    = config.get("main",   "user_agent",    fallback=None)
        self.filter_file   = config.get("main",   "filter",        fallback=None)
        self.client_id     = config.get("codes",  "client_id",     fallback=None)
        self.client_secret = config.get("codes",  "client_secret", fallback=None)
        self.access_token  = config.get("codes",  "access_token",  fallback=None)
        self.result_folder = config.get("result", "folder",        fallback=None)
        self.result_file   = config.get("result", "file_name",     fallback=None)

    def save(self) -> None:
        config = ConfigParser()
        config.read(self.setting_file_path)

        config.set("main",  "base_url",      self.base_url)
        config.set("main",  "user_agent",    self.user_agent)
        config.set("main",  "filter",        self.filter_file)
        config.set("codes", "client_id",     self.client_id)
        config.set("codes", "client_secret", self.client_secret)
        config.set("codes", "access_token",  self.access_token)
        config.set("result", "folder",       self.result_folder)
        config.set("result", "file_name",    self.result_file)

        with open(self.setting_file_path, 'w') as configfile:
            config.write(configfile)

    @property
    def headers(self) -> dict:
        return {
            "User-Agent": self.user_agent,
            "Authorization": "Bearer " + self.access_token
        }
    
    def __app_directory(self) -> str:
        home: str
        directory: str

        match os.name:
            case "posix":
                # if unix os
                home = os.getenv("HOME")
                directory = ".hhapp"
            case "nt":
                # if windows os
                home = os.getenv('LOCALAPPDATA')
                directory = "Hhapp"

        return os.path.join(home, directory)
    
    def __load_token(self) -> None:
        app_dir = self.__app_directory()

            
        token_dir = os.path.join(home, app_dir)

    
    # def update_params(self, section, parameter, value):
    #     config = ConfigParser()
    #     config.read(self.seting_file_path)
    #     config.set(section, parameter, value)
    #     with open(self.seting_file_path, 'w') as configfile:
    #         config.write(configfile)
    


if __name__ == '__main__':
    settings = Settings()
    print(settings.base_url)
    print(settings.client_id)
    print(settings.user_agent)
    print(settings.headers)


    home: str
    directory: str
    
    match os.name:
        case "posix":
            home = os.getenv("HOME")
            directory = ".hhapp"
        case "nt":
            home = os.getenv('LOCALAPPDATA')
            directory = "Hhapp"
            print("windows")
    
    token_dir = os.path.join(home, directory)

    print(token_dir)
