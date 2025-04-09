import requests


def get_employer(employer_id: str) -> dict:
    """Получить данные о компании по ID."""
    url = f"https://api.hh.ru/employers/{employer_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_vacancies(employer_id: str) -> list:
    """Получить список вакансий компании."""
    url = "https://api.hh.ru/vacancies"
    vacancies = []
    page = 0
    while True:
        params = {"employer_id": employer_id, "page": page, "per_page": 100}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        vacancies.extend(data["items"])
        if page >= data["pages"] - 1:
            break
        page += 1
    return vacancies
