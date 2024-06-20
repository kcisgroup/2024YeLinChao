import os
import pandas as pd
import csv
import numpy as np
from scipy.interpolate import interp1d



xp = [0, 1, 10]
fp = [0, 0.1, 1]
fx = interp1d(xp, fp)

dict_wordid = {}
id = 0
dict_relationship = {}

for root_dir, sub_dir, files in os.walk(r"train_AKN"):
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
        # 节点
        for words in words_list:
            len_words = len(words)
            for i in range(len_words):
                word_i = words[i].split('(')[0]

                if not word_i:
                    continue
                if word_i not in dict_wordid.keys():
                    dict_wordid[word_i] = id
                    id += 1
                word_id_i = dict_wordid[word_i]
                if word_id_i not in dict_relationship.keys():
                    dict_relationship[word_id_i] = {}
                # 滑动窗口 固定为7
                j_len = i + 7 if (i + 7) <= len_words else len_words
                for j in range(i + 1, j_len):
                    value = 1 / (j - i)
                    word_j = words[j].split('(')[0]
                    if not word_j:
                        continue
                    if word_i == word_j:
                        continue
                    # id
                    if word_j not in dict_wordid.keys():
                        dict_wordid[word_j] = id
                        id += 1
                    word_id_j = dict_wordid[word_j]
                    if word_id_j not in dict_relationship[word_id_i].keys():
                        dict_relationship[word_id_i][word_id_j] = value
                    else:
                        dict_relationship[word_id_i][word_id_j] += value
print('add2dict_finish')
f = open('word_nolabels.csv', 'w', encoding='utf-8', newline='')
csv_write = csv.writer(f)
csv_write.writerow(['word_id:ID', 'name', ':LABEL'])
for temp in dict_wordid:
    csv_write.writerow([dict_wordid[temp], temp, 'words_nolabels'])
f.close()
f = open('relationship_nolabels.csv', 'w', encoding='utf-8', newline='')
csv_write = csv.writer(f)
csv_write.writerow([':START_ID', 'role', ':END_ID', ':TYPE'])
for start_id in dict_relationship:
    for end_id in dict_relationship[start_id]:
        if dict_relationship[start_id][end_id] < 1:
            continue
        if dict_relationship[start_id][end_id] > 10:
            dict_relationship[start_id][end_id] = 10
        csv_write.writerow([start_id, fx(dict_relationship[start_id][end_id]), end_id, 'score_nolabels'])
f.close()

