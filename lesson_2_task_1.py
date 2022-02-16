import time

import requests
from bs4 import BeautifulSoup


class Vacancy:
    def __init__(self, job_title, link, salary):
        self.job_title = job_title
        self.link = link
        self.salary = salary
        self.vacancy_site='https://hh.ru'


HEADERS = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}


def get_input_data():
    vacancy_name = input("Введите название вакансии ")
    number_page = input("Введите количество страниц ")
    return vacancy_name, int(number_page)


def get_url(vacancy_name, page):
    return f'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=' \
           f'&text={vacancy_name}&page={page}&hhtmFrom=vacancy_search_list'


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
                salary = span.text
            else:
                salary = None
            vacancy = Vacancy(job_title, vacancy_link, salary)
            data.append(vacancy)
    except Exception as e:
        print(e)
    return data


def pipline():
    rezult_data = []
    vacancy_name, number_page = get_input_data()
    for page in range(number_page):
        url = get_url(vacancy_name, page)
        data = make_request(url)
        rezult_data.extend(data)
        time.sleep(1)
    return rezult_data


vacancys = pipline()
for n, vac in enumerate(vacancys, start=1):
    print(n, f'{vac.job_title} - {vac.salary}')


# <span data-qa="" class="bloko-header-section-3">3 000 – 5 000 <!-- -->USD</span>
# <div class="vacancy-serp-item_premium" data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_premium"><div class="vacancy-serp-item__row vacancy-serp-item__row_labels"><div class="vacancy-serp-item__label" data-qa=""><div class="search-result-label search-result-label_no-resume" data-qa=""><div class="bloko-text">Отклик без резюме</div></div><div class="bloko-v-spacing bloko-v-spacing_base-2"></div></div><div class="vacancy-serp-item__label" data-qa="vacancy-label-item-first"><div class="search-result-label search-result-label_few-responses" data-qa="vacancy-label-be-first"><div class="bloko-text">Будьте первыми</div></div><div class="bloko-v-spacing bloko-v-spacing_base-2"></div></div></div><div class=""><div class=""><div class="vacancy-serp-item__row vacancy-serp-item__row_header"><div class="vacancy-serp-item__info"><span data-qa="bloko-header-3" class="bloko-header-section-3 bloko-header-section-3_lite"><span class="resume-search-item__name"><span class="g-user-content" data-page-analytics-experiment-event="vacancy_search_suitable_item"><a data-qa="vacancy-serp__vacancy-title" target="_blank" class="bloko-link" href="https://hh.ru/analytics_source/vacancy/52414090?from=vacancy_search_list&amp;hhtmFrom=vacancy_search_list&amp;query=Python&amp;requestId=164495996286489f1f92b0147f4a86e9&amp;totalVacancies=16147&amp;position=6&amp;source=vacancies">Software Engineer</a></span></span></span></div><div class="vacancy-serp-item__sidebar"><span data-qa="vacancy-serp__vacancy-compensation" class="bloko-header-section-3 bloko-header-section-3_lite">4 800 – 7 500 <!-- -->USD</span></div></div><div class="vacancy-serp-item__row"><div class="vacancy-serp-item__info"><div class="bloko-text bloko-text_small bloko-text_tertiary"><div class="vacancy-serp-item__meta-info-company"><a data-qa="vacancy-serp__vacancy-employer" class="bloko-link bloko-link_kind-secondary" href="/employer/5928981?hhtmFrom=vacancy_search_list">lemon.io</a></div><div class="vacancy-serp-item__meta-info-badges"><div class="vacancy-serp-item__meta-info-link"><a target="_blank" class="bloko-link" href="https://feedback.hh.ru/article/details/id/5951"><span class="bloko-icon bloko-icon_done bloko-icon_initial-action"></span></a></div></div></div><div data-qa="vacancy-serp__vacancy-address" class="bloko-text bloko-text_small bloko-text_tertiary">Киев</div></div></div></div></div><div class="vacancy-serp-item__row"><div class="vacancy-serp-item__info"><div class="g-user-content"><div data-qa="vacancy-serp__vacancy_snippet_responsibility" class="bloko-text"><span>Did you hear that this January a London-based surgeon performed a test surgery on a banana that was located...</span></div><div data-qa="vacancy-serp__vacancy_snippet_requirement" class="bloko-text bloko-text_no-top-indent"><span>Solidity. Sounds great? — Join us in 2 easy steps: 1. Live interview. We need to make sure you are good...</span></div></div></div><div class="vacancy-serp-item__sidebar"><a data-qa="vacancy-serp__vacancy-employer-logo" href="/employer/5928981?hhtmFrom=vacancy_search_list"><img src="https://hhcdn.ru/employer-logo/4130136.png" loading="lazy" alt="lemon.io" class="vacancy-serp-item-logo"></a></div></div><div class="vacancy-serp-item__row vacancy-serp-item__row_controls"><div class="vacancy-serp-item__controls-item vacancy-serp-item__controls-item_response"><a class="bloko-button bloko-button_kind-primary bloko-button_scale-small" data-qa="vacancy-serp__vacancy_response" href="/applicant/vacancy_response?vacancyId=52414090&amp;hhtmFrom=vacancy_search_list"><span>Откликнуться</span></a></div><span class="vacancy-serp-item__controls-item vacancy-serp-item__controls-item_contacts"><span data-qa="vacancy-serp__vacancy_contacts" class="bloko-link"><span class="vacancy-serp-item-control-gt-xs">Показать контакты</span><span class="vacancy-serp-item-control-xs-only">Контакты</span></span></span><span class="vacancy-serp-item__controls-item vacancy-serp-item__controls-item_pubdate" data-qa="vacancy-serp__vacancy-date"><span class="vacancy-serp-item__publication-date vacancy-serp-item__publication-date_long">14&nbsp;февраля</span><span class="vacancy-serp-item__publication-date vacancy-serp-item__publication-date_short">14.02</span></span></div></div>
#a11y-main-content > div:nth-child(12)
# <div class="vacancy-serp-item__info"><div class="bloko-text bloko-text_small bloko-text_tertiary"><div class="vacancy-serp-item__meta-info-company"><a data-qa="vacancy-serp__vacancy-employer" class="bloko-link bloko-link_kind-secondary" href="/employer/3529?dpt=3529-3529-it&amp;hhtmFrom=vacancy_search_list">Сбер. IT</a></div><div class="vacancy-serp-item__meta-info-badges"><div class="vacancy-serp-item__meta-info-link"><a target="_blank" class="bloko-link" href="https://feedback.hh.ru/article/details/id/5951"><span class="bloko-icon bloko-icon_done bloko-icon_initial-action"></span></a></div><div class="vacancy-serp-item__meta-info-link"><a rel="nofollow noindex" data-qa="vacancy-serp__vacancy_hrbrand vacancy-serp__vacancy_hrbrand_winners" class="bloko-link bloko-link_disable-visited" href="http://hrbrand.ru/"><span class="bloko-icon bloko-icon_hr-brand bloko-icon_initial-unique"></span></a></div><div class="vacancy-serp-item__meta-info-link"><a rel="nofollow noindex" data-qa="vacancy-serp__vacancy_employer-hh-rating" class="bloko-link bloko-link_disable-visited" href="https://rating.hh.ru/history/rating2020?utm_source=hh.ru&amp;utm_medium=referral&amp;utm_campaign=icon&amp;utm_term=anonymous"><span class="bloko-icon bloko-icon_employer-hh-rating bloko-icon_initial-unique"></span></a></div></div></div><div data-qa="vacancy-serp__vacancy-address" class="bloko-text bloko-text_small bloko-text_tertiary">Москва</div></div>
# <span class="pager-item-not-in-short-range" data-qa="pager-page-wrapper-40-39"><a class="bloko-button" rel="nofollow" data-qa="pager-page" href="/search/vacancy?search_field=name&amp;search_field=company_name&amp;search_field=description&amp;text=Python&amp;from=suggest_post&amp;page=39&amp;hhtmFrom=vacancy_search_list"><span>40</span></a><span class="bloko-form-spacer"></span></span>
# div class="vacancy-serp-item vacancy-serp-item_premium"
# data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_premium"><div class="vacancy-serp-item__row vacancy-serp-item__row_labels"><div class="vacancy-serp-item__label" data-qa=""><div class="search-result-label search-result-label_no-resume" data-qa=""><div class="bloko-text">Отклик без резюме</div></div><div class="bloko-v-spacing bloko-v-spacing_base-2"></div></div><div class="vacancy-serp-item__label" data-qa="vacancy-label-item-first"><div class="search-result-label search-result-label_few-responses" data-qa="vacancy-label-be-first"><div class="bloko-text">Будьте первыми</div></div><div class="bloko-v-spacing bloko-v-spacing_base-2"></div></div></div><div class=""><div class=""><div class="vacancy-serp-item__row vacancy-serp-item__row_header"><div class="vacancy-serp-item__info"><span data-qa="bloko-header-3" class="bloko-header-section-3 bloko-header-section-3_lite"><span class="resume-search-item__name"><span class="g-user-content" data-page-analytics-experiment-event="vacancy_search_suitable_item"><a data-qa="vacancy-serp__vacancy-title" target="_blank" class="bloko-link" href="https://hh.ru/vacancy/52414090?from=vacancy_search_list&amp;hhtmFrom=vacancy_search_list&amp;query=Python">Software Engineer</a></span></span></span></div><div class="vacancy-serp-item__sidebar"><span data-qa="vacancy-serp__vacancy-compensation" class="bloko-header-section-3 bloko-header-section-3_lite">4 800 – 7 500 <!-- -->USD</span></div></div><div class="vacancy-serp-item__row"><div class="vacancy-serp-item__info"><div class="bloko-text bloko-text_small bloko-text_tertiary"><div class="vacancy-serp-item__meta-info-company"><a data-qa="vacancy-serp__vacancy-employer" class="bloko-link bloko-link_kind-secondary" href="/employer/5928981?hhtmFrom=vacancy_search_list">lemon.io</a></div><div class="vacancy-serp-item__meta-info-badges"><div class="vacancy-serp-item__meta-info-link"><a target="_blank" class="bloko-link" href="https://feedback.hh.ru/article/details/id/5951"><span class="bloko-icon bloko-icon_done bloko-icon_initial-action"></span></a></div></div></div><div data-qa="vacancy-serp__vacancy-address" class="bloko-text bloko-text_small bloko-text_tertiary">Киев</div></div></div></div></div><div class="vacancy-serp-item__row"><div class="vacancy-serp-item__info"><div class="g-user-content"><div data-qa="vacancy-serp__vacancy_snippet_responsibility" class="bloko-text"><span>Did you hear that this January a London-based surgeon performed a test surgery on a banana that was located...</span></div><div data-qa="vacancy-serp__vacancy_snippet_requirement" class="bloko-text bloko-text_no-top-indent"><span>Solidity. Sounds great? — Join us in 2 easy steps: 1. Live interview. We need to make sure you are good...</span></div></div></div><div class="vacancy-serp-item__sidebar"><a data-qa="vacancy-serp__vacancy-employer-logo" href="/employer/5928981?hhtmFrom=vacancy_search_list"><img src="https://hhcdn.ru/employer-logo/4130136.png" loading="lazy" alt="lemon.io" class="vacancy-serp-item-logo"></a></div></div><div class="vacancy-serp-item__row vacancy-serp-item__row_controls"><div class="vacancy-serp-item__controls-item vacancy-serp-item__controls-item_response"><a class="bloko-button bloko-button_kind-primary bloko-button_scale-small" data-qa="vacancy-serp__vacancy_response" href="/applicant/vacancy_response?vacancyId=52414090&amp;hhtmFrom=vacancy_search_list"><span>Откликнуться</span></a></div><span class="vacancy-serp-item__controls-item vacancy-serp-item__controls-item_contacts"><span data-qa="vacancy-serp__vacancy_contacts" class="bloko-link"><span class="vacancy-serp-item-control-gt-xs">Показать контакты</span><span class="vacancy-serp-item-control-xs-only">Контакты</span></span></span><span class="vacancy-serp-item__controls-item vacancy-serp-item__controls-item_pubdate" data-qa="vacancy-serp__vacancy-date"><span class="vacancy-serp-item__publication-date vacancy-serp-item__publication-date_long">14&nbsp;февраля</span><span class="vacancy-serp-item__publication-date vacancy-serp-item__publication-date_short">14.02</span></span></div></div>