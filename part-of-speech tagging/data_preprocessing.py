import re
import pandas as pd
import numpy as np
import csv
import os
# train_files_AKN
reg = '[\·\~\！\@\#\￥\%\……\&\*\（\）\——\-\+\=\【\】\{\}\、\|\；\‘\’\：\“\”\《\》\？\，\。\、\`\~\!\#\$\%\^\&\*\(\)\_\[\]{\}\|\;\:\,\.\/\<\>\?]_PU'
for root_dir, sub_dir, files in os.walk(r"train_AKN"):
    for file in files:
        txt = root_dir + "/" + file
        df = pd.read_csv(txt, header=None, index_col=False,sep="\t")
        df1 = df.replace(to_replace='<.*?>', value=np.nan, regex=True) \
            .replace(to_replace='（_PU 完_VV ）_PU', value=np.nan, regex=True) \
            .dropna() \
         .replace(to_replace='  ', value=' ', regex=True)\
            .replace(to_replace='_', value='(', regex=True) \
            .replace(to_replace=' ', value='),', regex=True)
        df1.to_csv(txt, index=False, header=False, sep='t')

#train_files_SKN
for root_dir, sub_dir, files in os.walk(r"train_SKN"):
    for file in files:

        txt = root_dir + "/" + file
        df = pd.read_csv(txt, header=None, index_col=False, sep="\t")
        df1 = df.replace(to_replace='[(](.*?)[)][,]', value='', regex=True)\
        .replace(to_replace='[)][,]', value='', regex=True)
        df1.to_csv(txt, index=False, header=False, sep='t')

        print(txt)
        f = open(txt,encoding='UTF-8').read()
        p = re.compile(r'[(](.*?)[)][,]', re.S)
        new_str1 = re.sub(p, '', f)

test_files
for root_dir, sub_dir, files in os.walk(r"test"):
    for file in files:
        txt = root_dir + "/" + file
        df = pd.read_csv(txt, header=None, index_col=False,sep="\t")
        df1 = df.replace(to_replace='<.*?>', value=np.nan, regex=True) \
            .replace(to_replace='（_PU 完_VV ）_PU', value=np.nan, regex=True) \
            .dropna() \
            .replace(to_replace=reg, value='', regex=True) \
            .replace(to_replace='  ', value=' ', regex=True)
        lst = df1[0].tolist()
        result = []
        len_1 = []
        len_2 = []
        len_3 = []
        for l in lst:
            if not l:
                continue
            temp = l.split(' ')
            words = []
            speechs = []
            for t in temp:
                res = re.search('[A-Z]', t)
                if not res:
                    continue
                word,speech = t.split('_')
                words.append(word)
                speechs.append(speech)
            if words:
                s1 = ''.join(words)
                s2 = ' '.join(words)
                s3 = ' '.join(speechs)
                len_1.append(s1)
                len_2.append(s2)
                len_3.append(s3)
        for i in range(len(len_1)):
            result.append(len_1[i])
            result.append(len_2[i])
            result.append(len_3[i])
        df = pd.DataFrame(result)
        df.to_csv(txt, index=False, header=False, sep='t')

