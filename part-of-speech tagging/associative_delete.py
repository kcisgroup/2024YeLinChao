import csv
import os

import numpy as np
import pandas as pd
from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher

url = 'http://localhost:7474'
usr, key = 'neo4j', 'wo1252590285'
graph = Graph(url, auth=(usr, key))

node_matcher = NodeMatcher(graph)
relationship_matcher = RelationshipMatcher(graph)
b = graph.run(
            "match(n:words)-[r:score]->(nn:words) WHERE n.word_id = '{0}' RETURN r".format(0)).data()
graph.separate(b)