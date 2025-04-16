import psycopg2

from api import get_employer, get_vacancies
from config import DB_CONFIG


def create_database(db_name: str) -> None:
    """Создать новую базу данных."""
    try:
        # Явно задаем кодировку подключения
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"].encode("utf-8").decode("utf-8"),
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            client_encoding="utf-8",
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name} ENCODING 'UTF8'")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Ошибка подключения: {str(e)}")
        raise


def create_tables(db_name: str) -> None:
    """Создать таблицы в базе данных."""
    conn = psycopg2.connect(dbname=db_name, **DB_CONFIG)
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE employers (
                employer_id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255)
            )
        """
        )
        cur.execute(
            """
            CREATE TABLE vacancies (
                vacancy_id INT PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                title VARCHAR(255) NOT NULL,
                salary_from INT,
                salary_to INT,
                avg_salary INT,
                url VARCHAR(255)
            )
        """
        )
    conn.commit()
    conn.close()


def insert_data(db_name: str, employer_ids: list) -> None:
    """Заполнить таблицы данными."""
    conn = psycopg2.connect(dbname=db_name, **DB_CONFIG)
    for employer_id in employer_ids:
        employer = get_employer(employer_id)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO employers (employer_id, name, url)
                VALUES (%s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING
            """,
                (employer["id"], employer["name"], employer["site_url"]),
            )
        vacancies = get_vacancies(employer_id)
        for vacancy in vacancies:
            salary = vacancy.get("salary")
            salary_from = salary["from"] if salary else None
            salary_to = salary["to"] if salary else None
            avg = (
                (salary_from + salary_to) // 2
                if salary_from and salary_to
                else salary_from or salary_to
            )
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO vacancies 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING
                """,
                    (
                        vacancy["id"],
                        employer["id"],
                        vacancy["name"],
                        salary_from,
                        salary_to,
                        avg,
                        vacancy["alternate_url"],
                    ),
                )
    conn.commit()
    conn.close()
