from pydantic import BaseModel, Field
from typing import Literal


class Area(BaseModel):
    id  : str
    name: str
    # url: str

#---------------------------------------
class Gender(BaseModel):
    id  : Literal["male"   , "female"]
    name: Literal["Мужской", "Женский", "Male", "Female"]

#---------------------------------------
class Counters(BaseModel):
    total: int # Общее количество комментариев


class Comments(BaseModel):
    url     : str # URL, на который нужно сделать GET-запрос, чтобы получить список комментариев
    counters: Counters

# Информация о владельце резюме
class Owner(BaseModel):
    id      : str # Идентификатор владельца резюме
    comments: Comments

#---------------------------------------
class GetWithContact(BaseModel):
    url: str # Ссылка на получение элементов

class Actions(BaseModel):
    get_with_contact: GetWithContact | None = None

#---------------------------------------
class Phone(BaseModel):
    city     : str
    country  : str
    formatted: str
    number   : str

class Type(BaseModel):
    id   : Literal["home"            , "work"           , "cell"             , "email"]
    # name: Literal["Домашний телефон", "Рабочий телефон", "Мобильный телефон", "Эл. почта"]
    name : str

class Contact(BaseModel):
    contact_type: Type = Field(alias="type")
    value       : str | Phone
    verified    : bool | None = None

#---------------------------------------
# XXX: Main app Model
class Item(BaseModel):
    id                : str
    title             : str
    first_name        : str | None
    last_name         : str | None
    middle_name       : str | None
    age               : int | None
    gender            : Gender | None
    area              : Area | None
    can_view_full_info: bool | None
    alternate_url     : str  | None
    owner             : Owner # Информация о владельце резюме
    actions           : Actions
    contact           : list[Contact] | None = None

#---------------------------------------
# XXX: Main network Model
class PageResults(BaseModel):
    found   : int
    page    : int
    pages   : int
    per_page: int
    items   : list[Item]


if __name__ == '__main__':
    print("Hello!")