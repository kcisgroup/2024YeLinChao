from py2neo import Graph, NodeMatcher, RelationshipMatcher

url = 'http://localhost:7474'
usr = 'neo4j'
key = '123456'
graph = Graph(url, auth=(usr, key))

'''约简后的'''
Node_label = 'words_nolabels'
Rel_label = 'score_nolabels'
node_matcher = NodeMatcher(graph)
relationship_matcher = RelationshipMatcher(graph)


def search_word_in_net(ngramwords):
    nodes = node_matcher.match(Node_label, name=ngramwords)
    if nodes:
        return True
    return False


def search_relation_in_net(ngramwords1, ngramwords2):
    node1 = node_matcher.match('words_nolabels', name=ngramwords1).first()
    node2 = node_matcher.match('words_nolabels', name=ngramwords2).first()
    if (not node2) or (not node1):
        return False
    rel = list(relationship_matcher.match([node1, node2], r_type='score_nolabels'))
    if rel:
        return True
    return False


def search_in_net(ngramwords):
    x = graph.run('match(n:{0}) where n.name="{1}" return id(n) LIMIT 1'.format(Node_label, ngramwords)).data()
    if x:
        return [i['id(n)'] for i in x]


def search_in_net2(id, ngramwords2):
    x = graph.run('match(n:{0})-[r:{1}]->(m:{2}) where id(n)={3} and m.name="{4}" return id(m) LIMIT 1'.
                  format(Node_label, Rel_label, Node_label, id, ngramwords2)).data()
    if x:
        return [i['id(m)'] for i in x]
    else:
        return []


class Walkinginnet_getwalking_path_OOV:
    def __init__(self):
        None

    def sentback(self, path_word, b_word, currentlo, sentence, lensen, oov_num, max_oov):
        fflag = 0
        ppath = []
        for ngram2 in range(currentlo, currentlo + 5):
            ngramwords2 = sentence[currentlo:ngram2 + 1]
            rela_net = search_relation_in_net(b_word, ngramwords2)
            if not rela_net:
                oov_num += 1
            if oov_num > max_oov:
                break
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
            word_in_net = search_word_in_net(ngramwords)
            path_word = [[ngramwords]]
            if not word_in_net:
                oov_num = + 1
            path_i, flag = self.sentback(path_word, ngramwords, currentlo, sentence, lensen, oov_num, max_oov)
            if flag:
                for p in path_i:
                    sent_allpath.append(p)

        return sent_allpath


class Walkinginnet_getwalking_path:
    def __init__(self):
        None

    def sentback(self, path_i, id, currentlo, sentence, lensen):
        fflag = 0
        ppath = []
        for ngram2 in range(currentlo, currentlo + 4):
            ngramwords2 = sentence[currentlo:ngram2 + 1]
            idm = search_in_net2(id, ngramwords2)
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
        for ngram in range(4):
            ngramwords = sentence[0:ngram + 1]
            currentlo = ngram + 1
            roadid = search_in_net(ngramwords)  # [7809, 46735]
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
