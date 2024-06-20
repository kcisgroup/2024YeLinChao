from py2neo import Graph
from py2neo.matching import NodeMatcher, RelationshipMatcher
import numpy as np

url = 'http://localhost:7474'
usr = 'neo4j'
key = '123456'
graph = Graph(url, auth=(usr, key))
'''约简后的'''
Node_label = 'words_nolabels'
Rel_label = 'score_nolabels'


def search_score_in_net2(a_id, b_id):
    Node1_label = 'words'
    Rel1_label = 'score'
    x = graph.run('match(n:{0})-[r:{1}]->(m:{2}) where n.word_id = "{3}" and m.word_id = "{4}" return r.role'.
                  format(Node1_label, Rel1_label, Node1_label, a_id, b_id)).data()

    return x[0]['r.role'] if len(x) > 0 else 0


class Walkinginnet_getwalking_path_OOV:
    def __init__(self):
        None

    def search_word_in_net(self, ngramwords):
        nodes = node_matcher.match(Node_label, name=ngramwords)
        if nodes:
            return True
        return False

    def search_relation_in_net(self, ngramwords1, ngramwords2):
        node1 = node_matcher.match('words_nolabels', name=ngramwords1).first()
        node2 = node_matcher.match('words_nolabels', name=ngramwords2).first()
        if (not node2) or (not node1):
            return False
        rel = list(relationship_matcher.match([node1, node2], r_type='score_nolabels'))
        if rel:
            return True
        return False

    def sentback(self, path_word, b_word, currentlo, sentence, lensen, oov_num, max_oov):
        fflag = 0
        ppath = []
        for ngram2 in range(currentlo, currentlo + 5):
            ngramwords2 = sentence[currentlo:ngram2 + 1]
            rela_net = self.search_relation_in_net(b_word, ngramwords2)
            if not rela_net:
                oov_num += 1
            if ngram2 < lensen - 1:
                path_i_ = [[ngramwords2]]
                path_i_, flag = self.sentback(path_i_, ngramwords2, ngram2 + 1, sentence, lensen, oov_num, max_oov)
                if oov_num > max_oov:
                    break
                if flag:
                    fflag = 1
                    for everypath in path_word:
                        for pp in path_i_:
                            newpa = everypath + pp
                            ppath.append(newpa)
            elif ngram2 > lensen - 1:
                continue
            else:
                fflag = 1
                if oov_num > max_oov:
                    break
                for everypath in path_word:
                    newpa = everypath + [ngramwords2]
                    ppath.append(newpa)
        path_word = ppath

        return path_word, fflag

    def sent_walking_in_net(self, lensen, sentence, max_oov):
        sent_allpath = []
        for ngram in range(5):
            oov_num = 0
            ngramwords = sentence[0:ngram + 1]
            currentlo = ngram + 1
            word_in_net = self.search_word_in_net(ngramwords)
            path_word = [[ngramwords]]
            if not word_in_net:
                oov_num += 1
            path_i, flag = self.sentback(path_word, ngramwords, currentlo, sentence, lensen, oov_num, max_oov)
            if flag:
                for p in path_i:
                    sent_allpath.append(p)

        return sent_allpath


node_matcher = NodeMatcher(graph)
relationship_matcher = RelationshipMatcher(graph)
# Walkinginnet_getwalking_path_OOV = Walkinginnet_getwalking_path_OOV()
# sentence = '新华社德黑兰８月３１日电记者陈铭'
#
# lensen = len(sentence)
# max_oov = 3
#
# all_path = Walkinginnet_getwalking_path_OOV.sent_walking_in_net(lensen, sentence, max_oov)
# print(all_path)
def CRF_per(path):
    path_cixin = []
    path_id = []
    path_VW = []

    for i in path:
        node1 = node_matcher.get(i)
        rel = relationship_matcher.match([node1], r_type='probability')
        tmp_VW = []
        tmp_cixin = []
        tmp_id = []
        for re in iter(rel):
            tmp_cixin.append(re.end_node['cixin'])
            tmp_id.append(re.end_node['word_id'])
            tmp_VW.append(float(re['role']))
        path_id.append(tmp_id)
        path_VW.append(tmp_VW)
        path_cixin.append(tmp_cixin)
    max_len = 0
    for i in range(len(path_VW)):
        max_len = len(path_VW[i]) if (len(path_VW[i]) > max_len) else max_len
    VW = np.zeros((len(path), max_len))
    for i, j in enumerate(path_VW):
        VW[i, 0:len(j)] = j
    V = VW
    V[V > 0] = 1
    EW = np.zeros((len(path_VW), max_len, max_len))
    for len_a in range(len(path_id) - 1):
        for x, a_id in enumerate(path_id[len_a]):
            for y, b_id in enumerate(path_id[len_a + 1]):
                score = search_score_in_net2(a_id, b_id)
                EW[len_a][x][y] = score
    E = EW
    E[E > 0] = 1
    return V, VW, E, EW

