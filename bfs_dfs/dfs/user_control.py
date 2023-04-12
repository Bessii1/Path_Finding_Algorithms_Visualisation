import pygame as pg
from random import random
from collections import deque


def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))
    return (grid_x, grid_y) if not grid[grid_y][grid_x] else False


def draw_grid():
    [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
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


cols, rows = 35, 20
TILE = 50
mouse_positions = []

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()
# grid
grid = [[1 if random() < 0.2 else 0 for col in range(cols)] for row in range(rows)]
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# BFS settings
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
    [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for x, y in queue]

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
            pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
            path_segment = visited[path_segment]
        pg.draw.rect(sc, pg.Color('blue'), get_rect(*start_position), border_radius=TILE // 3)
        pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)

    pg.display.flip()
    clock.tick(30)