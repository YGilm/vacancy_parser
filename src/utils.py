import json
from src.connector import HeadHunterAPI, SuperjobAPI


class JsonHandler:
    """Класс для работы с JSON-файлами."""

    @staticmethod
    def read_json(file_name):
        """
        Читает JSON-файл и возвращает данные.
        Args:file_name (str): Имя файла.
        Returns:dict: Данные из JSON-файла.
        """
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print("Файл не найден.")
            return {}

    @staticmethod
    def write_json(file_name, data):
        """Записывает данные в JSON-файл."""
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def clear_file(file_name):
        """Очищает содержимое файла."""
        with open(file_name, 'w', encoding='utf-8') as file:
            file.truncate(0)


class HeadHunterVacancy(HeadHunterAPI):
    """Класс для получения вакансий с HeadHunterAPI."""

    def __init__(self, keyword: str):
        super().__init__(keyword)
        self.json_handler = JsonHandler()

    @property
    def get_vacancy(self):
        """
        Получает список вакансий с HeadHunterAPI.
        Returns: list: Список вакансий с информацией о каждой вакансии.
        """
        list_vacancy = []
        for item in self.request:
            if item['snippet']['requirement'] is not None:
                s = item['snippet']['requirement']
                for x, y in [("<highlighttext>", ""), ("</highlighttext>", "")]:
                    s = s.replace(x, y)
            info = {
                'source': 'HeadHunter',
                'name': item['name'],
                'city': "(Город не указан)" if (item['address'] is None) else (
                    item['address']['city']),
                'salary': ("Зарплата не указана" if item['salary'] is None else (
                    item['salary']['from'], item['salary']['to'])),
                'requirements': "Требования не указаны" if (item['snippet']['requirement'] is None) else s,
                'url': item['alternate_url']
            }
            list_vacancy.append(info)
        return list_vacancy

    def to_json(self):
        """Очищает предыдущие записи и сохраняет список вакансий в JSON-файл 'headhunter.json'."""
        self.json_handler.clear_file('headhunter.json')
        self.json_handler.write_json('headhunter.json', self.get_vacancy)


class SuperJobVacancy(SuperjobAPI):
    """Класс для получения вакансий с SuperjobAPI."""

    @property
    def get_vacancy(self):
        """
        Получает список вакансий с SuperjobAPI.
        Returns: list: Список вакансий с информацией о каждой вакансии.
        """
        list_vacancy = []
        for item in self.request:
            if item['profession'] is not None:
                prof = item['profession']
                for x, y in [("<highlighttext>", ""), ("</highlighttext>", "")]:
                    prof = prof.replace(x, y)
            info = {
                'source': 'Superjob',
                'name': item['profession'],
                'city': "(Город не указан)" if (item['town'] is None) else (
                    item['town']['title']),
                'salary': ("Зарплата не указана" if item['payment_from'] is None else (
                    item['payment_from'], item['payment_to'])),
                'requirements': "С требованиями можете ознакомиться по ссылке" if (
                        item['candidat'] is None or isinstance(item['candidat'], str)) else (
                    item['candidat'].get('professionalSkills', ["Не указаны"])[0]),
                'url': item['link']
            }
            list_vacancy.append(info)
        return list_vacancy

    def to_json(self):
        """Очищает предыдущие записи и сохраняет список вакансий в JSON-файл 'superjob.json'."""
        data = self.get_vacancy
        JsonHandler.clear_file('superjob.json')
        JsonHandler.write_json('superjob.json', data)


class CountMixin:
    """Подсчитывает количество вакансий от указанного сервиса"""

    def __init__(self, data: str):
        """
        Инициализирует объект CountMixin.
        Args: data (str): Имя файла, содержащего данные о вакансиях.
        """
        self.data = data
        self.count = 0

    def get_count_of_vacancy(self):
        """
        Получает количество вакансий из файла.
        Returns: int: Количество вакансий.
        """
        try:
            with open(self.data, 'r') as f:
                data = json.load(f)
                self.count = len(data)
                return self.count
        except FileNotFoundError:
            print("Файл не найден")

    def add_count(self, count):
        """
        Увеличивает количество вакансий на заданное значение.
        Args: count (int): Значение, на которое увеличивается количество вакансий.
        """
        self.count += count


