from wiki.scrapping.service import replace_pairs, replace_chars, scrapping_path, get_files_in_folder, get_filename

import re

en_replace_pairs = [
        # this sequence is sometimes added to en wiki article texts, doesn't have any meaning to the article
        ('vte', ''),
        (r'Categories\: .*', ''),

        # remove some internal wiki text in english
        (r'^(?=Not logged inTalk|ReadView sourceView history|Main pageContentsCurrent|HelpLearn|What links hereRelated changes).*', ''),

        #remove edit button
        (r'\[edit\]', ''),

        # remove edit button attached to an end of a sentence
        (r'\.edit', '')
    ]

en_replace_pairs.extend(list(replace_pairs))

en_articles = get_files_in_folder('/ver2/articles_text_ver2/en')

for article in en_articles:
    filename = get_filename(article)
    with open(article, 'r') as f:
            example_text = [replace_chars(y, en_replace_pairs) for y in filter(lambda x: x != '\n', f.readlines())]

            clean = ''.join(example_text).replace('\n\n', '\n')

            with open(f'{scrapping_path}ver2/articles_clean_ver2/en/{filename}', 'w') as f2:
                f2.write(clean)
            print(filename)



