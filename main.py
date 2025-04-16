from database import create_database, create_tables, insert_data
from db_manager import DBManager


def main():
    db_name = "hh_vacancies"
    employer_ids = [
        "1740",
        "78638",
        "1122462",
        "15478",
        "3529",
        "4181",
        "3127",
        "3776",
        "907345",
        "4934",
    ]

    # Создание и наполнение БД
    create_database(db_name)
    create_tables(db_name)
    insert_data(db_name, employer_ids)

    # Работа с пользователем
    db = DBManager(db_name)
    while True:
        print(
            "\n1. Список компаний и вакансий\n2. Все вакансии\n3. Средняя зарплата\n4. Вакансии с высокой зарплатой\n5. Поиск вакансий\n0. Выход"
        )
        choice = input("Выберите действие: ")
        if choice == "1":
            for row in db.get_companies_and_vacancies_count():
                print(f"{row[0]}: {row[1]} вакансий")
        elif choice == "2":
            for row in db.get_all_vacancies():
                print(f"{row[0]}: {row[1]}, Зарплата: {row[2]}-{row[3]}, URL: {row[4]}")
        elif choice == "3":
            print(f"Средняя зарплата: {db.get_avg_salary()}")
        elif choice == "4":
            for row in db.get_vacancies_with_higher_salary():
                print(f"{row[0]}: {row[1]}, Зарплата: {row[2]}, URL: {row[3]}")
        elif choice == "5":
            keyword = input("Ключевое слово: ")
            for row in db.get_vacancies_with_keyword(keyword):
                print(f"{row[0]}: {row[1]}, URL: {row[3]}")
        elif choice == "0":
            break
    db.close()


if __name__ == "__main__":
    main()
