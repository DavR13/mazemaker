import pygame
import random
import time
import functools
import disjointset
from maze_node import Node

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (211, 211, 211)
GREEN = (0, 128, 0)
RED = (128, 0, 0)

screen_width = 800
win = pygame.display.set_mode((screen_width, screen_width), flags = pygame.HIDDEN)


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args):
        start_time = time.perf_counter()
        value = func(*args)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


def make_grid(rows, width=800):
    grid = []
    gap = width // rows
    for x in range(rows):
        grid.append([])
        for y in range(rows):
            new_node = Node(x, y, gap, rows)
            grid[x].append(new_node)

    for row in grid:
        for node in row:
            node.get_neighbors(grid)

    return grid


def draw(win, grid):
    for row in grid:
        for node in row:
            node.show(win)

    pygame.display.update()


def get_random_neighbor(grid, current_node):
    direction = random.choice(current_node.valid_directions)

    if direction == "down":
        rand_neighbor = grid[current_node.row + 1][current_node.col]

    if direction == "up":
        rand_neighbor = grid[current_node.row - 1][current_node.col]

    if direction == "left":
        rand_neighbor = grid[current_node.row][current_node.col - 1]

    if direction == "right":
        rand_neighbor = grid[current_node.row][current_node.col + 1]

    return rand_neighbor


def animate(grid, speed):
    time.sleep(speed)
    draw(win, grid)

def color_rg_spaces(grid):
    for row in grid:
        for node in row:
            node.color = WHITE
            node.current = False
            node.visited = False

    grid[0][0].color = GREEN
    grid[len(grid)-1][len(grid)-1].color = RED
    draw(win, grid)

@timer
def binary_tree(grid, animation_speed):
    vertical_dir = random.choice(['up', 'down'])
    horizontal_dir = random.choice(['left', 'right'])
    directions = [vertical_dir, horizontal_dir]

    for row in grid:
        for node in row:
            node.current = True
            new_dir = random.choice(directions)
            if new_dir not in node.valid_directions:
                new_dir = random.choice(node.valid_directions)

            node.add_edge(grid, direction=new_dir)
            animate(grid, animation_speed)
            node.current = False
            node.color = WHITE

    color_rg_spaces(grid)

@timer
def aldous_broder(grid, animation_speed):
    start_row = random.randint(0, len(grid) - 1)
    start_col = random.randint(0, len(grid) - 1)
    start = grid[start_row][start_col]

    unvisited_nodes = [node for row in grid for node in row]
    unvisited_nodes.remove(start)

    current_node = start

    while unvisited_nodes:
        current_node.current = True
        new_node = get_random_neighbor(grid, current_node)
        new_node.color = WHITE
        if new_node in unvisited_nodes:
            current_node.add_edge(grid, neighbor=new_node)

            unvisited_nodes.remove(new_node)

        animate(grid, animation_speed)
        current_node.current = False
        current_node = new_node

    color_rg_spaces(grid)


@timer
def wilson(grid, animation_speed):
    start = None
    end = grid[random.randint(0,len(grid)-1)][random.randint(0,len(grid)-1)]
    end.color = RED
    maze = []
    unvisited_nodes = [node for row in grid for node in row]

    maze.append(end)
    unvisited_nodes.remove(end)

    while unvisited_nodes:

        while start not in unvisited_nodes:
            start_row = random.randint(0, len(grid) - 1)
            start_col = random.randint(0, len(grid) - 1)
            start = grid[start_row][start_col]

        current_node = start

        while current_node not in maze:
            current_node.current = True
            current_node.visited = True
            new_node = get_random_neighbor(grid, current_node)
            animate(grid, animation_speed)
            current_node.current = False
            current_node = new_node

        builder_node = None
        maze.append(start)

        while current_node != start:
            animate(grid, animation_speed)
            direction = ''
            maze.append(current_node)

            if current_node.row > start.row:
                direction = 'up'
                builder_node = grid[current_node.row - 1][current_node.col]
            if current_node.row < start.row:
                direction = 'down'
                builder_node = grid[current_node.row + 1][current_node.col]
            if current_node.col > start.col:
                direction = 'left'
                builder_node = grid[current_node.row][current_node.col - 1]
            if current_node.col < start.col:
                direction = 'right'
                builder_node = grid[current_node.row][current_node.col + 1]

            current_node.add_edge(grid, direction=direction)
            current_node = builder_node

        for node in maze:
            if node in unvisited_nodes:
                unvisited_nodes.remove(node)

        for row in grid:
            for node in row:
                node.visited = False
                if node in maze:
                    node.color = WHITE


    color_rg_spaces(grid)

