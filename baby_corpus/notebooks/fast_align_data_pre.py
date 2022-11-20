#%%
import pandas as pd
import codecs
from tqdm import tqdm

csv_path = r'C:\Users\lvshu\Downloads\test_seg_v7.csv' #Need a bilingual parallel corpus which is totally cleaned.
df = pd.read_csv(csv_path, header = None)
print(df.head())
df.columns = ['en', 'zh']
df['new'] = df.index.to_series().apply(lambda x : df['en'].iloc[x] + '\t' + df['zh'].iloc[x])
df = df[['new']]
print(df.head())
df.to_csv(r'C:\Users\lvshu\Downloads\test_seg_v8.csv',encoding= 'utf-8', index = False)

#%%
rootpath = r'C:\Users\lvshu\Downloads\test_seg_v8.csv'
topath   = r'C:\Users\lvshu\Downloads\final.txt' #Output as a txt file, the requirement is: between each bilingual sentence there is a " ||| " (before and after '|||', there is a space).
with codecs.open(rootpath,'r',encoding='utf=8') as f1, codecs.open(topath,'w') as f2:
    for line in tqdm(f1):
        f1_lines = line.strip().replace('\t',' ||| ')
        f2.write(f1_lines + '\n' )

# %%

#Then use fast-align (https://github.com/clab/fast_align) which runs in Ubuntu, by using the instructions as follows:
#$ ./fast_align -i text.txt en-zh   -d -o -v > forward.align

#$ ./fast_align -i text.txt en-zh -d -o -v -r > reverse.align

#$ ./atools -i forward.align -j reverse.align -c grow-diag-final-and > final.align