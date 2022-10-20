from wiki.scrapping.service import replace_pairs, replace_chars, scrapping_path, get_files_in_folder, get_filename
from wiki.scrapping.service import scrapping_path
import re

zh_replacement_pairs = [
    # remove edit button
    (r'\[编辑\]', ''),

    # remove notes
    (r'\[注 \d+\]', ''),

    # some random gs are added to the chinese text
    (r'g(?=[\u4e00-\u9fff])', ''),

    # add a line break after the chines dot
    (r'。(?!$)', '。\n'),

    # remove dots in the beginning of the string
    (r'^[. ]+', ''),

    # remove chinese quote at the begining of sentence
    (r'^(」|，)', ''),

    (r'^。$', '')

]

zh_replacement_pairs.extend(list(replace_pairs))

zh_articles = get_files_in_folder('/ver2/articles_text_ver2/zh-cn')

for article in zh_articles:
    filename = get_filename(article)
    with open(article, 'r') as f:
        example_text = [replace_chars(y, zh_replacement_pairs) for y in f.readlines()]
        clean = ''.join(example_text).replace('\n\n', '\n')

        with open(f'{scrapping_path}ver2/articles_clean_ver2/zh-cn/{filename}', 'w') as f2:
            f2.write(clean)
        print(filename)
