import os

import numpy as np
import pandas as pd
from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher



class Walkinginnet_getwalking_path:
    def __init__(self):
        None


    def search_in_net(self,ngramwords):
        x = graph.run('match(n:{0}) where n.name="{1}" return id(n)'.format(Nodelabel, ngramwords)).data()
        if x:
            return [i['id(n)'] for i in x]


    def search_in_net2(self,id, ngramwords2):
        x = graph.run('match(n:{0})-[r:{1}]->(m:{2}) where id(n)={3} and m.name="{4}" return id(m)'.
                      format(Nodelabel, Rellabel, Nodelabel, id, ngramwords2)).data()
        if x:
            return [i['id(m)'] for i in x]
        else:
            return []

    def sentback(self, path_i, id, currentlo, sentence, lensen):
        fflag = 0
        ppath = []
        for ngram2 in range(currentlo, lensen):
            ngramwords2 = sentence[currentlo:ngram2 + 1]
            idm = self.search_in_net2(id, ngramwords2)
            if idm:
                if ngram2 != lensen - 1:
                    for idx in idm:
                        path_i_ = [[idx]]
                        path_i_, flag = self.sentback(path_i_, idx, ngram2 + 1, sentence, lensen)
                        if flag:
                            fflag = 1
                            for everypath in path_i:
                                for pp in path_i_:
                                    newpa = everypath + pp
                                    ppath.append(newpa)
                else:
                    fflag = 1
                    for everypath in path_i:
                        for iddx in idm:
                            newpa = everypath + [iddx]
                            ppath.append(newpa)
        path_i = ppath
        return path_i, fflag

    def sent_walking_in_net(self, lensen, sentence):
        sent_allpath = []
        for ngram in range(lensen):
            ngramwords = sentence[0:ngram + 1]
            currentlo = ngram + 1
            roadid = self.search_in_net(ngramwords)  # [7809, 46735]
            if roadid:
                for id in roadid:
                    path_i = [[id]]
                    path_i, flag = self.sentback(path_i, id, currentlo, sentence, lensen)
                    if flag:
                        for p in path_i:
                            sent_allpath.append(p)
        '''
        for path in sent_allpath:
            print(path)'''
        return sent_allpath

def read_text(txt):
    df = pd.read_csv(txt, header=None, index_col=False, sep="\t")
    df1 = df.drop(df[df.index % 3 != 0].index)
    df2 = df.drop(df[df.index % 3 != 1].index)
    df3 = df.drop(df[df.index % 3 != 2].index)
    lst1 = list(df1[0])
    lst2 = list(df2[0])
    lst3 = list(df2[0])
    return lst1, lst2, lst3


if __name__ == "__main__":
    url = 'http://localhost:7474'
    usr,key = 'neo4j','123456'
    graph = Graph(url, auth=(usr, key))
    Nodelabel,Rellabel = 'words','score'

    node_matcher = NodeMatcher(graph)
    relationship_matcher = RelationshipMatcher(graph)
    Walkinginnet_getwalking_path = Walkinginnet_getwalking_path()

    sum_words = 0
    true_cixin,true_words = 0,0

    for root_dir, sub_dir, files in os.walk(r"test"):
        for file in files:
            txt = root_dir + "/" + file
            lst1, lst2, lst3 = read_text(txt)

            for lst1_index in range(len(lst1)):
                print(lst1[lst1_index])
                sum_words += 1
                lensen = len(lst1[lst1_index])
                sent_allpath = Walkinginnet_getwalking_path.sent_walking_in_net(lensen, lst1[lst1_index])
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
                node_cixin, node_name = [], []
                for i in aim_path:
                    node_cixin.append(node_matcher[i].get('cixin'))
                    node_name.append(node_matcher[i].get('name'))
                aim_cixin = ' '.join(node_cixin)
                aim_name = ' '.join(node_name)
                if aim_cixin == true_cixin:
                    true_cixin += 1
                if aim_name == true_words:
                    true_words += 1
