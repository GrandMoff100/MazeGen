import networkx as nx


__all__ = (
    "Maze",
    "space_to_wall_graph",
)

def space_to_wall_graph(
    spaces_wide: int, spaces_high: int, spaces_graph: nx.Graph
) -> nx.Graph:
    """Construct the dual graph of the maze spaces graph and negate it. Edges will then represent the maze walls."""

    wall_graph = nx.Graph()

    # Start with all walls up
    for i in range(spaces_wide + 1):
        for j in range(spaces_high + 1):
            wall_graph.add_node((i, j))
    wall_graph.add_edge((spaces_wide, spaces_high), (spaces_wide, spaces_high - 1))
    wall_graph.add_edge((spaces_wide, spaces_high), (spaces_wide - 1, spaces_high))

    for i in range(spaces_wide + 1):
        for j in range(spaces_high + 1):
            if i < spaces_wide:
                wall_graph.add_edge((i, j), (i + 1, j))
            if j < spaces_high:
                wall_graph.add_edge((i, j), (i, j + 1))

    # Subtract the walls that correspond to the edges in the space graph
    # remember that an edge in the space graph is a non-wall in the wall graph
    for edge in spaces_graph.edges:
        smaller, larger = sorted(edge)

        if smaller[0] == larger[0]:
            wall_graph.remove_edge(larger, (larger[0] + 1, larger[1]))
        elif smaller[1] == larger[1]:
            wall_graph.remove_edge(larger, (larger[0], larger[1] + 1))

    return wall_graph


class Maze:
    """The maze grid class."""

    def __init__(
        self,
        spaces_wide: int,
        spaces_high: int,
        spaces_graph: nx.Graph | None = None,
    ):
        """
        :param spaces_wide: The number of spaces wide the maze is.
        :param spaces_high: The number of spaces high the maze is.
        :param start: The start coordinate of the maze.
        :param end: The end coordinate of the maze.
        :param default_graph: The default graph to use for the maze. Edges correspond to non-walls. Vertices correspond to spaces.
        """

        self.spaces_wide = spaces_wide
        self.spaces_high = spaces_high

        self._graph: nx.Graph = spaces_graph # represents the spaces


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    maze = Maze(10, 10)

    # draw the graph with the node labels as coordinates
    nx.draw((graph := maze._graph), pos={node: node for node in graph.nodes})
    plt.show()