@timer
def hunt_and_kill(grid, animation_speed):
    start_row = random.randint(0, len(grid) - 1)
    start_col = random.randint(0, len(grid) - 1)
    start = grid[start_row][start_col]
    unvisited_nodes = [node for row in grid for node in row]

    current_node = start
    while current_node is not None:
        current_node.current = True
        current_node.visited = True
        unvisited_nodes.remove(current_node)
        unvisited_neighbors = [neighbor for neighbor in current_node.neighbors if neighbor in unvisited_nodes]
        animate(grid, animation_speed)

        if len(unvisited_neighbors) > 0:
            neighbor = random.choice(unvisited_neighbors)
            current_node.add_edge(grid, neighbor=neighbor)
            current_node.current = False
            current_node = neighbor
        else:
            current_node.current = False
            current_node = None

            for node in unvisited_nodes:
                visited_neighbors = [neighbor for neighbor in node.neighbors if len(neighbor.edges) > 0]
                if len(node.edges) == 0 and len(visited_neighbors) > 0:
                    current_node = node
                    neighbor = random.choice(visited_neighbors)
                    current_node.add_edge(grid, neighbor=neighbor)
                    animate(grid, animation_speed)
                    break

    color_rg_spaces(grid)



def rec_backtrack(curr_row, curr_col, grid, animation_speed):

    current_node = grid[curr_row][curr_col]
    current_node.visited = True
    current_node.current = True

    for neighbor in current_node.neighbors:
        if not neighbor.visited:
            current_node.add_edge(grid, neighbor=neighbor)
            animate(grid, animation_speed)
            rec_backtrack(neighbor.row, neighbor.col, grid, animation_speed)

    current_node.current = False


@timer
def kruskal(grid, animation_speed):
    node_list = [node for row in grid for node in row]
    maze = []

    edges = [(node, neighbor) for node in node_list for neighbor in node.neighbors]
    ds = disjointset.DisjointSet(node_list)

    while len(maze) < len(node_list) - 1:
        edge = edges.pop(random.randint(0, len(edges)-1))
        edge[0].color = WHITE
        if ds.find(edge[0]) != ds.find(edge[1]):
            ds.union(edge[0], edge[1])
            edge[0].add_edge(grid, neighbor=edge[1])
            maze.append(edge)


        animate(grid, animation_speed)

    color_rg_spaces(grid)


@timer
def prim(grid, animation_speed):
    node_list = [node for row in grid for node in row]
    maze = set()
    frontier_nodes = []

    start_row = random.randint(0, len(grid) - 1)
    start_col = random.randint(0, len(grid) - 1)
    start = grid[start_row][start_col]

    maze.add(start)
    for neighbor in start.neighbors:
        frontier_nodes.append(neighbor)

    while len(maze) < len(node_list):
        for node in frontier_nodes:
            node.color = (255, 255, 140)
        for node in maze:
            node.color = WHITE
        animate(grid, animation_speed)
        new_node = random.choice(frontier_nodes)
        bridge_node = None
        while not bridge_node:
            bridge_node = random.choice(new_node.neighbors)
            if bridge_node in maze:
                new_node.add_edge(grid, neighbor = bridge_node)
                maze.add(new_node)
                frontier_nodes.remove(new_node)
                for neighbor in new_node.neighbors:
                    if neighbor not in maze and neighbor not in frontier_nodes:
                        frontier_nodes.append(neighbor)

            else:
                bridge_node = None

    color_rg_spaces(grid)


def run(algo, animation_speed, rows):
    grid = make_grid(rows, screen_width)

    pygame.display.set_caption("Maze Generator")
    pygame.display.set_mode((screen_width, screen_width), flags=pygame.SHOWN)

    if algo == 'binary tree':
        binary_tree(grid, animation_speed)

    elif algo == 'aldous broder':
        aldous_broder(grid, animation_speed)

    elif algo == 'wilson':
        wilson(grid, animation_speed)

    elif algo == 'hunt and kill':
        hunt_and_kill(grid, animation_speed)

    elif algo == 'recursive backtracking':
        rec_backtrack(random.randint(0, rows - 1),
                      random.randint(0, rows - 1),
                      grid, animation_speed)

        color_rg_spaces(grid)

    elif algo == 'prim':
        prim(grid, animation_speed)

    elif algo == 'kruskal':
        kruskal(grid, animation_speed)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.set_mode(flags=pygame.HIDDEN)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                pygame.display.set_mode(flags=pygame.HIDDEN)
