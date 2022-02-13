import json
import os
import requests


def get_url():
    user_name = input("Введите username пользователя GitHub ")
    return os.path.join('https://api.github.com/users', user_name, 'repos')


def separate_last_page_link(page_links):
    last_page_link = page_links.split()[-2][1:-2]
    page_link = last_page_link[:-1]
    last_page_number = int(last_page_link[-1])
    return page_link, last_page_number


def make_request(url):
    json_data = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data.extend(response.json())
        headers = dict(response.headers)
        link = headers.get('Link')
        if link:
            page_link, last_page_number = separate_last_page_link(link)
            for i in range(2, last_page_number + 1):
                response = requests.get(f'{page_link}{str(i)}')
                response.raise_for_status()
                json_data.extend(response.json())
        return json_data
    except Exception as e:
        print(e)


def create_list_repos_name(data):
    repos_name_list = []
    print('Список репозиториев')
    for number, repos in enumerate(data, start=1):
        print(number, repos['name'])
        repos_name_list.append(repos['name'])
    return repos_name_list


def write_data(data):
    with open('test.json', "w") as f:
        json.dump(data, f, indent=4)


def pipeline():
    url = get_url()
    data = make_request(url)
    if data:
        create_list_repos_name(data)
        write_data(data)
    else:
        print('Нет данных')


if __name__ == "__main__":
    pipeline()
