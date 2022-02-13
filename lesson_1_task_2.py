import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv("./.env")


def get_url():
    city_name = input("Введите название города ")
    key = 'KEY'
    api_key = os.getenv(key, None)
    return f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'


def make_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(e)

def output_data(data):
    print (f'Tемпература {data.get("main").get("temp")} гр.Цельсия')
    print(f'Скорость ветра {data.get("wind").get("speed")} м/с')

def pipeline():
    url = get_url()
    data = make_request(url)
    if data:
        output_data(data)
    else:
        print('Нет данных')


if __name__ == "__main__":
    pipeline()



