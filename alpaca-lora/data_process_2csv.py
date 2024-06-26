import csv
import re
import zh_core_web_trf
import pandas as pd
import os
from tqdm import tqdm

search_path = './data'
filePath = 'data.csv'
df = pd.read_csv('dict.csv', encoding='gb18030', header=None)
dict = df[0].values.tolist()

nlp = zh_core_web_trf.load(disable=['tagger', 'parser', 'ner'])
nlp.tokenizer.pkuseg_update_user_dict(dict)
with open(filePath, "w+") as f:
    writer = csv.writer(f)

    writer.writerow(['1', '2', '3'])
for root, dirs, files in os.walk(search_path):
    for file in files:
        print(file)
        res_input, res_output, res_mask_words = [], [], []
        file_name = os.path.join(root, file)
        with open(file_name, "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                if line.isspace():
                    line = f.readline()
                else:
                    print(line)
                    text_lines = re.split(r"[;。?]", line)
                    for text_line in text_lines:
                        fg_save = False
                        doc = nlp(text_line)
                        text = ''
                        mask_word = []
                        res_mask_word = []
                        for token in doc:
                            if token.text in dict:
                                fg_save = True
                                text = text + '[MASK]'
                                mask_word.append(token.text)
                                res_mask_word.append(token.text)
                            else:
                                text = text + token.text
                        if fg_save:
                            res_input.append(text)
                            res_output.append(text_line)
                            res_mask_words.append(res_mask_word)
                    line = f.readline()

        res = zip(res_input, res_output, res_mask_words)
        with open(filePath, "a+") as f:
            writer = csv.writer(f)
            for row in res:
                writer.writerow(row)
