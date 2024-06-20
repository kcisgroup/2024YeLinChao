import csv
import os

import pandas as pd

head_row = pd.read_csv('word_nolabels.csv', nrows=0)
head_row_list = list(head_row)
# print(head_row)
csv_result = pd.read_csv('word_nolabels.csv', usecols=head_row_list)
row_list = csv_result.values.tolist()
# print(f"行读取结果：{row_list}")
dic_word = {}
for word in row_list:
    dic_temp = {'id': word[0],'cixin':{},'total':0}
    dic_word[word[1]] = dic_temp


head_row = pd.read_csv('word.csv', nrows=0)
head_row_list = list(head_row)
# print(head_row)
csv_result = pd.read_csv('word.csv', usecols=head_row_list)
row_list = csv_result.values.tolist()
for word in row_list:
    if word[1] not in dic_word.keys():
        continue
    dic_word[word[1]]['cixin'][word[2]] = {'id':word[0],'num':0}
for root_dir, sub_dir, files in os.walk(r"train_SKN"):
    for file in files:
        txt = root_dir + "/" + file
        df = pd.read_csv(txt, header=None, index_col=False, sep="\t")
        lst = df[0].tolist()
        words_list = []
        for l in lst:
            temp = l.split(',')
            words_list.append(temp)
        for words in words_list:
            for word in words:
                if len(word) <= 3:
                    words.remove(word)
        for lst in words_list:
            for words in lst:
                try:
                    word, cixin = words.split('(')
                    cixin = cixin.replace(')', '')
                except:
                    word = words
                    cixin = 'error'
                error_cixin = ['PU','error']
                if cixin in error_cixin:
                    continue
                if not dic_word[word]['cixin']:
                    continue
                dic_word[word]['cixin'][cixin]['num'] += 1
                dic_word[word]['total'] += 1
print(dic_word)

f = open('probability.csv', 'w', encoding='utf-8', newline='')
csv_write = csv.writer(f)
csv_write.writerow([':START_ID', 'role', ':END_ID', ':TYPE'])

for word_key, word_value in dic_word.items():
    for cixin_key, cixin_value in word_value['cixin'].items():
        score = round(cixin_value['num'] / word_value['total'],4)
        csv_write.writerow([word_value['id'], score, cixin_value['id'], 'probability'])
