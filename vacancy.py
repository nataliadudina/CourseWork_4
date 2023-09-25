from functools import total_ordering


@total_ordering
class Vacancy:

    def __init__(self, url, name, salary_str, salary=0, requirements=None):
        self.url = url if url else ''
        self.name = name if name else ''
        self.salary_str = salary_str
        self.salary = salary
        self.requirements = requirements

    def __str__(self):
        return f'{self.url}, {self.name}, {self.salary_str}'

    def __eq__(self, other):
        if isinstance(other, Vacancy):
            return self.salary == other.salary
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Vacancy):
            return self.salary > other.salary
        else:
            return NotImplemented

    def to_dict(self):
        """Конвертирует экземпляр класса в словарь для последующей записи в JSON-файл"""

        return {
            'url': self.url,
            'name': self.name,
            'salary_str': self.salary_str,
            'requirements': self.requirements
        }
