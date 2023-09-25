from abc import ABC, abstractmethod
import json


class FileManager(ABC):
    """Класс для работы с файлами"""

    @abstractmethod
    def add_vac(self, file_path):
        """Добавить вакансию в хранилище"""
        pass

    @abstractmethod
    def get_vac(self, file_path):
        """Получить вакансии из хранилища по указанным критериям"""
        pass


class JSONFileManager(FileManager):
    """Класс для записи и чтения JSON-файла"""

    def __init__(self, file_path):
        self.file_path = file_path

    def add_vac(self, vacancy_data):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(vacancy_data, file, ensure_ascii=False)
            file.write('\n')

    def get_vac(self, criteria):
        """Возвращает список вакансий, отфильтрованный по заданным ключевым словам"""

        criteria = [word.lower() for word in criteria]  # Привести все слова фильтрации в нижний регистр

        filtered_vacancies = []

        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                vacancy_list = json.loads(line)

                for vacancy in vacancy_list:
                    if vacancy['requirements']:
                        requirements = vacancy.get('requirements', '')
                        if requirements is not None:
                            requirements = requirements.lower()  # Привести требования к вакансии в нижний регистр

                        # Проверить, что все ключевые слова есть в требованиях к вакансии
                        if all(word in requirements for word in criteria):
                            filtered_vacancies.append(vacancy)
        return filtered_vacancies
