from bs4 import BeautifulSoup
import requests
import re
from pathlib import Path
import os
import glob
import chinese_converter

scrapping_path = os.environ['SCRAPPING']

# Put a link to the folder
html_folder = Path('{env_var}articles_html'.format(env_var=scrapping_path))
text_folder = Path('{env_var}articles_text'.format(env_var=scrapping_path))

replace_pairs = (
    # remove the quotation, like [1]
    (r'\[[\d\w ]+]', ''),
    # remove citation like (1)
    (r'\(\d+\)', ''),
    # remove math figures
    (r'{\\displaystyle .*', ''),
    # remove space in the beginning of line
    (r'^ ', ''),
    # remove the sign of quotation mark
    (r'\^', ''),
    # remove the arrows
    (u'\u2191', ''),
    ('←', ''),
    ('→', ''),
    # remove the list of languages, that should always contains this sequence
    (r'.*(EspañolEsperanto|EsperantoEspañol).*', ''),
    # remove urls beginning with https
    (r'https?\://[\w \./\?\=&-]+', ''),
    # remove urls beginning with www
    (r'www\.[\w \./\?\=&-]+', ''),
    # remove (en)|(en-GB)|(en-US) mark before the quoted resources
    (r'\(en(?:\)|-GB\)|-US\))', ''),
    # check lines containing multiple sentences and break them into different lines
    (r'(?<=[a-z][a-z"»』」\)])\. (?=[A-Z«"『「][\w \'])', '.\n'),
    # break lines if sentence ends with an abbreviation
    (r'(?<=[A-Z][A-Z])\. (?=[A-Z«"『「][\w \'])', '.\n'),
    # break lines abbreviation and quotaion
    (r'(?<=[A-Z][A-Z]["»』」\)]) (?=[A-Z«"『「][\w \'])', '\n'),
    # break a quoted sentence into different lines
    (r'(?<=[a-z]\.[»』」"]) (?=[A-Z«"『「][\w \'])', '\n'),
    # remove a broken parenthesis: if a string ends with (
    (r'\($', ''),
    # remove a broken parenthesis: if a string starts with )
    (r'^\)', ''),
    # remove a string if it's just separators and spaces
    (r'^\W+$', ''),
    # remove a string that's just one letter
    (r'^\w$', ''),
    # replace multiple line breaks with one
    (r'\n+', '\n'),
    # replace multiple spaces with one
    (r' +', ' ')
)


def get_article_name(soup):
    # return soup.find('span', {'class': 'mw-page-title-main'}).text
    return soup.find('h1').text.replace("/", "").replace(",", "")


def load_page_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_article_lines(soup):
    lines = []
    for el in ['h1', 'h2', 'h3', 'h4', 'p']:
        lines.extend(x.text.strip() for x in soup.find_all(el))
    return lines


def construct_url(language, partial):
    return f'https://{language}.wikipedia.org{partial}'


def write_article_lines(lines, filename):
    with open(filename, 'w') as f:
        for line in lines:
            f.write(f'{line}\n')


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


def load_soup_by_html(filename):
    with open(filename, 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def replace_chars(s, replace_pairs):
    # apply all the rules above in the order
    for pair in replace_pairs:
        s = re.sub(*pair, s)
    s = remove_toc(s)
    return s.lstrip()


def remove_toc(s):
    # completely removes all Table of Contents lines, since they are duplicated later in the text
    regex = r"^(\d{1,2}(?:\.\d){0,}[A-Z« ])"
    cond = re.match(regex, s)
    if cond:
        s = re.sub(regex, '', s)
    return s


def get_files_in_folder(path_from_scrapping):
    return glob.glob(f'{scrapping_path}{path_from_scrapping}/*')


def get_filename(filepath):
    return filepath.split('/')[-1]


def get_num_sentences_in_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return len(lines)