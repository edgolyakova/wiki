from wiki.scrapping.service import replace_pairs, replace_chars, scrapping_path, get_files_in_folder, get_filename

import re

fr_replace_pairs = list(replace_pairs)
fr_replace_pairs.extend(
    [
        # this sequence is sometimes added to french wiki article texts, doesn't have any meaning to the article
        ('v · m', ''),
        # remove edit links in french
        (r'\[(?=modifier).*\]', ''),
        # remove some internal wiki text in french
        (r'^(?=ArticleDiscussion|DiscussionContributions|AccueilPortails thématiquesArticle au hasardContact|'
         r'Débuter sur Wikipédia|Wikimedia Commons|Pages liées|LireModifierModifier le code).*', ''),
        # remove edit button that got attached to the text (attached to a comma)
        (r'\.+modifier', '')
    ]
)

fr_articles = get_files_in_folder('articles_text/fr')

for article in fr_articles:
    filename = get_filename(article)
    with open(article, 'r') as f:
        example_text = [replace_chars(y, fr_replace_pairs) for y in filter(lambda x: x != '\n', f.readlines())]

        clean = ''.join(example_text)
        with open(f'{scrapping_path}/articles_clean/fr/{filename}', 'w') as f2:
            f2.write(clean)
        print(filename)


