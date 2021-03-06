import pygame
import random

BLACK = (0, 0, 0)
GRAY = (211, 211, 211)
YELLOW = (255, 255, 110)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = self.col * width
        self.y = self.row * width
        self.edges = []  # stores nodes that share edge with this node
        self.degree = len(self.edges)
        self.visited = False
        self.current = False
        self.walls = [True, True, True, True]  # [TOP, RIGHT, DOWN, LEFT]
        self.total_rows = total_rows
        self.valid_directions = self.get_valid_directions()
        self.neighbors = []
        self.color = BLACK

    def show(self, win):
        width = self.width
        x = self.x
        y = self.y

        pygame.draw.rect(win, self.color, (x, y, width, width))

        if self.visited:
            pygame.draw.rect(win, GRAY, (x, y, width, width))
        if self.current:
            pygame.draw.rect(win, YELLOW, (x, y, width, width))
        if self.walls[0]:
            pygame.draw.line(win, BLACK, (x, y), (x+width, y))
        if self.walls[1]:
            pygame.draw.line(win, BLACK, (x+width, y), (x+width, y+width))
        if self.walls[2]:
            pygame.draw.line(win, BLACK, (x+width, y+width), (x, y+width))
        if self.walls[3]:
            pygame.draw.line(win, BLACK, (x, y+width), (x, y))

    def get_valid_directions(self):
        valid_directions = ["up", "down", "left", "right"]
        random.shuffle(valid_directions)

        if self.row == 0:
            valid_directions.remove("up")
        if self.col == 0:
            valid_directions.remove("left")
        if self.row == self.total_rows - 1:
            valid_directions.remove("down")
        if self.col == self.total_rows - 1:
            valid_directions.remove("right")

        return valid_directions

    def get_neighbors(self, grid):
        for dir in self.valid_directions:
            if dir == "down":
                new_neighbor = grid[self.row + 1][self.col]

            elif dir == "up":
                new_neighbor = grid[self.row - 1][self.col]

            elif dir == "left":
                new_neighbor = grid[self.row][self.col - 1]

            elif dir == "right":
                new_neighbor = grid[self.row][self.col + 1]

            else:
                continue

            self.neighbors.append(new_neighbor)

    def remove_walls(self, neighbor):
        x = self.col - neighbor.col
        if x == 1:
            self.walls[3] = False
            neighbor.walls[1] = False
        elif x == -1:
            self.walls[1] = False
            neighbor.walls[3] = False

        y = self.row - neighbor.row
        if y == 1:
            self.walls[0] = False
            neighbor.walls[2] = False
        elif y == -1:
            self.walls[2] = False
            neighbor.walls[0] = False

    def add_edge(self, grid, direction=None, neighbor=None):

        if neighbor:
            new_neighbor = neighbor
        elif direction:
            if direction == "down":
                new_neighbor = grid[self.row + 1][self.col]

            if direction == "up":
                new_neighbor = grid[self.row - 1][self.col]

            if direction == "left":
                new_neighbor = grid[self.row][self.col - 1]

            if direction == "right":
                new_neighbor = grid[self.row][self.col + 1]
        else:
            return

        self.remove_walls(new_neighbor)
        new_neighbor.edges.append(self)
        new_neighbor.degree += 1
        self.edges.append(new_neighbor)
        self.degree += 1
