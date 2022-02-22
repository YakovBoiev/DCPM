import json
import time
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

URL = 'https://hh.ru/search/vacancy'
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'test'

HEADERS = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/97.0.4692.71 Safari/537.36'
}


def create_vacancy_dict(job_title, link, salary_min, salary_max, salary_currency):
    return {
        'job_title': job_title,
        'link': link,
        'salary_min': salary_min,
        'salary_max': salary_max,
        'salary_currency': salary_currency,
        'vacancy_site': 'https://hh.ru'
    }


def get_input_data():
    vacancy_name = input("Введите название вакансии ")
    number_page = input("Введите количество страниц ")
    return vacancy_name, int(number_page)


def get_params(vacancy_name, page):
    params = {
        'text': vacancy_name,
        'page': str(page),
        'hhtmFrom': 'vacancy_search_list'
    }
    return params


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
        salary_min = int(salary)
    else:
        salary_max = int(salary)
        salary = ""
        while salary_info and salary_info[-1].isdigit:
            egg = salary_info.pop()
            salary = egg + salary
        if salary:
            salary_min = int(salary)
    return salary_min, salary_max, currency


def write_data(data):
    with open('test.json', "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def write_data_db(db, data):
    collection = db['vacancy_col']
    for vacancy in data:
        if collection.find_one({'link': vacancy['link']}):
            continue
        collection.insert_one(vacancy)


def output_vacancy_salary_min(db):
    salary_min = int(input('Введите минимальную зарплату '))
    collection = db['vacancy_col']
    vacancy_list = collection.find({'salary_min': {'$gt': salary_min}}, )
    # vacancy_list = collection.find({'&end': [{'salary_min': {'$gt': salary_min}}, {'salary_currency': 'руб.'}]})
    for vacancy in vacancy_list:
        pprint(vacancy)


def make_request(url, params):
    data = []
    try:
        response = requests.get(url, headers=HEADERS, params=params)
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
            vacancy = create_vacancy_dict(job_title, vacancy_link, salary_min, salary_max, salary_currency)
            data.append(vacancy)
    except Exception as e:
        print(e)
    return data


def pipeline():
    result_data = []
    vacancy_name, number_page = get_input_data()
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        for page in range(number_page):
            params = get_params(vacancy_name, page)
            data = make_request(URL, params)
            write_data_db(db, data)
            result_data.extend(data)
            time.sleep(1)
        output_vacancy_salary_min(db)
    return result_data


if __name__ == "__main__":
    pipeline()
