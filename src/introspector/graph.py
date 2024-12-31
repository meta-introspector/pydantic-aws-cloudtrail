import networkx as nx

def build_cluster_graph(graph, clusters):
    """
    Constructs a graph of clusters and includes inbound edges for each cluster.

    Args:
        graph (nx.DiGraph): The original directed graph.
        clusters (list[nx.DiGraph]): The list of clusters (subgraphs).

    Returns:
        tuple:
            - nx.DiGraph: The meta-graph of clusters.
            - dict: A mapping of cluster indices to their inbound edges.
    """
    # Create the cluster meta-graph
    cluster_graph = nx.DiGraph()
    cluster_map = {node: i for i, cluster in enumerate(clusters) for node in cluster.nodes()}
    inbound_edges = {i: [] for i in range(len(clusters))}

    for i, cluster in enumerate(clusters):
        cluster_graph.add_node(i)  # Add cluster as a node in the meta-graph
        
        # Check all edges in the original graph
        for node in cluster.nodes():
            for pred in graph.predecessors(node):
                if pred not in cluster.nodes():  # Edge from outside the cluster
                    inbound_edges[i].append((pred, node))
                    pred_cluster = cluster_map.get(pred)
                    if pred_cluster is not None:
                        cluster_graph.add_edge(pred_cluster, i)

    return cluster_graph, inbound_edges

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
