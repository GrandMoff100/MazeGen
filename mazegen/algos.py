import itertools
import random

import networkx as nx

from .maze import Maze


__all__ = (
    "MazeGenerationAlgorithm",
    "OriginWalk",
    "Backtracking",
    "BinaryTree",
)


def digraph_to_graph(digraph: nx.DiGraph) -> nx.Graph:
    """Convert a directed graph to an undirected graph (just removing the directedness of the edges and condensing resulting multi-edges)."""
    graph = nx.Graph()
    for node in digraph.nodes:
        graph.add_node(node)
    for edge in digraph.edges:
        graph.add_edge(*edge)
    return graph


class MazeGenerationAlgorithm:
    def __init__(self, spaces_wide: int, spaces_high: int):
        self.spaces_wide = spaces_wide
        self.spaces_high = spaces_high

    def generate(self) -> Maze:
        raise NotImplementedError("The generate method must be implemented.")


class OriginWalk(MazeGenerationAlgorithm):
    """Also known as origin shift, this algorithm starts with a tree (a graph without cycles) and moves the root of the directed graph around."""

    def __init__(self, spaces_wide: int, spaces_high: int, steps: int | None = None):
        super().__init__(spaces_wide, spaces_high)
        self.steps = steps or spaces_wide * spaces_high * 20

    def default_tree(self) -> tuple[nx.DiGraph, tuple[int, int]]:
        tree = nx.DiGraph()
        tree.add_node((0, 0))

        for i in range(1, self.spaces_wide):
            tree.add_node((i, 0))
            tree.add_edge((i, 0), (i - 1, 0))

        for i in range(self.spaces_wide):
            for j in range(1, self.spaces_high):
                tree.add_node((i, j))
                tree.add_edge((i, j), (i, j - 1))

        return tree, (0, 0)

    def generate(self) -> Maze:
        tree, root = self.default_tree()

        roots = [root]
        
        for _ in range(self.steps):
            x, y = roots[-1]  # get the current root
            next_root_possibilities = filter(
                lambda v: 0 <= v[0] < self.spaces_wide and 0 <= v[1] < self.spaces_high,
                {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)},
            )
            new_root = random.choice(
                list(next_root_possibilities)
            )  # choose a random neighbor to move to
            roots.append(new_root)
        

        for prev, new_root in zip(roots, roots[1:]):
            tree.add_edge(prev, new_root)

            # remove the new_roots pointer (it might not point to the root at all)
            x, y = new_root
            for neighbor in {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)}:
                try:
                    tree.remove_edge(new_root, neighbor)
                    break  # found it! we can stop now
                except nx.NetworkXError:
                    pass

        return Maze(
            self.spaces_wide, self.spaces_high, spaces_graph=digraph_to_graph(tree),
        )


class Backtracking(MazeGenerationAlgorithm):
    """A recursive backtracking algorithm for generating mazes."""

    def generate(self) -> Maze:
        maze: nx.Graph = nx.grid_2d_graph(self.spaces_wide, self.spaces_high)
        tree: nx.Graph = nx.Graph()
        tree.add_nodes_from(maze.nodes)
        
        def backtrack(node: tuple[int, int]):
            maze.nodes[node]["visited"] = True

            neighbors = list(maze.neighbors(node))
            random.shuffle(neighbors)

            for neighbor in neighbors:
                if "visited" not in maze.nodes[neighbor]:
                    tree.add_edge(node, neighbor)
                    backtrack(neighbor)

        backtrack((0, 0))

        return Maze(self.spaces_wide, self.spaces_high, spaces_graph=digraph_to_graph(tree))


class BinaryTree(MazeGenerationAlgorithm):
    """A binary tree maze generation algorithm."""

    def generate(self) -> Maze:
        maze: nx.Graph = nx.grid_2d_graph(self.spaces_wide, self.spaces_high)
        tree: nx.Graph = nx.Graph()
        tree.add_nodes_from(maze.nodes)

        for i, j in itertools.product(range(self.spaces_wide), range(self.spaces_high)):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                tree.add_edge((i, j), (i, j - 1))
            elif j == 0:
                tree.add_edge((i, j), (i - 1, j))
            else:
                tree.add_edge((i, j), random.choice([(i - 1, j), (i, j - 1)]))

        return Maze(self.spaces_wide, self.spaces_high, spaces_graph=tree)
