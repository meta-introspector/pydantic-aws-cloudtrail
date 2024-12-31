import yaml
#from pydantic import BaseModel
import json_schema.model as model
import json_schema.meta as model2
from datamodel_code_generator import DataModelType, InputFileType, generate
from introspector.graph import build_cluster_graph, create_clusters_with_depth
import networkx as nx
from pathlib import Path

def generate_schema_entry_prelude(entry_name, framework="Pydantic"):
    """
    Generate a prelude for a specific schema entry.

    Args:
        entry_name (str): The name of the schema entry.
        framework (str): The framework being used (default: "Pydantic").

    Returns:
        str: A prelude for the schema entry.
    """
    return f"""
Purpose:
This schema entry '{entry_name}' represents a component of the JSON Schema, modeled using {framework}. It is part of a larger meta-model of the JSON Schema, which aims to facilitate deeper analysis, validation, or transformation.

Details:
- **Entry Name**: {entry_name}
- **Framework**: {framework}

Considerations:
- Reflect on the clarity and appropriateness of the naming.
- Visualize how this schema entry interacts with others.
- Identify potential improvements or refactoring needs.
- Create examples of how this might be used with others, think of use cases.
Testing and Validation:
- Ensure the schema entry is correctly modeled.
- Validate its relationships with other components.
"""

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

Cluster Analysis:
1. **Rename to Improve Clarity**:
   - `Cluster 8` -> `JSONSchemaCluster`
   - `Nodes` -> `Components`

2. **Improve Variable Names**:
   - `Properties5` -> `PropertiesWithRoot`
   - `Root2` -> `TopLevelComponent`
   - `AnyOfItem4` -> `AnyOfSubComponent`
   
3. **Reasons for Naming Improvements**:
   - **Descriptive Naming**: The new names are more descriptive, making it clear what each component represents.
   - **Consistency**: Using a naming convention that follows the structure of the JSON Schema components.
   - **Clarity in Relationships**: The relationships (edges) between these components are clearer with improved naming.

Visualization and Editing:
To visualize this data structure, we can use a **Graphical Representation** such as a Directed Acyclic Graph (DAG). Here’s how it could look:

TopLevelComponent
  ├── PropertiesWithRoot
      └── Root2
          ├── anyOf
              └── AnyOfSubComponent
                  └── $ref: '#/$defs/AnyOfItem4'

Nodes represent the different components (`TopLevelComponent`, `PropertiesWithRoot`, etc.).
Edges represent the relationships between these components, such as containment or references.

User Interaction:
To allow the user to edit this data structure, we need a way to:

1. **Modify Properties**: Allow users to change properties of existing components.
2. **Add/Remove Components**: Enable adding new components and removing existing ones.
3. **Change Relationships**: Allow changes to the relationships between components.

Implementation Ideas:
- **GUI Interface**: Create a Graphical User Interface (GUI) using libraries like `Tkinter`, `PyQt`, or `PySimpleGUI`. This would allow users to visually edit the graph by dragging and dropping nodes.
- **Command-Line Interface (CLI)**: Develop a CLI tool using `argparse` or similar libraries. Users can interact with the data structure through commands like:
  - `add_node <node_type> <component_name>`
  - `remove_node <component_name>`
  - `change_property <component_name> <property_name> <new_value>`
  - `edit_edge <from_node> <to_node>` 
- **Web Interface**: Create a web-based interface using frameworks like `Flask` or `Django`. Users can interact with the data through a web browser, providing a more scalable and accessible solution.

Testing and Validation:
Adding a section on how to test and validate the changes and improvements could be beneficial.

User Feedback:
Consider discussing how user feedback will be collected and incorporated into future iterations of the data structure and interface.

Data Security:
Consider which values would need to be secured and encrypted.
"""
    return prelude


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
                    #print("Node",x,"SCHEMA:",file=fo)
                    print(generate_schema_entry_prelude(x), file=fo)
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
    
