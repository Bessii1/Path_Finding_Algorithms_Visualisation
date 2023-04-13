from random import random


class Grid:
    def __init__(self, columns, rows, tile, inspect_diagonals=True):
        self.inspect_diagonals = inspect_diagonals
        self.columns = columns
        self.rows = rows
        self.tile = tile
        self.grid = [[1 if random() < 0.2 else 0 for col in range(self.columns)] for row in range(self.rows)]

    # draw a cell in the grid according to the specified size of our grid(window)
    def get_rect(self, x, y):
        return x * self.tile + 1, y * self.tile + 1, self.tile - 2, self.tile - 2

    def get_graph(self):
        graph = {}
        grid = self.grid
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                if not col:
                    graph[(x, y)] = graph.get((x, y), []) + self.__get_next_nodes(x, y)

        return graph

    # determine which are the neighbor cells of the x, y cell
    def __get_next_nodes(self, x, y):
        if self.inspect_diagonals:
            ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        else:
            ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        neighbor_nodes = lambda x, y: True if 0 <= x < self.columns and 0 <= y < self.rows and not self.grid[y][x] else False
        return [(x + dx, y + dy) for dx, dy in ways if neighbor_nodes(x + dx, y + dy)]
