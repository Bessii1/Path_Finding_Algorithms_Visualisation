import pygame as pg
from heapq import *


def get_circle(x, y):
    return (x * TILE + TILE // 2, y * TILE + TILE // 2), TILE // 4


def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]

def get_rgb_color_from_hex(hex_color):
    return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))

def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))
    return (grid_x, grid_y)

def heuristic(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])

def dijkstra(start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break

        neighbours = graph[cur_node]
        for neighbour in neighbours:
            neigh_cost, neigh_node = neighbour
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node
    return visited, queue

cols, rows = 23, 13
TILE = 70
mouse_positions = []


pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()
# grid
grid = ['22222222222222222222212',
        '22222292222911112244412',
        '22444422211112911444412',
        '24444444212777771444912',
        '24444444219777771244112',
        '92444444212777791192144',
        '22229444212777779111144',
        '11111112212777772771122',
        '27722211112777772771244',
        '27722777712222772221244',
        '22292777711144429221244',
        '22922777222144422211944',
        '22222777229111111119222']
grid = [[int(char) for char in string ] for string in grid]
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# BFS settings
start = tuple()
goal = tuple()
queue = []
cost_visited = {}
visited = {}

running = True
while running:
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            pg.draw.rect(sc, get_rgb_color_from_hex("#F9E2AF"), get_rect(x, y))

    [pg.draw.rect(sc, get_rgb_color_from_hex("#009FBD"), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, get_rgb_color_from_hex("#A5D7E8"), get_rect(*xy)) for _, xy in queue]

    if start:
        pg.draw.circle(sc, pg.Color('red'), *get_circle(*start))
    if goal:
        pg.draw.circle(sc, pg.Color('red'), *get_circle(*goal))


    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == pg.BUTTON_LEFT:
                mouse_pos = get_click_mouse_pos()
                if mouse_pos:
                    mouse_positions.append(mouse_pos)
                    if len(set(mouse_positions)) == 1:
                        start = list(set(mouse_positions))[0]

                    if len(set(mouse_positions)) == 2:
                        start = list(mouse_positions)[0]
                        goal = list(mouse_positions)[1]
                        visited, queue = dijkstra(start, goal, graph)



            elif event.button == pg.BUTTON_RIGHT:
                start = tuple()
                goal = tuple()
                queue = []
                cost_visited = {}
                visited = {}
                cur_node = tuple()
                mouse_positions = []



    # draw path
    path_head, path_segment = goal, goal
    if goal:
        while path_segment and path_segment in visited:
            pg.draw.circle(sc, get_rgb_color_from_hex("#77037B"), *get_circle(*path_segment))
            path_segment = visited[path_segment]
        pg.draw.circle(sc, pg.Color('red'), *get_circle(*start))
        pg.draw.circle(sc, get_rgb_color_from_hex("#77037B"), *get_circle(*path_head))

    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(30)