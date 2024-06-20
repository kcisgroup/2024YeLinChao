import networkx as nx
from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
import matplotlib.pyplot as plt

import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

def graph_from_cypher(data):
    G = nx.MultiDiGraph()

    def add_node(node):
        # Adds node id it hasn't already been added
        u = node.identity
        if G.has_node(u):
            return
        G.add_node(u, labels=node, properties=dict(node))

    def add_edge(relation):
        # Adds edge if it hasn't already been added.
        # Make sure the nodes at both ends are created
        for node in (relation.start_node, relation.end_node):
            add_node(node)
        # Check if edge already exists
        u = relation.start_node.identity
        v = relation.end_node.identity
        eid = relation.identity
        if G.has_edge(u, v, key=eid):
            return
        # If not, create it
        G.add_edge(u, v, key=eid, properties=dict(relation))

    for entry in data.all():
        # Parse node
        if isinstance(entry, Node):
            add_node(entry)

        # Parse link
        elif isinstance(entry, Relationship):
            add_edge(entry)
        else:
            raise TypeError("Unrecognized object")
    return G


url = 'http://localhost:7474'
usr, key = 'neo4j', '123456'
graph = Graph(url, auth=(usr, key))
node_matcher = NodeMatcher(graph)
relationship_matcher = RelationshipMatcher(graph)

rel = relationship_matcher.match([], r_type='score_nolabels')
test = graph_from_cypher(rel)
print(test.edges)
nx.draw_networkx(test)
plt.show()
# return G
# print(rel)
#
# g = graph_from_cypher(relationship_matcher.data())
# print(g)
