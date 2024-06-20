import os

import xuejiedaima as daima
import pandas as pd

Walkinginnet_getwalking_path = daima.Walkinginnet_getwalking_path()

true_cixin, true_name = 0, 0
# 得分计算
for root_dir, sub_dir, files in os.walk(r"test"):
    for file in files:
        txt = root_dir + "/" + file
        df = pd.read_csv(txt, header=None, index_col=False, sep="\t")
        lst = df[0].tolist()
        A_lst_id = [x for x in range(len(lst)) if x % 3 == 0]
        B_lst_id = [x for x in range(len(lst)) if x % 3 == 1]
        C_lst_id = [x for x in range(len(lst)) if x % 3 == 2]
        A_lst, B_lst, C_lst = [], [], []
        for i in A_lst_id:
            A_lst.append(lst[i])
        for i in B_lst_id:
            B_lst.append(lst[i])
        for i in C_lst_id:
            C_lst.append(lst[i])
        for sentence_id, sentence in enumerate(A_lst):
            lensen = len(sentence)
            if lensen > 100:
                continue
            print(sentence)
            sent_allpath = Walkinginnet_getwalking_path.sent_walking_in_net(lensen, sentence)
            print(sent_allpath)
            if (sent_allpath == []):
                continue
            max_id, path_id = 0, 0
            max_sum = 0
            for path in sent_allpath:
                path_sum = 0
                for i in range(len(path) - 1):
                    node1 = node_matcher[path[i]]
                    node2 = node_matcher[path[i + 1]]
                    relationship = relationship_matcher.match((node1, node2)).first()
                    score = float(relationship.get('role'))
                    path_sum += score
                if path_sum > max_sum:
                    max_sum = path_sum
                    max_id = path_id
                path_id += 1
            aim_path = sent_allpath[max_id]
            # CRF.CRF_per()
            # if not sent_allpath:
            #     max_oov = 3
            #     sent_allpath = Walkinginnet_getwalking_path_oov.sent_walking_in_net(lensen, sentence, max_oov)
            # print(sent_allpath)
