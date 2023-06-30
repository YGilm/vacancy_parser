from src.utils import HeadHunterVacancy, SuperJobVacancy, CountMixin, VacancyList


def main():
    """
    Основная функция программы для поиска и фильтрации вакансий.
    """
    count_vacancies = CountMixin('all_vacancy.json')
    return_to_resource_choice = False  # Флаг для возврата к выбору ресурса

    while True:
        if not return_to_resource_choice:
            print("Выберите ресурс для поиска вакансий:")
            print("1. HeadHunter")
            print("2. Superjob")
            print("3. Все ресурсы")
            print("0. Выход")
            resource_choice = input("Введите номер ресурса: ")

            if resource_choice == "0":
                break

            elif resource_choice not in ["1", "2", "3"]:
                print("Вы не выбрали ресурс для поиска вакансий.")
                continue

            keyword = input("Введите ключевое слово для поиска вакансий: ")

            if resource_choice == "1":
                print('Ищем для Вас вакансии')
                resource = "HeadHunter"
                file_name = 'headhunter.json'
                print('Это может занять некоторое время...')
                hh_vacancy = HeadHunterVacancy(keyword)
                hh_vacancy.get_request()
                print('Обрабатываем полученые данные...')
                hh_vacancy.to_json()  # Сохранение данных в файл 'headhunter.json'
                vacancy_list = VacancyList(file_name)
            elif resource_choice == "2":
                print('Ищем для Вас вакансии')
                resource = "Superjob"
                file_name = 'superjob.json'
                print('Это может занять некоторое время...')
                sj_vacancy = SuperJobVacancy(keyword)
                sj_vacancy.get_request()
                print('Обрабатываем полученые данные...')
                sj_vacancy.to_json()  # Сохранение данных в файл 'superjob.json'
                vacancy_list = VacancyList(file_name)
            else:
                resource = "all"
                print('Ищем для Вас вакансии')
                file_name = 'all_vacancy.json'
                print('Это может занять некоторое время...')
                hh_vacancy = HeadHunterVacancy(keyword)
                hh_vacancy.get_request()
                hh_vacancy.to_json()  # Сохранение данных в файл 'headhunter.json'
                sj_vacancy = SuperJobVacancy(keyword)
                sj_vacancy.get_request()
                print('Обрабатываем полученые данные...')
                sj_vacancy.to_json()  # Сохранение данных в файл 'superjob.json'
                vacancy_list = VacancyList(file_name)  # Используем 'all_vacancy.json' для получения списка вакансий
        else:
            return_to_resource_choice = False

        vacancies = vacancy_list.search_vacancies(keyword, resource=resource, count_vacancy=count_vacancies)
        if not vacancies:
            exit("Вакансии не найдены, попробуйте ввести другое ключевое слово.")
        else:
            print(f"Найдено {len(vacancies)} вакансий:")

        vacancy_list.write_vacancies(vacancies)

        print("1. Фильтровать вакансии")
        print("2. Не фильтровать вакансии")
        print("0. Возврат к выбору ресурса")
        filter_choice = input("Выберите действие: ")

        if filter_choice == "0":
            return_to_resource_choice = True  # Установка флага для возврата к выбору ресурса
            continue

        if filter_choice == "1":
            city = input("Введите город для фильтрации (или оставьте пустым): ")
            salary_from = input("Введите нижнюю границу зарплаты для фильтрации (или оставьте пустым): ")
            salary_to = input("Введите верхнюю границу зарплаты для фильтрации (или оставьте пустым): ")
            vacancies = vacancy_list.filter_vacancies(city=city, salary_from=salary_from, salary_to=salary_to)
            print(f"Найдено {len(vacancies)} вакансий после фильтрации:\n")
            for vacancy in vacancies:
                print("Источник:", vacancy["source"])
                print("Название:", vacancy["name"])
                print("Город:", vacancy["city"])
                print("Зарплата:", vacancy["salary"])
                print("Требования:", vacancy["requirements"])
                print("URL:", vacancy["url"])
                print()

        if filter_choice == "2":
            if not vacancies:
                print("Нет доступных вакансий для фильтрации.")
                continue

            print(f"Найдено {len(vacancies)} вакансий:\n")
            for vacancy in vacancies:
                print("Источник:", vacancy["source"])
                print("Название:", vacancy["name"])
                print("Город:", vacancy["city"])
                print("Зарплата:", vacancy["salary"])
                print("Требования:", vacancy["requirements"])
                print("URL:", vacancy["url"])
                print()

            while True:
                print("1. Изменить параметры фильтра данных вакансий")
                print("0. Выход")
                filter_choice = input("Выберите действие: \n")

                if filter_choice == "0":
                    exit("Благодарим за использование нашей программы!")
                elif filter_choice == "1":
                    city = input("Введите город для фильтрации (или оставьте пустым): ")
                    salary_from = input("Введите нижнюю границу зарплаты для фильтрации (или оставьте пустым): ")
                    salary_to = input("Введите верхнюю границу зарплаты для фильтрации (или оставьте пустым): ")
                    vacancies = vacancy_list.filter_vacancies(city=city, salary_from=salary_from, salary_to=salary_to)
                    print(f"Найдено {len(vacancies)} вакансий после фильтрации:")
                    for vacancy in vacancies:
                        print("Источник:", vacancy["source"])
                        print("Название:", vacancy["name"])
                        print("Город:", vacancy["city"])
                        print("Зарплата:", vacancy["salary"])
                        print("Требования:", vacancy["requirements"])
                        print("URL:", vacancy["url"])
                        print()
                else:
                    print("Некорректный выбор. Пожалуйста, повторите.")


if __name__ == "__main__":
    main()