class Vacancy:
    """Класс для представления информации о вакансии."""

    __slots__ = ('source', 'name', 'url', 'city', 'requirements', 'currency', 'salary_from', 'salary_to')

    def __init__(self, source, name, url, city, requirements, currency, salary_from, salary_to):
        """
        Инициализация объекта Vacancy.
        Args:
            source (str): Источник вакансии (HeadHunter или Superjob).
            name (str): Название вакансии.
            url (str): Ссылка на вакансию.
            city (str): Город, в котором находится вакансия.
            requirements (str): Требования к кандидату.
            currency (str): Валюта зарплаты.
            salary_from (int): Нижняя граница зарплаты.
            salary_to (int): Верхняя граница зарплаты.
        """
        self.source = source
        self.name = name
        self.url = url
        self.city = city
        self.requirements = requirements
        self.currency = currency
        self.salary_from = salary_from
        self.salary_to = salary_to

    def __str__(self):
        """Возвращает строковое представление объекта Vacancy."""

        return f"Источник: {self.source}\n" \
               f"Название: {self.name}\n" \
               f"Ссылка: {self.url}\n" \
               f"Город: {self.city}\n" \
               f"Требования: {self.requirements}\n" \
               f"Валюта: {self.currency}\n" \
               f"Зарплата: {self.salary_from}-{self.salary_to}"


class VacancyList:
    """Класс для работы со списком вакансий."""

    def __init__(self, file_name):
        """
        Инициализация объекта VacancyList.
        Args: file_name (str): Имя файла, содержащего список вакансий.
        """
        self.file_name = file_name
        self.vacancies = self.get_vacancy()

    def get_vacancy(self):
        """
        Получение списка вакансий из файла.
        Returns: list: Список вакансий.
        """
        with open(self.file_name, 'r', encoding='utf-8') as file:
            vacancies = json.load(file)
        return vacancies

    def write_vacancies(self, vacancies):
        """
        Записывает список вакансий в файл.
        Args: vacancies (list): Список вакансий.
        """
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    def filter_vacancies(self, city=None, salary_from=None, salary_to=None):
        """
        Фильтрует список вакансий по городу и зарплате.
        Args:
            city (str): Город для фильтрации.
            salary_from (int): Нижняя граница зарплаты для фильтрации.
            salary_to (int): Верхняя граница зарплаты для фильтрации.
        Returns: list: Отфильтрованный список вакансий.
        """
        filtered_vacancies = []
        for vacancy in self.vacancies:
            # Применить фильтры города и зарплаты к вакансиям
            if city and vacancy.get('city') != city:
                continue
            # Фильтровать по нижней границе зарплаты
            if salary_from and vacancy.get('salary'):
                if isinstance(vacancy['salary'], list):
                    if vacancy['salary'][0] is not None and int(vacancy['salary'][0]) < int(salary_from):
                        continue
                elif isinstance(vacancy['salary'], dict):
                    if vacancy['salary']['from'] is not None and int(vacancy['salary']['from']) < int(salary_from):
                        continue
            # Фильтровать по верхней границе зарплаты
            if salary_to and vacancy.get('salary'):
                if isinstance(vacancy['salary'], list):
                    if vacancy['salary'][-1] is not None and int(vacancy['salary'][-1]) > int(salary_to):
                        continue
                elif isinstance(vacancy['salary'], dict):
                    if vacancy['salary']['to'] is not None and int(vacancy['salary']['to']) > int(salary_to):
                        continue
            filtered_vacancies.append(vacancy)

        if not filtered_vacancies:
            print("По заданным параметрам фильтрации не найдено вакансий.")

        return filtered_vacancies

    @staticmethod
    def search_vacancies(keyword, resource=None, count_vacancy=None):
        """
        Поиск вакансий по ключевому слову и источнику.
        Args:
            keyword (str): Ключевое слово для поиска вакансий.
            resource (str): Источник вакансий для поиска ("HeadHunter", "Superjob" или "all").
            count_vacancy (CountMixin): Объект CountMixin для подсчета количества вакансий.
        Returns: list: Список вакансий, соответствующих поисковому запросу.
        """
        vacancies = []

        if resource == "HeadHunter" or resource == "all":
            hh_vacancy = HeadHunterVacancy(keyword)
            hh_vacancy.get_request()
            hh_vacancy.to_json()
            hh_vacancy_list = VacancyList('headhunter.json')
            hh_vacancies = hh_vacancy_list.get_vacancy()
            vacancies.extend(hh_vacancies)
            if count_vacancy:
                count_vacancy.add_count(len(hh_vacancies))

        if resource == "Superjob" or resource == "all":
            sj_vacancy = SuperJobVacancy(keyword)
            sj_vacancy.get_request()
            sj_vacancy.to_json()
            sj_vacancy_list = VacancyList('superjob.json')
            sj_vacancies = sj_vacancy_list.get_vacancy()
            vacancies.extend(sj_vacancies)
            if count_vacancy:
                count_vacancy.add_count(len(sj_vacancies))

        return vacancies
