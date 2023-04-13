import pygame as pg
from bfs_dfs.grid_generator.Grid import *

grid_generator = Grid(25, 15, 60, False)

pg.init()

cols = grid_generator.columns
rows = grid_generator.rows
TILE = grid_generator.tile
grid = grid_generator.grid
graph = grid_generator.get_graph()

sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()

# DFS settings
start = (0, 0)
queue = [start]
visited = {start: None}
cur_node = start

while True:
    sc.fill(pg.Color('black'))
    [[pg.draw.rect(sc, pg.Color('darkorange'), grid_generator.get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
    [pg.draw.rect(sc, pg.Color('forestgreen'), grid_generator.get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), grid_generator.get_rect(x, y)) for x, y in queue]

    if queue:
        cur_node = queue.pop()
        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node

    path_head, path_segment = cur_node, cur_node
    while path_segment:
        pg.draw.rect(sc, pg.Color('white'), grid_generator.get_rect(*path_segment), TILE, border_radius=TILE // 3)
        path_segment = visited[path_segment]
    pg.draw.rect(sc, pg.Color('blue'), grid_generator.get_rect(*start), border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('magenta'), grid_generator.get_rect(*path_head), border_radius=TILE // 3)

    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(7)
