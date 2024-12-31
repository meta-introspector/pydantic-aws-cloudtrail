import yaml
#from pydantic import BaseModel
import json_schema.model as model
import json_schema.meta as model2
from datamodel_code_generator import DataModelType, InputFileType, generate
import networkx as nx

import networkx as nx

def create_clusters_with_depth(graph, depth, max_size):
    """
    Creates clusters of nodes with a depth around each node, ensuring clusters are within the max size.

    Args:
        graph (nx.DiGraph): The directed graph.
        depth (int): The depth to explore around each node.
        max_size (int): The maximum size of each cluster.

    Returns:
        list[nx.DiGraph]: A list of clusters as subgraphs.
    """
    visited = set()
    clusters = []

    for node in graph.nodes():
        if node in visited:
            continue
        
        # Use BFS to get nodes within the depth
        cluster_nodes = set()
        queue = [(node, 0)]
        
        while queue:
            current_node, current_depth = queue.pop(0)
            if current_node in cluster_nodes or current_depth > depth:
                continue
            
            cluster_nodes.add(current_node)
            if len(cluster_nodes) >= max_size:
                break
            
            for neighbor in graph.successors(current_node):
                if neighbor not in cluster_nodes:
                    queue.append((neighbor, current_depth + 1))
            for neighbor in graph.predecessors(current_node):
                if neighbor not in cluster_nodes:
                    queue.append((neighbor, current_depth + 1))
        
        # Mark nodes in this cluster as visited
        visited.update(cluster_nodes)
        
        # Add this cluster as a subgraph
        clusters.append(graph.subgraph(cluster_nodes).copy())

    return clusters

def main():

    print_json_schema()

def extract(x):
    if isinstance (x, str):
        yield x
        for p in x.split("/"):
            yield p
    elif isinstance (x, int):
        yield x
    elif isinstance (x, list):
        for i,j in enumerate(x):
            yield from extract(j)
            #print(i,j)
    elif isinstance (x, dict):
        for i in x:
            v = x[i]
            yield from extract(v)
            #print(i,x[i])
            
    else:
        yield("unknown {x}")
    
            
def print_json_schema():
    for m,mod in enumerate([model, model2]):
        schema = mod.Model.model_json_schema()
        #print(schema)
        G = nx.DiGraph()
        
        for defi in schema['$defs']:
            def1 = schema['$defs'][defi]
            refs = set([x for x in extract(def1) if x in schema['$defs']])

            for x in extract(def1) :
                if x in schema['$defs']:
                    if x != defi:
                        G.add_edge(defi, x)
            #deps[defi] = refs
        clusters = create_clusters_with_depth(G, depth=5, max_size=10)


        # Review each cluster
        for i, cluster in enumerate(clusters):
            print(f"Cluster {i+1}:")
            print(f"Nodes: {cluster.nodes()}")
            for x in cluster.nodes():
                s= schema['$defs'][x]
                print("Node",x,s)
            print(f"Edges: {cluster.edges()}")
            print()
    
        #T = nx.dfs_tree(G, depth_limit=10)
        #print(T)
        #nx.write_gml(T, f"model{m}.dot")
        
            #print(defi, schema['$defs'][defi])
        # now lets get all the deps recursivly.
        
        # result = generate(schema,
        #               disable_timestamp=True,
        #               enable_version_header = False,
        #               input_file_type=InputFileType.Dict,
        #               input_filename=None,
        #               #output=output_file,
        #               output_model_type=DataModelType.PydanticV2BaseModel,
        #               snake_case_field=True
        #               )
        #print(yaml.dump(schema))
        #print(result)
        


if __name__ == "__main__":
    print_json_schema()
    
