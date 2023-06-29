from abc import ABC, abstractmethod
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Connector(ABC):
    """Абстрактный базовый класс для коннекторов."""
    @abstractmethod
    def get_request(self):
        """Абстрактный метод для выполнения запроса."""
        pass

    @staticmethod
    def get_connector(file_name):
        """Статический метод, возвращающий имя файла коннектора."""
        return file_name


class HeadHunterAPI(Connector):
    """Класс для взаимодействия с API HeadHunter."""

    def __init__(self, keyword: str):
        """
        Инициализация объекта HeadHunterAPI.
        Args: keyword (str): Ключевое слово для поиска вакансий.
        """
        self.keyword = keyword
        self.request = self.get_request()

    def get_request(self):
        """
        Получение результатов запроса к API HeadHunter.
        Returns: list: Список вакансий, полученных в результате запроса.
        """
        vacancies = []
        for page in range(1, 11):
            params = {
                "text": f"{self.keyword}",
                "area": 113,
                "page": page,
                "per_page=100": 100
            }
            vacancies.extend(requests.get('https://api.hh.ru/vacancies', params=params).json()["items"])
        return vacancies


class SuperjobAPI(Connector):
    """Класс для взаимодействия с API Superjob."""

    def __init__(self, keyword: str):
        """
        Инициализация объекта SuperjobAPI.
        Args: keyword (str): Ключевое слово для поиска вакансий.
        """
        self.keyword = keyword
        self.request = self.get_request()

    def get_request(self):
        """
        Получение результатов запроса к API Superjob.
        Returns: list: Список вакансий, полученных в результате запроса.
        """
        url = "https://api.superjob.ru/2.0/vacancies/"
        params = {'keyword': self.keyword, "count": 100}
        authorization = {"X-Api-App-Id": os.environ['SJ_KEY']}
        response = requests.get(url, headers=authorization, params=params)
        vacancies = response.json()['objects']
        return vacancies
