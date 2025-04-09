import psycopg2
from config import DB_CONFIG


class DBManager:
    def __init__(self, db_name: str):
        self.conn = psycopg2.connect(dbname=db_name, **DB_CONFIG)

    def get_companies_and_vacancies_count(self) -> list:
        """Получить список компаний и количество вакансий."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, COUNT(v.vacancy_id)
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name
            """
            )
            return cur.fetchall()

    def get_all_vacancies(self) -> list:
        """Получить все вакансии с указанием компании."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
            """
            )
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Получить среднюю зарплату."""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT AVG(avg_salary) FROM vacancies WHERE avg_salary IS NOT NULL"
            )
            return round(cur.fetchone()[0], 2)

    def get_vacancies_with_higher_salary(self) -> list:
        """Получить вакансии с зарплатой выше средней."""
        avg = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.title, v.avg_salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.avg_salary > %s
            """,
                (avg,),
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """Получить вакансии по ключевому слову."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.title, v.avg_salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.title ILIKE %s
            """,
                (f"%{keyword}%",),
            )
            return cur.fetchall()

    def close(self) -> None:
        """Закрыть соединение с БД."""
        self.conn.close()
