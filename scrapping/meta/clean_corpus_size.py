from wiki.scrapping.service import *

with open('clean_corpus_size.csv', 'w') as f:
    f.write('Language,Sentence_count\n')


en_sentence_count = 0
en_files = get_files_in_folder('ver2/articles_clean_ver2/en')
for file in en_files:
    en_sentence_count += get_num_sentences_in_file(file)
with open('clean_corpus_size.csv', 'a') as f:
    f.write(f'EN,{en_sentence_count}\n')

fr_sentence_count = 0
fr_files = get_files_in_folder('ver2/articles_clean_ver2/fr')
for file in fr_files:
    fr_sentence_count += get_num_sentences_in_file(file)
with open('clean_corpus_size.csv', 'a') as f:
    f.write(f'FR,{fr_sentence_count}\n')

zh_sentence_count = 0
zh_files = get_files_in_folder('ver2/articles_clean_ver2/zh-cn')
for file in zh_files:
    zh_sentence_count += get_num_sentences_in_file(file)
with open('clean_corpus_size.csv', 'a') as f:
    f.write(f'ZH,{zh_sentence_count}\n')