from wiki.scrapping.service import *
import pandas as pd
import os


def get_cat_name(cat_soup):
    name_raw = cat_soup.text
    # Get the header up to the first (
    name = name_raw.split('(')[0].rstrip().replace(",", "")
    return name


def start_meta_file(file):
    with open(file, 'w') as f:
        f.write('EN_Name,FR_Name,ZH_Name,EN_URL,FR_URL,ZH_URL,Category\n')


def write_meta(en_name, fr_name, zh_name, en_url, fr_url, zh_url, cat, file):
    with open(file, 'a') as f:
        f.write(f'{en_name},{fr_name},{zh_name},{en_url},{fr_url},{zh_url},{cat}\n')


root_soup = load_page_soup("https://en.wikipedia.org/wiki/Wikipedia:Vital_articles")
categories = root_soup.find_all('h2', {'class': 'ext-discussiontools-init-section'})

meta_file = 'articles_meta.csv'

#start_meta_file(meta_file)

existing_data = pd.read_csv('articles_meta.csv')
url_set = set(existing_data["EN_URL"])

for cat in categories:
    en_urls = get_list_of_articles('en', cat.nextSibling.nextSibling)
    cat_name = get_cat_name(cat)
    for en_url in en_urls:
        print(en_url)
        if en_url not in url_set:
            en_article_soup = load_page_soup(en_url)
            en_name = get_article_name(en_article_soup)
            dump_article_html(en_article_soup, 'en', en_name)
            dump_text_only(en_article_soup, 'en', en_name)

            fr_url = get_in_another_language(en_article_soup, 'fr')
            if fr_url:
                fr_article_soup = load_page_soup(fr_url)
                fr_name = get_article_name(fr_article_soup)
                dump_article_html(fr_article_soup, 'fr', en_name)
                dump_text_only(fr_article_soup, 'fr', en_name)
            else:
                fr_url = "NA"
                fr_name = "NA"

            zh_url = get_in_another_language(en_article_soup, 'zh-cn')
            if zh_url:
                zh_article_soup = load_page_soup(zh_url)
                zh_name = get_article_name(zh_article_soup)
                dump_article_html(zh_article_soup, 'zh-cn', en_name)
                dump_text_only(zh_article_soup, 'zh-cn', en_name)
            else:
                zh_url = "NA"
                zh_name = "NA"

            write_meta(en_name, fr_name, zh_name, en_url, fr_url, zh_url, cat_name, meta_file)

            print(en_name, fr_name, zh_name, en_url, fr_url, zh_url, cat_name)

