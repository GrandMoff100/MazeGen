import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import random
from mazegen import OriginWalk, space_to_wall_graph, Backtracking, BinaryTree, MazeGenerationAlgorithm

import networkx as nx

options: list[MazeGenerationAlgorithm] = [
    OriginWalk(30, 40),
    Backtracking(30, 40),
    BinaryTree(30, 40),
]


number = 500
with PdfPages("mazes.pdf") as pdf:
    for i in range(number):
        
        algo = random.choice(options)
        print(i + 1, "of", number, ":", algo.__class__.__name__)
        maze = algo.generate()

        graph = space_to_wall_graph(maze.spaces_wide, maze.spaces_high, maze._graph)
        graph.remove_edge((0, 0), (0, 1))  # remove the start wall
        graph.remove_edge(
            (maze.spaces_wide, maze.spaces_high),
            (maze.spaces_wide, maze.spaces_high - 1),
        )  # remove the end wall

        plt.figure(figsize=(maze.spaces_wide, maze.spaces_high))
        # draw the graph with the node labels as coordinates
        nx.draw_networkx_edges(
            graph,
            pos={node: node for node in graph.nodes},
            width=3,
        )
        plt.axis("equal")
        plt.box(False)
        plt.margins(0)  # configure the margins between the plot and the edge
        pdf.savefig(bbox_inches="tight")
        plt.close()
