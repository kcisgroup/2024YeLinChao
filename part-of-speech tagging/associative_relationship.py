import csv
from py2neo import Graph
from py2neo.matching import NodeMatcher, RelationshipMatcher

url = 'http://localhost:7474'
usr, key = 'neo4j', '123456'
graph = Graph(url, auth=(usr, key))

node_matcher = NodeMatcher(graph)
relationship_matcher = RelationshipMatcher(graph)

# f = open('relationship_ass4_no.csv', 'w', encoding='utf-8', newline='')
# csv_write = csv.writer(f)
# csv_write.writerow([':START_ID', 'role', ':END_ID', ':TYPE'])
# f.close()

dict_score = {}
for a_id in node_matcher:
    if a_id not in dict_score.keys():
        if a_id <= 108:
            continue
        a_b = graph.run(
            "match(n:words_nolabels)-[r:score_nolabels]->(nn:words_nolabels) WHERE n.word_id = '{0}' "
            "RETURN nn.word_id as word_id,r.role as score".format(a_id)).data()
        dict_score[a_id] = {}
        for node in iter(a_b):
            dict_score[a_id][node['word_id']] = round(float(node['score']), 4)
    a_b_score = dict_score[a_id]
    dict_ass = {}
    for b_node_id in a_b_score.keys():
        b_score = a_b_score[b_node_id]
        if b_score <= 0.3:
            continue
        if b_node_id not in dict_score.keys():
            b_c = graph.run(
                "match(n:words_nolabels)-[r:score_nolabels]->(nn:words_nolabels) WHERE n.word_id = '{0}' "
                "RETURN nn.word_id as word_id,r.role as score".format(b_node_id)).data()
            dict_score[b_node_id] = {}
            for node in iter(b_c):
                dict_score[b_node_id][node['word_id']] = round(float(node['score']), 4)
        b_c_score = dict_score[b_node_id]
        for c_id in b_c_score.keys():
            if b_score <= 0.3:
                continue
            if (c_id in a_b_score.keys()) or int(c_id) == int(a_id):
                continue
            cnode_score = round(float(b_c_score[c_id]), 4)
            if c_id in dict_ass.keys():
                dict_ass[c_id] = max(dict_ass[c_id], b_score * cnode_score * 0.7)
            else:
                dict_ass[c_id] = b_score * cnode_score * 0.7

    print("####" + str(a_id) + "####" + 'start write to csv' + '####')
    f = open('relationship_ass4_no.csv', 'a+', encoding='utf-8', newline='')
    csv_write = csv.writer(f)
    for c_id in dict_ass:
        if dict_ass[c_id] >= 0.2:
            csv_write.writerow(
                [a_id, round(dict_ass[c_id], 4), c_id, 'score_nolabels'])
    f.close()
    print("####" + str(a_id) + "####" + 'finish' + '####')
