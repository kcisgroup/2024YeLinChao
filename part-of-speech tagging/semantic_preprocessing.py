import csv
import re
import pandas as pd

head_row = pd.read_csv('CSV/SKN.csv', nrows=0)
head_row_list = list(head_row)
csv_result = pd.read_csv('CSV/SKN.csv', usecols=head_row_list)
row_list = csv_result.values.tolist()
header = ['word', 'dep', 'seg', 'Pof_Tag']
with open('SKN_word.csv', 'w', encoding='utf-8', newline='') as fp:
    writer = csv.writer(fp)
    writer.writerow(header)
    for row in row_list:
        word_list = re.findall(r"['](.*?)[']", row[1])
        dep_list = re.findall(r"[(](.*?)[)]", row[2])
        seg_list = re.findall(r"[(](.*?)[)]", row[3])
        tag_list = re.findall(r"['](.*?)[']", row[4])
        for i, res in enumerate(dep_list):
            try:
                word_index = seg_list[i].split(',')[0]
                rel_word_index = seg_list[i].split(',')[1]
                if int(rel_word_index) == 0:
                    rel_word_index = word_index
                word = word_list[int(word_index) - 1]
                rel_word = word_list[int(rel_word_index) - 1]
                word_dep = re.findall(r"['](.*?)[']", res.split(',')[2])[0]
                word_seg = re.findall(r"['](.*?)[']", seg_list[i].split(',')[2])[0]
                data = [word, word_dep, word_seg,tag_list[i]]
                writer.writerow(data)
            except:
                continue
