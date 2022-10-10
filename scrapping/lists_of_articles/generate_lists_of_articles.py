import requests
import json
import re
from bs4 import BeautifulSoup

main_pages = {
    'en': 'https://en.wikipedia.org/wiki/Wikipedia:Vital_articles',
    'fr': 'https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Articles_vitaux',
    'zh': 'https://zh.wikipedia.org/wiki/Wikipedia:%E5%9F%BA%E7%A4%8E%E6%A2%9'
          'D%E7%9B%AE/%E8%8B%B1%E8%AA%9E%E7%B6%AD%E5%9F%BA%E7%99%BE%E7%A7%91%E7%AC%AC%E4%B8%89%E7%B4%9A'
}


def load_page_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def construct_url(language, partial):
    return f'https://{language}.main.org{partial}'


def get_list_of_articles(language, soup):
    # Find urls (a tags), exclude service links like File, Category, User etc
    results = soup.find_all('a', {'href': re.compile(r'^/wiki/(?!Wikipedia)(?!File)(?!User)(?!Category).*')})

    # For all the found partial links construct a full URL and store it in a set to avoid duplicates
    return {construct_url(language, x['href']) for x in results}


def write_results(language, results):
    with open(f'lists_of_articles/{language}_list_of_urls.txt', 'w') as f:
        for res in results:
            f.writelines(f'{res}\n')


for language, url in main_pages.items():
    soup = load_page_soup(url)
    results = get_list_of_articles(language, soup)
    write_results(language, results)


