import pygame
import sys
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 900, 900
FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CELL_SIZE = np.array([50, 50])

win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('xd pls why')
clock = pygame.time.Clock()

class Point:
    def __init__(self, pos, velocity, size, mass) -> None:
        self.pos = pos.astype("float64")
        self.velocity = velocity.astype("float64")
        self.size = size
        self.mass = mass


def swap_2D_vec(vec):
    v = vec.tolist()
    return np.array([v[0], HEIGHT - v[1]]).astype("float64")


class Cell:
    def __init__(self, force_vec, size_vec) -> None:
        self.force_vec = force_vec.astype("float64")
        self.size_vec =  size_vec


class Grid:
    def __init__(self, cells, win, friction) -> None:
        self.cells = cells
        self.win = win
        self.points = []
        self.friction = friction


    def draw_vector_field(self):
        cell_size = self.cells[0][0].size_vec.tolist()
        
        for x_index in range(len(self.cells[0])):
            pygame.draw.line(self.win, "green", [x_index * cell_size[0], 0], [x_index * cell_size[0], HEIGHT])

        for y_index in range(len(self.cells)):
            pygame.draw.line(self.win, "green", [0, y_index * cell_size[1]], [WIDTH, y_index * cell_size[1]])

        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                cell = self.cells[y][x]
                vec_origin = np.array([(x + 0.5) * cell_size[0], (y + 0.5) * cell_size[1]])
                pygame.draw.line(self.win, "red", swap_2D_vec(vec_origin), swap_2D_vec(vec_origin + cell.force_vec * 30))

        # for point in self.points:
        #     pygame.draw.circle(self.win, "white", swap_2D_vec(point.pos), point.size)


    def change_cells(self, acc_function, cell_size, grid_res):
        self.cells = [[Cell(acc_function(x, y), cell_size) for x in range(grid_res.flat[0])] for y in range(grid_res.flat[1])]

    def update(self):
        for point in self.points:

            point_coord = np.floor(point.pos / CELL_SIZE).astype("int32")
        
            if point.pos.flat[0] < 0 or point.pos.flat[0] >= WIDTH or point.pos.flat[1] < 0 or point.pos.flat[1] >= HEIGHT: # if point outside the canvas
                self.points.remove(point)
                continue

            cell = self.cells[point_coord.flat[1]][point_coord.flat[0]]

            force = cell.force_vec.astype("float64")
            acceleration = force / point.mass
            point.velocity += acceleration - (point.velocity * self.friction)
            point.pos += point.velocity

    def update_and_draw(self):
        for point in self.points:
            pos0 = point.pos.astype("float64")

            point_coord = np.floor(point.pos / CELL_SIZE).astype("int32")
        
            if point.pos.flat[0] < 0 or point.pos.flat[0] >= WIDTH or point.pos.flat[1] < 0 or point.pos.flat[1] >= HEIGHT: # if point outside the canvas
                self.points.remove(point)
                continue

            cell = self.cells[point_coord.flat[1]][point_coord.flat[0]]

            force = cell.force_vec.astype("float64")
            acceleration = force / point.mass
            point.velocity += acceleration - (point.velocity * self.friction)
            point.pos += point.velocity

            pygame.draw.line(self.win, "white", swap_2D_vec(pos0), swap_2D_vec(point.pos), 1)


def acc_function(x, y):
    return np.array([
        random.uniform(-1, 1),
        random.uniform(-1, 1),
    ])

def generate_points(n):
    points = []
    # for i in range(n):
    #     points.append(Point(np.array([random.randint(0, WIDTH), random.randint(0, HEIGHT)]), np.array([0, 0]), 5, 10))

    # return points
    cell_size = grid.cells[0][0].size_vec.tolist()

    for y in range(len(grid.cells)):
        for x in range(len(grid.cells[y])):
            vec_origin = np.array([(x + 0.5) * cell_size[0], (y + 0.5) * cell_size[1]])
            points.append(Point(vec_origin, np.array([0, 0]), 5, 10))

    return points


grid_res = np.ceil(np.array([WIDTH, HEIGHT]) / CELL_SIZE).astype("int32")
grid = Grid(None, win, 0.1)
grid.change_cells(acc_function, CELL_SIZE, grid_res)

# grid.points.append(Point(np.array([300, 300]), np.array([0, 0]), 1, 1))
grid.points = generate_points(2000)

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            grid_res = np.ceil(np.array([WIDTH, HEIGHT]) / CELL_SIZE).astype("int32")
            grid.change_cells(np.array([5, 0]), CELL_SIZE, grid_res)
            
            print("XX")



    # grid.draw()
    grid.update_and_draw()
    grid.draw_vector_field()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()