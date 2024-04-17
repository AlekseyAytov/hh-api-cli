from dataclasses import dataclass
from typing import NamedTuple, TypedDict, List, Literal, Dict
from enum import Enum


########################################
# MARK: типы данных для настроек

@dataclass
class AccessToken:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"


########################################
# MARK: типы данных для объекта - резюме 

class Gender(Enum):
    MALE = "мужской"
    FEMALE = "женский"

class ResumeItem(NamedTuple):
    last_name: str | None
    first_name: str | None
    middle_name: str | None
    gender: Gender | None
    age: int | None
    area: str | None
    title: str | None

ResumeCollection = List[ResumeItem]

class ApiResponse(NamedTuple):
    items: ResumeCollection
    found: int
    page: int
    pages: int
    per_page: int


if __name__ == '__main__':
    h: RequstHeaders = {"ad": 1.9}
    print(h["one"])