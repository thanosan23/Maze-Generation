import random
import sys
import numpy as np
import pygame

from dsu import DSU

DIM = 10

# generate nodes
nodes = []
node_id = {}
for y in range(DIM):
    for x in range(DIM):
        nodes.append((x, y))
        node_id[(x, y)] = len(node_id)

# utilities to calculate neighbours from nodes
def valid_neighbour(x, y):
    return x >= 0 and x < DIM and y >= 0 and y < DIM

delta_x = [1, -1, 0, 0]
delta_y = [0, 0, 1, -1]

def neighbours(x, y):
    ret = []
    for dx, dy in zip(delta_x, delta_y):
        if valid_neighbour(x + dx, y + dy):
            ret.append((x+dx, y+dy))
    return ret

# generates maze using Kruskal's minimum spanning tree algorithm
def generate_maze():
    # generate edges from nodes based on neighbours
    edges = []
    for node in nodes:
        for neighbour in neighbours(*node):
            edges.append((node, neighbour))
    # Kruskal's algorithim with randomization
    maze = []

    dsu = DSU()
    dsu.init(len(nodes))

    random.shuffle(edges)

    while len(edges) > 0:
        edge = edges.pop(0)
        if not dsu.connected(node_id[edge[0]], node_id[edge[1]]):
            maze.append(edge)
            dsu.merge(node_id[edge[0]], node_id[edge[1]])
    return maze


# Rendering the maze
def pos_to_renderpos(x, cell_size=50):
    return 5 + x * (cell_size+5)

def generate_grid(maze):
    grid = [[0] * pos_to_renderpos(DIM)] * pos_to_renderpos(DIM)
    grid = np.array(grid)
    for edge in maze:
        x1, y1 = edge[0]
        x2, y2 = edge[1]

        for y in range(pos_to_renderpos(min(y1, y2)), pos_to_renderpos(max(y1, y2))+50):
            for x in range(pos_to_renderpos(min(x1, x2)), pos_to_renderpos(max(x1, x2))+50):
                grid[y][x] = 255
    return grid

maze = generate_maze()
grid = generate_grid(maze)

pygame.init()
screen = pygame.display.set_mode(((pos_to_renderpos(DIM),
                                   pos_to_renderpos(DIM))))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                maze = generate_maze()
                grid = generate_grid(maze)

    for y in range(pos_to_renderpos(DIM)):
        for x in range(pos_to_renderpos(DIM)):
            screen.set_at((y, x), (grid[y][x], grid[y][x], grid[y][x]))

    pygame.display.update()
    clock.tick(60)
