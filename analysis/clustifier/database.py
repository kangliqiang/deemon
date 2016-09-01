from py2neo import *
import sql_query_normalization as sqlnorm


def get_debug_connection():
    host = "localhost"
    user = "neo4j"
    pwd = "seesurf"
    return Graph(host=host, user=user, password=pwd)


def get_all_normalized_queries(graph):
    cursor = graph.run("MATCH (norm:NormalizedQuery) RETURN norm")
    normNodes = dict()
    while cursor.forward():
        normNodes[cursor.current()['norm']['hash']] = cursor.current()['norm']
    return normNodes
    

def normalize_sql_queries(graph):
    cursor = graph.run("MATCH (query:SQLQuery) RETURN query LIMIT 25")
    normalized_hash_nodes = get_all_normalized_queries(graph)
    while cursor.forward():
        hash = sqlnorm.generate_normalized_query_hash(cursor.current()['query']['ts'])
        if not hash in normalized_hash_nodes:            
            print "create new hash node {}".format(hash)
            normalizedQuery = Node("NormalizedQuery", hash=hash)
            normalized_hash_nodes[hash] = normalizedQuery
            graph.create(normalizedQuery)
        print "adding relationship for query {} to {}".format(cursor.current()['query'],normalized_hash_nodes[hash])
        print(type(normalized_hash_nodes[hash]))
        normalizesto = Relationship(cursor.current()['query'], 'NORMALIZESTO', normalized_hash_nodes[hash])
        graph.create(normalizesto)
        


def testing():
    normalize_sql_queries(get_debug_connection())


testing()
