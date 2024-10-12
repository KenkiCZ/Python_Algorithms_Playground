import json
from dijkstra_parts import *
from variables import *

def save_graph(graph):
    # Convert the graph to a dictionary
    graph_data = {
        'nodes': [node.to_dict() for node in graph.nodes],
        'edges': [edge.to_dict() for edge in graph.edges]
    }
    
    # Save the graph data to a JSON file
    with open(SAVE_PATH, 'w') as f:
        json.dump(graph_data, f, indent=4)

    print("Graph saved to graph.json")


def load_graph(graph):

    graph.nodes.clear()
    graph.edges.clear()

    with open(LOAD_PATH, 'r') as f:
        graph_data = json.load(f)

    # Create a new Graph instance
    node_map = {}

    # Reconstruct nodes
    for node_data in graph_data['nodes']:
        node = Node(
            x=node_data['x'],
            y=node_data['y'],
            name=node_data['name']
        )
        node.root = node_data.get('root', False)
        node.radius = node_data.get('radius', NODE_RADIUS)
        node.value = node_data.get('value', 0)
        graph.add_node(node)
        node_map[node.name] = node

    # Reconstruct edges
    for edge_data in graph_data['edges']:
        start_node = node_map[edge_data['start']]
        end_node = node_map[edge_data['end']]
        edge = Edge(start=start_node, end=end_node)
        edge.value = edge_data.get('value', 1)
        graph.add_edge(edge)

    return graph

        