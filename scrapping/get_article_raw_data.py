from bs4 import BeautifulSoup
import requests

languages = ['en', 'fr', 'zh']


def load_page_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_article_name(soup):
    return soup.find('span', {'class': 'mw-page-title-main'}).text


def dump_article(language, soup):
    name = get_article_name(soup)
    with open(f'articles_html/{language}/{name}.txt', 'w') as f:
        f.write(str(soup))

    with open(f'articles_text/{language}/{name}.txt', 'w') as f:
        f.write(soup.text)


language = 'en'
soup = load_page_soup('https://en.wikipedia.org/wiki/Culture')
dump_article(language, soup)
