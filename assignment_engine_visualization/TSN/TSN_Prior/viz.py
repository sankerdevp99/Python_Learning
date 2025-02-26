#!/usr/bin/env python3
import networkx as nx
import plotly.graph_objects as go
import numpy as np


# Your dictionary describing connections
# connections = {(0, 1): 1, (1, 2): 0, (0, 3): 0, (1, 4): 1, (2, 5): 0, (3, 4): 1, (4, 5): 0, (6, 7): 1, (7, 8): 0,
#                (9, 10): 1, (10, 11): 2, (1, 7): 1}
# num_nodes_per_row = 3
connections = {}
num_nodes_per_row = None
row_labels = None

def main():
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes and edges based on the dictionary
    for edge, connection in connections.items():
        if connection > 0:
            G.add_edge(*edge, weight=connection)

    # Extract node positions for rectangular layout with a limit of 3 nodes per row
    
    pos = {node: (i % num_nodes_per_row, i // num_nodes_per_row) for i, node in enumerate(sorted(set().union(*connections.keys())))}

    # Create edge trace
    edge_x = []
    edge_y = []
    mid_x = []
    mid_y = []
    edge_weights = []
    arrow_x = []
    arrow_y = []
   
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        xg, yg = pos[edge[1]]
        
        #draw the curves as lines with different sizes and angle based on direction in visualization
        arc_extension = 0.02*(abs(yg-y0))
        if x0 == xg and yg > xg:
            
            x1 = x0 + arc_extension
            y1 = y0 + arc_extension
            x2 = xg + arc_extension
            y2 = yg - arc_extension
            edge_x.extend([x0,x1,x2, xg, None])
            edge_y.extend([y0,y1,y2, yg, None])

            x_half = (x1 + x2) / 2
            y_half = (y1 + y2) / 2
            mid_x.extend([None,x_half,None])
            mid_y.extend([None,y_half,None])

            arrow_x.extend([x2,xg,None])
            arrow_y.extend([y2,yg,None])
        elif x0 == xg and yg < xg: 
            x1 = x0 + arc_extension
            y1 = y0 - arc_extension
            x2 = xg + arc_extension
            y2 = yg + arc_extension
            edge_x.extend([x0,x1,x2, xg, None])
            edge_y.extend([y0,y1,y2, yg, None])

            x_half = (x1 + x2) / 2
            y_half = (y1 + y2) / 2
            mid_x.extend([None,x_half,None])
            mid_y.extend([None,y_half,None])

            arrow_x.extend([x2,xg,None])
            arrow_y.extend([y2,yg,None])
        else:
            edge_x.extend([x0, xg, None])
            edge_y.extend([y0, yg, None])

            x_half = (x0 + xg) / 2
            y_half = (y0 + yg) / 2
            mid_x.extend([None,x_half,None])
            mid_y.extend([None,y_half,None])

            arrow_x.extend([x0 + 0.8 * (xg - x0),xg,None])
            arrow_y.extend([y0 + 0.8* (yg - y0),yg,None])

        
        
        edge_weights.extend([None,f"  {edge[2]['weight']}",None])

        #finding the point just before the end of the line for starting the arrow 
        # if x0 == xg:
        #     x_arr = xg
        #     y_arr = yg - 0.3
        # elif y0 == yg:
        #     y_arr = yg
        #     x_arr = xg - 0.2
        # else:
        #     #not possible
        #     x_arr = x0 + 0.8 * (xg - x0)
        #     y_arr = y0 + 0.8* (yg - y0)
        # arrow_x.extend([x_arr,xg,None])
        # arrow_y.extend([y_arr,yg,None])
        

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='black'),
        
        hoverinfo='none',
        mode='lines',  # Add 'text' mode to display edge labels
        # text=edge_weights,  # Set the text to be the edge weights
        # textposition='middle center',  # Set text position to the middle of the edges
    )
   
    edge_info =go.Scatter(x = mid_x, y=mid_y, mode='text', text=edge_weights ,textposition='top right',
                        textfont=dict(color='blue'),)
    
    edge_arrow =go.Scatter(x = arrow_x, y=arrow_y, mode='lines',line=dict(width= 3,color='red'),)


    # Create node trace
    node_x = []
    node_y = []
    node_text = []

    for node, (x, y) in pos.items():
        node_x.append(x)
        node_y.append(y)
        node_text.append(f'{node}')

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',  # Add 'text' mode to display node labels
        hoverinfo='text',
        text=node_text,  # Set the text to be the node labels
        marker=dict(size=10),
        textposition='bottom center',
    )
    
    # annotations for row name and column names
    annotations = []

    # Check if pos is not empty
    if pos:
        for row, label in row_labels.items():
            annotations.append(
                dict(
                    x=-2.0,
                    y=row,
                    xref='x',
                    yref='y',
                    text=label,
                    showarrow=False,
                    font=dict(color="black"),
                )
            )

        for col in range(0, max(pos.values(), key=lambda x: x[0])[0] + 1):
            annotations.append(
                dict(
                    x=col,
                    y=-0.8,
                    xref='x',
                    yref='y',
                    text=f't_{col + 1}',
                    showarrow=False,
                    font=dict(color="black"),
                )
            )

    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace, edge_info, edge_arrow],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        annotations=annotations,))

    # Show the figure

    fig.show()
   
# main()
