import os
from api_manager import HeadHunterAPI, SuperJobAPI
from file_manager import JSONFileManager

current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_directory, 'vacancies.json')
json_storage = JSONFileManager(json_file_path)


# Функция для взаимодействия с пользователем
def user_interaction():
    platforms = ['HeadHunter', 'SuperJob']

    while True:
        platform_choice = input('Выберите сайт для поиска вакансий: HeadHunter (введите 1) или SuperJob (введите 2): ')
        if platform_choice in ('1', '2'):
            choice = int(platform_choice)
            break
        else:
            print('Пожалуйста, введите 1 или 2.')

    platform = platforms[choice - 1]
    print(f'Ищем вакансии на {platform}.')

    hh = HeadHunterAPI()
    sj = SuperJobAPI()

    search_query = input('Введите поисковый запрос: ')
    result = [hh.get_vacancies(search_query), sj.get_vacancies(search_query)][choice - 1]

    # Запись полученных по запросу вакансий в JSON-файл
    storage = []
    for vacancy in result:
        storage.append(vacancy.to_dict())
        json_storage.add_vac(storage)

    while True:
        action_choice = input('Выберите действие: отфильтровать вакансии по зарплате (введите 1), '
                              'отфильтровать вакансии по ключевым словам (введите 2): ')
        if action_choice in ('1', '2'):
            choice = int(action_choice)
            break
        else:
            print("Пожалуйста, введите 1 или 2.")

    if choice == 1:
        # Вывод топ вакансий по зарплате в заданном количестве
        top_n = int(input('Введите количество вакансий для вывода в топ: '))
        sorted_vacancies = sort_vacancies(result)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
        print_vacancies(top_vacancies)

    else:
        filter_words = input('Введите ключевые слова для фильтрации вакансий через запятую: ').split(',')
        filtered_vacancies = json_storage.get_vac(criteria=filter_words)
        print_vacancies_from_json(filtered_vacancies)

        if not filtered_vacancies:
            print('Нет вакансий, соответствующих заданным критериям.')


def sort_vacancies(vacancies):
    """Сортирует вакансии по уровню зарплаты"""
    return sorted(vacancies, key=lambda v: v.salary, reverse=True)


def get_top_vacancies(sorted_vacancies: list, top_n: int) -> list:
    """Возвращает список отсортированных вакансий заданной длины"""
    return sorted_vacancies[:top_n]


def print_vacancies_from_json(vacancies):
    """Печатает список отфильтрованных вакансий из JSON-файла"""
    for i, vacancy in enumerate(vacancies, start=1):
        print(f"Вакансия {i}: {vacancy['name']}, {vacancy['salary_str']}, {vacancy['url']}")
        print('---')


def print_vacancies(vacancies):
    """Печатает список отфильтрованных вакансий"""
    for i, vacancy in enumerate(vacancies, start=1):
        print(f"Вакансия {i}: {vacancy.name}, {vacancy.salary_str}, {vacancy.url}")
        print('---')


if __name__ == "__main__":
    user_interaction()
