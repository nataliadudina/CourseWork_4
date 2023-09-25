from abc import ABC, abstractmethod
import requests

from config import API_TOKEN
from vacancy import Vacancy


class APIManager(ABC):
    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def get_vacancies(self, query: str) -> list[Vacancy]:
        """Получения вакансий по ключевому запросу"""

    @abstractmethod
    def _create_vacancy(self, data: dict) -> Vacancy:
        """Создаёт экземпляры класса Vacancy"""


class HeadHunterAPI(APIManager):

    def __init__(self, base_url='https://api.hh.ru/'):
        super().__init__(base_url)

    def get_vacancies(self, query: str) -> list[Vacancy]:
        url = f'{self.base_url}vacancies'
        param = {'text': query}

        # Проверка на возможные ошибки при отправлении запроса
        try:
            response = requests.get(url, param)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f'Запрос невозможен: {str(e)}')

        return [self._create_vacancy(item) for item in response.json().get('items', [])]

    def _create_vacancy(self, data: dict) -> Vacancy:
        url = data.get('alternate_url')
        name = data.get('name')

        # Детали по зарплате
        salary_data = data.get('salary')
        if salary_data:
            salary_from = salary_data.get('from') if salary_data.get('from') is not None else 0
            salary_to = salary_data.get('to') if salary_data.get('to') is not None else 0
            salary_currency = salary_data.get('currency')

            # Нахождение числового значения зарплаты для возможности сравнения вакансий по зарплате
            if salary_from != 0:
                salary = salary_from
            elif salary_to != 0:
                salary = salary_to
            else:
                salary = 0

            # Полная информация по зарплате, собранная в строку для отображения
            salary_str = f'{salary_from}-{salary_to} {salary_currency}' if salary_from is not None else 'Зарплата не указана'

        else:
            salary_str = 'Зарплата не указана'
            salary = 0

        requirements = data['snippet'].get('requirement')
        return Vacancy(url=url, name=name, salary_str=salary_str, salary=salary, requirements=requirements)


class SuperJobAPI(APIManager):

    def __init__(self, base_url='https://api.superjob.ru/2.0/'):
        super().__init__(base_url)

    def get_vacancies(self, query):
        url = f'{self.base_url}vacancies'
        param = {'keyword': query}
        header = {'X-Api-App-Id': API_TOKEN}

        try:
            response = requests.get(url, param, headers=header)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f'Запрос невозможен: {str(e)}')

        return [self._create_vacancy(item) for item in response.json().get('objects', [])]

    def _create_vacancy(self, data: dict) -> Vacancy:

        url = data.get('link')
        name = data.get('profession')

        # Детали по зарплате
        salary = data.get('payment_from')
        if salary:
            salary_to = data.get('payment_to') if data.get('payment_to') is not None else 0
            salary_currency = data.get('currency')

            # Полная информация по зарплате, собранная в строку для отображения
            salary_str = f'{salary}-{salary_to} {salary_currency}' if salary is not None else 'Зарплата не указана'
        else:
            salary_str = 'Зарплата не указана'
            salary = 0

        requirements = data.get('candidat')

        return Vacancy(url=url, name=name, salary_str=salary_str, salary=salary, requirements=requirements)
