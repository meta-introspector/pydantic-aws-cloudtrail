import argparse
import yaml
import json_schema.model as model
import json_schema.meta as model2
from datamodel_code_generator import DataModelType, InputFileType, generate
from introspector.graph import build_cluster_graph, create_clusters_with_depth
import networkx as nx
from pathlib import Path
from jinja2 import Template
import subprocess

def generate_schema_entry_prelude(entry_name, framework="Pydantic", template_path=None):
    if template_path:
        with open(template_path) as file:
            template_content = file.read()
        template = Template(template_content)
    else:
        template_content = """
Purpose:
This schema entry '{{ entry_name }}' represents a component of the JSON Schema, modeled using {{ framework }}. It is part of a larger meta-model of the JSON Schema, which aims to facilitate deeper analysis, validation, or transformation.

Details:
- **Entry Name**: {{ entry_name }}
- **Framework**: {{ framework }}

Considerations:
- Reflect on the clarity and appropriateness of the naming.
- Visualize how this schema entry interacts with others.
- Identify potential improvements or refactoring needs.
- Create examples of how this might be used with others, think of use cases.
Testing and Validation:
- Ensure the schema entry is correctly modeled.
- Validate its relationships with other components.
"""
        template = Template(template_content)
    return template.render(entry_name=entry_name, framework=framework)

def generate_expanded_prelude(framework="Pydantic", goal="Meta-model of JSON Schema", template_path=None):
    if template_path:
        with open(template_path) as file:
            template_content = file.read()
        template = Template(template_content)
    else:
        template_content = """
Purpose:
This cluster represents a localized subgraph of the JSON Schema. The nodes are schema components, modeled using {{ framework }}, 
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
        template = Template(template_content)
    return template.render(framework=framework, goal=goal)

def extract(x):
    if isinstance(x, str):
        yield x
        for p in x.split("/"):
            yield p
    elif isinstance(x, int):
        yield x
    elif isinstance(x, list):
        for i, j in enumerate(x):
            yield from extract(j)
    elif isinstance(x, dict):
        for i in x:
            v = x[i]
            yield from extract(v)
    else:
        yield(f"unknown {x}")

def print_json_schema(output_path, framework, goal, entry_template_paths, prelude_template_paths, script_name):
    for m, mod in enumerate([model, model2]):
        schema = mod.Model.model_json_schema()
        G = nx.DiGraph()

        for defi in schema['$defs']:
            def1 = schema['$defs'][defi]
            refs = set([x for x in extract(def1) if x in schema['$defs']])
            for x in extract(def1):
                if x in schema['$defs']:
                    if x != defi:
                        G.add_edge(defi, x)

        clusters = create_clusters_with_depth(G, depth=4, max_size=8)
        cluster_graph, inbound_edges = build_cluster_graph(G, clusters)

        Path(output_path).mkdir(exist_ok=True)
        for i, cluster in enumerate(clusters):
            with open(f"{output_path}/cluster{i}.txt", "w") as fo:
                if prelude_template_paths:
                    for prelude_template_path in prelude_template_paths:
                        print(generate_expanded_prelude(framework=framework,
                                                        goal=goal, template_path=prelude_template_path), file=fo)
                else:
                    print(generate_expanded_prelude(
                        framework=framework, goal=goal), file=fo)                          
                          
                print(f"Cluster {i + 1}:", file=fo)
                print(f"Nodes: {cluster.nodes()}", file=fo)
                for x in cluster.nodes():
                    s = schema['$defs'][x]
                    if (entry_template_paths):
                        for entry_template_path in entry_template_paths:
                            print(generate_schema_entry_prelude(x,
                                                                framework=framework,
                                                                template_path=entry_template_path), file=fo)
                    else:
                        print(generate_schema_entry_prelude(x, framework=framework), file=fo)
                    print(yaml.dump(s).replace("\n", "\n    "), file=fo)
                print(f"Edges: {cluster.edges()}", file=fo)
                print(f"Inbound Edges: {inbound_edges[i]}", file=fo)

        # Execute another process on the output file in the background
        subprocess.Popen(['python', script_name, output_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    parser = argparse.ArgumentParser(description='Process JSON Schema and generate preludes.')
    parser.add_argument('--output_path', type=str, default='output/', help='Path to the output directory')
    parser.add_argument('--framework', type=str, default='Pydantic', help='Framework being used')
    parser.add_argument('--goal', type=str, default='Meta-model of JSON Schema', help='Purpose or goal of the project')
    parser.add_argument('--entry_template_paths', type=str, nargs='+', help='Paths to the entry template files')
    parser.add_argument('--prelude_template_paths', type=str, nargs='+', help='Paths to the prelude template files')
    parser.add_argument('--script_name', type=str, required=True, help='Name of the script to execute on the output files')

    args = parser.parse_args()

    print_json_schema(args.output_path, args.framework, args.goal, args.entry_template_paths, args.prelude_template_paths, args.script_name)
    
if __name__ == "__main__":
    main()
