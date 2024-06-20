import numpy as np
from py2neo import Graph, NodeMatcher, RelationshipMatcher

url = 'http://localhost:7474'
usr = 'neo4j'
key = '123456'
graph = Graph(url, auth=(usr, key))
node_matcher = NodeMatcher(graph)
relationship_matcher = RelationshipMatcher(graph)


def search_score_in_net2(a_id, b_id):
    Node1_label = 'words'
    Rel1_label = 'score'
    x = graph.run('match(n:{0})-[r:{1}]->(m:{2}) where n.word_id = "{3}" and m.word_id = "{4}" return r.role'.
                  format(Node1_label, Rel1_label, Node1_label, a_id, b_id)).data()

    return x[0]['r.role'] if len(x) > 0 else 0


def CRF_per(path):
    url = 'http://localhost:7474'
    usr = 'neo4j'
    key = '123456'
    graph = Graph(url, auth=(usr, key))
    '''约简后的'''
    Node_label = 'words_nolabels'
    Rel_label = 'score_nolabels'

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



class CRF(object):
    """
    实现条件随机场预测问题的维特比算法
    """

    def __init__(self, V, VW, E, EW):
        """
        :param V:是定义在节点上的特征函数，称为状态特征
        :param VW:是V对应的权值
        :param E:是定义在边上的特征函数，称为转移特征
        :param EW:是E对应的权值
        """
        self.V = V  # 点分布表
        self.VW = VW  # 点权值表
        self.E = E  # 边分布表
        self.EW = EW  # 边权值表
        self.D = []  # Delta表，最大非规范化概率的局部状态路径概率
        self.P = []  # Psi表，当前状态和最优前导状态的索引表s
        self.BP = []  # BestPath，最优路径
        return


    def Viterbi(self):
        """
        条件随机场预测问题的维特比算法，此算法一定要结合CRF参数化形式对应的状态路径图来理解，更容易理解.
        """
        self.D = np.full(shape=(np.shape(self.V)), fill_value=.0)
        self.P = np.full(shape=(np.shape(self.V)), fill_value=.0)
        for i in range(np.shape(self.V)[0]):
            # 初始化
            if 0 == i:
                self.D[i] = np.multiply(self.V[i], self.VW[i])
                self.P[i] = np.array([0, 0])
                pass
            # 递推求解布局最优状态路径
            else:
                for y in range(np.shape(self.V)[1]):  # delta[i][y=1,2...]
                    for l in range(np.shape(self.V)[1]):  # V[i-1][l=1,2...]
                        delta = 0.0
                        delta += self.D[i - 1, l]  # 前导状态的最优状态路径的概率
                        delta += self.E[i - 1][l, y] * self.EW[i - 1][l, y]  # 前导状态到当前状体的转移概率
                        delta += self.V[i, y] * self.VW[i, y]  # 当前状态的概率
                        if 0 == l or delta > self.D[i, y]:
                            self.D[i, y] = delta
                            self.P[i, y] = l

        # 返回，得到所有的最优前导状态
        N = np.shape(self.V)[0]
        self.BP = np.full(shape=(N,), fill_value=0.0)
        t_range = -1 * np.array(sorted(-1 * np.arange(N)))
        for t in t_range:
            if N - 1 == t:  # 得到最优状态
                self.BP[t] = np.argmax(self.D[-1])
            else:  # 得到最优前导状态
                self.BP[t] = self.P[t + 1, int(self.BP[t + 1])]

        # 最优状态路径表现在存储的是状态的下标，我们执行存储值+1转换成示例中的状态值
        # 也可以不用转换，只要你能理解，self.BP中存储的0是状态1就可以~~~~
        self.BP += 1
        return self.BP

# if __name__ == '__main__':
#     V = np.array([[1, 1],  # X1:S(Y1=1), S(Y1=2)
#                   [1, 1],  # X2:S(Y2=1), S(Y2=2)
#                   [1, 1],
#                   [1, 0]])  # X3:S(Y3=1), S(Y3=1)
#     VW = np.array([[1.0, 0.5],  # X1:SW(Y1=1), SW(Y1=2)
#                    [0.8, 0.5],  # X2:SW(Y2=1), SW(Y2=2)
#                    [0.8, 0.5],
#                    [1.0, 0]])  # X3:SW(Y3=1), SW(Y3=1)
#     E = np.array([[[1, 1],  # Edge:Y1=1--->(Y2=1, Y2=2)
#                    [1, 0]],  # Edge:Y1=2--->(Y2=1, Y2=2)
#                   [[0, 1],  # Edge:Y2=1--->(Y3=1, Y3=2)
#                    [1, 1]],
#                   [[1, 1],  # Edge:Y2=1--->(Y3=1, Y3=2)
#                    [0, 0]]
#                   ])  # Edge:Y2=2--->(Y3=1, Y3=2)
#     EW = np.array([[[0.6, 1],  # EdgeW:Y1=1--->(Y2=1, Y2=2)
#                     [1, 0.0]],  # EdgeW:Y1=2--->(Y2=1, Y2=2)
#                    [[0.0, 1],  # EdgeW:Y2=1--->(Y3=1, Y3=2)
#                     [1, 0.2]],
#                    [[0.9, 0],  # EdgeW:Y2=1--->(Y3=1, Y3=2)
#                     [0.7, 0]]
#                    ])  # EdgeW:Y2=2--->(Y3=1, Y3=2)
#
#     crf = CRF(V, VW, E, EW)
#     ret = crf.Viterbi()
#     print('最优状态路径为:', ret)
