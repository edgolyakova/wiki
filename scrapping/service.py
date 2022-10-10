from bs4 import BeautifulSoup
import requests
import re
from pathlib import Path

# Put a link to the folder
html_folder = Path('/Users/egoliakova/wikipedia/wiki/scrapping/articles_html')
text_folder = Path('/Users/egoliakova/wikipedia/wiki/scrapping/articles_text')


def get_article_name(soup):
    # return soup.find('span', {'class': 'mw-page-title-main'}).text
    return soup.find('h1').text.replace("/", "").replace(",", "")


def load_page_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def construct_url(language, partial):
    return f'https://{language}.wikipedia.org{partial}'


def get_list_of_articles(language, soup):
    # Find urls (a tags), exclude service links like File, Category, User etc
    results = soup.find_all('a', {'href': re.compile(r'^/wiki/(?!Wikipedia)(?!File)(?!User)(?!Category).*')})

    # For all the found partial links construct a full URL and store it in a set to avoid duplicates
    return {construct_url(language, x['href']) for x in results}


def get_in_another_language(soup, language):
    url = soup.find('a', {'href': re.compile(r'https://{language}.wikipedia.org/.*'.format(language=language)),
                          'class': 'interlanguage-link-target'})

    if url:
        return url['href']
    else:
        return None


def dump_article_html(arcticle_soup, language, en_name):
    with open(f"{html_folder}/{language}/{en_name}.txt", 'w') as f:
        f.write(str(arcticle_soup))


def dump_text_only(arcticle_soup, language, en_name):
    with open(f"{text_folder}/{language}/{en_name}.txt", 'w') as f:
        f.write(arcticle_soup.text)