**Название проекта**

Парсинг информации о вакансиях с разных платформ в России.

**Описание проекта**

На данном этапе можно получать информацию по выбору с одной из платформ: HeadHunter или SuperJob. Поиск вакансий осуществляется по ключевому запросу.
Найденные по запросу вакансии сохраняются с json-файл.
Можно вывести топ вакансий с лучшим предложением по зарплате и отфильтровать вакансии по интересующим требованиям.

**Установка**

Прежде чем начать использовать API от SuperJob, необходимо зарегистрироваться (https://www.superjob.ru/auth/login/) и получить токен для работы. 
Подробная инструкция дается по ссылке описания документации в разделе Getting started: https://api.superjob.ru/#gettin. 
При регистрации приложения можно указать произвольные данные.

Для корректной работы программы необходимо создать файл config.py сохранить в нём полученный токен в переменную API_TOKEN.

**Зависимости**

Из сторонних библиотек требуется только установка requests.
