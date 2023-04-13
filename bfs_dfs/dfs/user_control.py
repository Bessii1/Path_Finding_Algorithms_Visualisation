import pygame as pg
from bfs_dfs.grid_generator.Grid import *

grid_generator = Grid(35, 20, 50, False)

pg.init()

cols = grid_generator.columns
rows = grid_generator.rows
TILE = grid_generator.tile
grid = grid_generator.grid
graph = grid_generator.get_graph()
mouse_positions = []

sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()

def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.rect(sc, pg.Color('red'), grid_generator.get_rect(grid_x, grid_y))
    return (grid_x, grid_y) if not grid[grid_y][grid_x] else False


def draw_grid():
    [[pg.draw.rect(sc, pg.Color('darkorange'), grid_generator.get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]


def dfs(start, goal, graph):
    stack = [start]
    visited = {start: None}

    while stack:
        cur_node = stack.pop()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                stack.append(next_node)
                visited[next_node] = cur_node

    return stack, visited

start_position = tuple()
goal = tuple()
queue = []
visited = {}
running = True
while running:
    # fill screen
    sc.fill(pg.Color('black'))
    # draw grid
    draw_grid()
    # draw BFS work
    [pg.draw.rect(sc, pg.Color('forestgreen'), grid_generator.get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), grid_generator.get_rect(x, y)) for x, y in queue]

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == pg.BUTTON_LEFT:
                mouse_pos = get_click_mouse_pos()
                if mouse_pos:
                    mouse_positions.append(mouse_pos)
                    if len(set(mouse_positions)) == 1:
                        start_position = list(set(mouse_positions))[0]
                        goal = start_position if not goal else goal
                        if len(queue) == 0:
                            queue = [start_position]
                        visited = {start_position: None} if not visited else visited

                    if len(set(mouse_positions)) == 2:
                        mouse_positions_set = set(mouse_positions)
                        start_position = list(mouse_positions_set)[1]
                        end_position = list(mouse_positions_set)[0]
                        if start_position and not grid[start_position[1]][start_position[0]]:
                            queue, visited = dfs(start_position, end_position, graph)
                            goal = end_position
                            mouse_positions = []

            elif event.button == pg.BUTTON_RIGHT:
                start_position = tuple()
                goal = tuple()
                queue = []
                visited = {}
                mouse_positions = []

    if start_position:
        path_head, path_segment = goal, goal
        while path_segment and path_segment in visited:
            pg.draw.rect(sc, pg.Color('white'), grid_generator.get_rect(*path_segment), TILE, border_radius=TILE // 3)
            path_segment = visited[path_segment]
        pg.draw.rect(sc, pg.Color('blue'), grid_generator.get_rect(*start_position), border_radius=TILE // 3)
        pg.draw.rect(sc, pg.Color('magenta'), grid_generator.get_rect(*path_head), border_radius=TILE // 3)

    pg.display.flip()
    clock.tick(30)