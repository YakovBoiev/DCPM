import time

import requests
from bs4 import BeautifulSoup


class Vacancy:
    def __init__(self, job_title, link, salary_min, salary_max, salary_currency):
        self.job_title = job_title
        self.link = link
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.salary_currency = salary_currency
        self.vacancy_site = 'https://hh.ru'


HEADERS = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/97.0.4692.71 Safari/537.36'
}


def get_input_data():
    vacancy_name = input("Введите название вакансии ")
    number_page = input("Введите количество страниц ")
    return vacancy_name, int(number_page)


def get_url(vacancy_name, page):
    return f'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=' \
           f'&text={vacancy_name}&page={page}&hhtmFrom=vacancy_search_list'


def get_salary_info(salary_str):
    salary_info = salary_str.split()
    salary_min = None
    salary_max = None
    currency = salary_info.pop()
    salary = ""
    while salary_info[-1].isdigit():
        egg = salary_info.pop()
        salary = egg + salary
    spam = salary_info.pop()
    if spam == "от":
        salary_min = salary
    else:
        salary_max = salary
        salary = ""
        while salary_info and salary_info[-1].isdigit:
            egg = salary_info.pop()
            salary = egg + salary
        salary_min = salary
    return salary_min, salary_max, currency


def make_request(url):
    data = []
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        html_string = response.text
        soup = BeautifulSoup(html_string, "html.parser")
        vacancy_list = soup.findAll(attrs={'class': 'vacancy-serp-item_redesigned'})
        for vacancy in vacancy_list:
            tag_a = vacancy.find(attrs={'class': 'resume-search-item__name'}).find('a')
            vacancy_link = tag_a.get('href')
            job_title = tag_a.string
            span = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            if span:
                salary_min, salary_max, salary_currency = get_salary_info(span.text)
            else:
                salary_min, salary_max, salary_currency = None, None, None
            vacancy = Vacancy(job_title, vacancy_link, salary_min, salary_max, salary_currency)
            data.append(vacancy)
    except Exception as e:
        print(e)
    return data


def pipeline():
    result_data = []
    vacancy_name, number_page = get_input_data()
    for page in range(number_page):
        url = get_url(vacancy_name, page)
        data = make_request(url)
        result_data.extend(data)
        time.sleep(1)
    return result_data


if __name__ == "__main__":
    data = pipeline()