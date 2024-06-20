import os
import re

import pandas as pd
import numpy as np
from ltp import LTP
import csv


header = ['sentence', 'segment', 'dep', 'seg', 'Pof_Tag']

ltp = LTP()

with open('SKN.csv', 'w', encoding='utf-8', newline='') as fp:
    writer = csv.writer(fp)
    writer.writerow(header)
    for root_dir, sub_dir, files in os.walk(r"train_SKN"):
        for file in files:
            txt = root_dir + "/" + file
            AKN_txt = 'train_AKN/' + file
            df_AKN = pd.read_csv(AKN_txt, header=None, index_col=False, sep="\t")
            df_SKN = pd.read_csv(txt, header=None, index_col=False, sep="\t")
            data_np_list = np.array(df_SKN)
            df_AKN = np.array(df_AKN)
            for i, sentence in enumerate(data_np_list):
                try:
                    dep_list = re.findall(r"[(](.*?)[)]", df_AKN[i][0])
                except:
                    print('fenci error')
                    continue
                try:
                    seg, hidden = ltp.seg(sentence.tolist())
                    sdp = ltp.sdp(hidden, mode='tree')
                    dep = ltp.dep(hidden)
                except:
                    print('LTP error')
                    continue
                data = [sentence, seg, dep, sdp, dep_list]
                writer.writerow(data)
