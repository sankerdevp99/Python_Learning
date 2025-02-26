import networkx as nx
import matplotlib.pyplot as plt

# connections = {(0, 1): 1, (1, 2): 0, (0, 3): 0, (1, 4): 1, (2, 5): 0, (3, 4): 1, (4, 5): 0, (6, 7): 1, (7, 8): 0, (9, 10): 1, (10, 11): 2, (1, 7): 1, (2, 5): 1}
# num_nodes_per_row = 3

connections = {}
num_nodes_per_row = None
row_labels = None

def main():
    G = nx.DiGraph()
    for edge, connection in connections.items():
        G.add_edge(*edge, weight=connection)

    pos = {node: (i % num_nodes_per_row, i // num_nodes_per_row) for i, node in enumerate(sorted(set().union(*connections.keys())))}

    # Draw nodes
    nx.draw_networkx_nodes(G, pos)

    # Draw directed edges as arcs for weight > 0 using nx.draw_networkx_edges
    edge_labels = nx.get_edge_attributes(G, 'weight')

    for edge, weight in edge_labels.items():
        if weight > 0:
            color = 'b' if weight == 1 else 'r'
            nx.draw_networkx_edges(G, pos, edgelist=[edge], connectionstyle=f"arc3,rad=-0.3" if weight == 1 else "arc3,rad=-0.3", edge_color=color, width=2)

    # Draw edge labels (weights) for weight > 0
    edge_labels_gt_0 = {edge: weight for edge, weight in edge_labels.items() if weight > 0}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_gt_0)

    # Draw node labels
    nx.draw_networkx_labels(G, pos)

    # Label every row
    
    for row, label in row_labels.items():
        plt.text(-3.0, row, label, fontsize=10, verticalalignment="center")

     # Label every column
    col_labels = {i % num_nodes_per_row: f't_{i % num_nodes_per_row + 1}' for i in range(len(pos))}
    for col, label in col_labels.items():
        plt.text(col, -0.5, label, fontsize=10, horizontalalignment="center")



    # Invert y-axis
    plt.gca().invert_yaxis()

    # Display the graph
    plt.axis('equal')

    plt.show()

# main()
