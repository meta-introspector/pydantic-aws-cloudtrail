import yaml
#from pydantic import BaseModel
import json_schema.model as model
import json_schema.meta as model2
from datamodel_code_generator import DataModelType, InputFileType, generate
from introspector.graph import build_cluster_graph, create_clusters_with_depth
import networkx as nx
from pathlib import Path

def generate_expanded_prelude(framework="Pydantic", goal="Meta-model of JSON Schema"):
    """
        clusters (list[nx.DiGraph]): The list of clusters (subgraphs).
        inbound_edges (dict): Inbound edges for each cluster.
        framework (str): Framework being used (default: "Pydantic").
        goal (str): The purpose or goal of the project (default: "Meta-model of JSON Schema").

    Returns:
        list[str]: A list of expanded preludes for each cluster.
    """
    prelude = f"""Purpose:
This cluster represents a localized subgraph of the JSON Schema. The nodes are schema components, modeled using {framework}, 
and the edges indicate the relationships (e.g., references, containment) between these components. The goal is to construct 
a meta-model of the JSON Schema for deeper analysis, validation, or transformation.

    Your task is to reflect over this chunk, first of all, what could we rename to make it more clear, how can we improve the names of the variables and why. How would you visualize this data structure? How would you allow the user to edit this data?
"""
    return prelude

# "Purpose:
# This cluster represents a localized subgraph of the JSON Schema. The nodes are schema components, modeled using {framework}, 
# and the edges indicate the relationships (e.g., references, containment) between these components. The goal is to construct 
# a meta-model of the JSON Schema for deeper analysis, validation, or transformation.
# """


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

        ## COLLECT AND POPULATE GRAPH
        for defi in schema['$defs']:
            def1 = schema['$defs'][defi]
            refs = set([x for x in extract(def1) if x in schema['$defs']])
            for x in extract(def1) :
                if x in schema['$defs']:
                    if x != defi:
                        G.add_edge(defi, x)

        ## Report on graph
        clusters = create_clusters_with_depth(G, depth=4, max_size=8)
        # Build the cluster graph
        cluster_graph, inbound_edges = build_cluster_graph(G, clusters)
        # Review each cluster

        output_path = "output/"
        Path(output_path).mkdir(exist_ok=True)
        for i, cluster in enumerate(clusters):
            with open(f"{output_path}/cluster{i}.txt","w") as fo:
                print(generate_expanded_prelude(framework="Pydantic", goal="Meta-model of JSON Schema"),file=fo)
                print(f"Cluster {i+1}:",file=fo)
                print(f"Nodes: {cluster.nodes()}",file=fo)            
                for x in cluster.nodes():
                    s= schema['$defs'][x]
                    print("Node",x,"SCHEMA:",file=fo)
                    print(yaml.dump(s).replace("\n","\n    "),file=fo)
                print(f"Edges: {cluster.edges()}",file=fo)
                print(f"Inbound Edges: {inbound_edges[i]}",file=fo)
            
        # Display meta-graph of clusters
        #print("Meta-Graph of Clusters:")
        #print(f"Nodes: {cluster_graph.nodes()}")
        #print(f"Edges: {cluster_graph.edges()}")
        
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
    
