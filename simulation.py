import random
import pygame
import time
import math
from queue import Queue
from queue import PriorityQueue
from collections import deque

ROWS = 70
WIDTH = 770

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

dir = ((-1, 0), (0, 1), (1, 0), (0, -1))
dirAll = ((-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1))

CATACLYSM_PRODUCED = False
CATACLYSM = []
DEQUE_CATACLYSM = deque()
LEVEL_CATACLYSM = {}
CATACLYSM_BEEN = set()
CATACLYSM_PREV_LEVEL = 0
DEQUE_CATACLYSM_RELEASE = deque()
LEVEL_CATACLYSM_RELEASE = {}
CATACLYSM_BEEN_RELEASE = set()
CATACLYSM_PREV_LEVEL_RELEASE = 0
CATACLYSM_COUNTER = 0

PREDATOR = []
PREDATOR_NUMBER = 4
PREDATOR_ENERGY = 50
PREDATOR_CHANCE_EVOLVE = 30

EVOLVED_PREDATOR = []
EVOLVED_PREDATOR_ENERGY = 70
EVOLVED_PREDATOR_CHANCE_REGRESSION = 30

EVOLVED_PREY = []

PLANT = []
PREY = []
PREY_ENERGY = 30
PREY_NUMBER = 10
PREY_CHANCE_EVOLVE = 30

"""
predator = RED
prey = BLUE
plant = GREEN - spawn randomly

The prey (BLUE) eats plants (GREEN) and has a range of view ~ if it sees a plant, it will go after it,
if it doesn't see it stays on the same spot waiting.
If it's traveling and doesn't have enough energy it dies. 
If it has enough energy it reproduces itself at some point.

The evolved prey (TURQUOISE) eats plants is pretty slow, has a slow metabolism, it lets a mark behind by destroying the terrain.
It can't be eaten by predators since it's pretty big. (Probably wont survive to a cataclysm). It reproduces the unevoled one.

The predator (RED) hunts after prey (BLUE) and has a higher speed and range of view than prey, it also destroys every plant he passes by.
If it doesn't have enough energy, stays on the ground waiting for regeneration.
If it has enough energy it reproduce itself or it might evolve into the perfect predator.

The evolved predator (PURPLE) hunts prey and predator and has a higher speed and range view. 
It reproduces.
It has a chance of regression - to the species predator (RED).

The cataclysm (ORANGE) is an event that happens by chance once in a while (meteorite hit), it destroys the whole area nearby.

The hard terrain (BLACK) is an terrain obstacle.

The land (WHITE).

"""


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.energy = 0

    def get_pos(self):
        return self.row, self.col

    def is_ground(self):
        return self.color == WHITE

    def is_predator(self):
        return self.color == RED

    def is_prey(self):
        return self.color == BLUE

    def is_plant(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_uninhabitable(self):
        return self.color == ORANGE

    def reset(self):
        self.color = WHITE

    def make_predator(self):
        self.color = RED

    def make_ev_predator(self):
        self.color = PURPLE

    def make_prey(self):
        self.color = BLUE

    def make_plant(self):
        self.color = GREEN

    def make_uninhabitable(self):
        self.color = ORANGE

    def make_ground(self):
        self.color = WHITE

    def make_hard(self):
        self.color = BLACK

    def make_evolved_prey(self):
        self.color = TURQUOISE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):  # draws the lines of the grid
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):  # draws the spots
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def plant_spawn(win, grid):  # spawn plants
    global ROWS, PLANT
    n = 10
    while n != 0:
        r = random.randrange(0, ROWS)
        c = random.randrange(0, ROWS)
        spot = grid[r][c]
        if spot.is_ground():
            spot.make_plant()
            spot.energy = 15  # a plant has 15 energy to offer
            PLANT.append((r, c))
            for d in dir:
                if 0 <= r + d[0] < ROWS and 0 <= c + d[1] < ROWS and grid[r + d[0]][c + d[1]].is_plant():
                    for j in dir:
                        if 0 <= r + j[0] < ROWS and 0 <= c + j[1] < ROWS and grid[r + j[0]][c + j[1]].is_ground():
                            grid[r + j[0]][c + j[1]].make_plant()
                            grid[r + j[0]][c + j[1]].energy = 15
                            PLANT.append((r + j[0], c + j[1]))
                            break
                    break
        n -= 1


def prey_spawn(win, grid):  # spawn prey
    global PREY_NUMBER, PREY_ENERGY, ROWS, PREY
    n = PREY_NUMBER
    while n != 0:
        r = random.randrange(0, ROWS)
        c = random.randrange(0, ROWS)
        spot = grid[r][c]
        if spot.is_ground():
            PREY.append((r, c))
            spot.make_prey()
            spot.energy = PREY_ENERGY
            n -= 1


def prey_move(win, grid):  # the move made by the prey
    global PREY, PREY_ENERGY, GREEN, BLACK, PURPLE, ROWS, RED, ORANGE, TURQUOISE

    def dfs(graph, node, prev):
        if node not in graph:
            return prev
        return dfs(graph, graph[node], node)

    for i, prey in enumerate(PREY):
        chance_evolve = False
        number = random.randrange(0, 200)
        if number % 169 == 0:
            chance_evolve = True

        parent = {}
        start1, start2 = prey
        queue = Queue()
        been = set()
        t1, t2, foundClose = None, None, False
        been.add(prey)
        queue.put(prey)
        level = {prey: 0}
        if not chance_evolve:
            if grid[start1][start2].energy >= 50:  # here the species reproduces itself
                for d in dir:
                    if 0 <= start1 + d[0] < ROWS and 0 <= start2 + d[1] < ROWS and grid[start1 + d[0]][
                        start2 + d[1]].is_ground():
                        grid[start1 + d[0]][start2 + d[1]].make_prey()
                        grid[start1 + d[0]][start2 + d[1]].energy = PREY_ENERGY
                        PREY.append((start1 + d[0], start2 + d[1]))
                        grid[start1][start2].energy -= PREY_ENERGY
                        break
        elif chance_evolve and grid[start1][start2].energy >= 50:

            PREY.remove((start1, start2))
            EVOLVED_PREY.append((start1, start2))
            grid[start1][start2].color = TURQUOISE
            grid[start1][start2].energy -= 40
            continue

        for d in dirAll:  # here the prey eats the plants
            if 0 <= start1 + d[0] < ROWS and 0 <= start2 + d[1] < ROWS and grid[start1 + d[0]][
                start2 + d[1]].color == GREEN:  # seek for a close one
                grid[start1][start2].make_ground()
                grid[start1 + d[0]][start2 + d[1]].make_prey()
                PREY[i] = (start1 + d[0], start2 + d[1])
                foundClose = True
                PLANT.remove((start1 + d[0], start2 + d[1]))
                grid[start1 + d[0]][start2 + d[1]].energy += grid[start1][
                    start2].energy  # the new location of the prey + energy eaten from the plant
                grid[start1][start2].energy = 0
                break

        while not queue.empty() and not foundClose:
            r, c = queue.get()

            if level[(r, c)] == 15:  # the maximum range of the prey's view
                break

            for d in dirAll:
                if (r + d[0], c + d[1]) not in been and 0 <= r + d[0] < ROWS and 0 <= c + d[1] < ROWS and \
                        grid[r + d[0]][c + d[1]].color not in (BLUE, RED, ORANGE, BLACK, PURPLE, TURQUOISE):
                    parent[(r + d[0], c + d[1])] = (r, c)
                    level[(r + d[0], c + d[1])] = level[(r, c)] + 1
                    if grid[r + d[0]][c + d[1]].color == GREEN:

                        t1, t2 = r + d[0], c + d[1]
                        t1, t2 = dfs(parent, (t1, t2), None)
                        grid[start1][start2].make_ground()
                        grid[t1][t2].make_prey()

                        grid[t1][t2].energy = grid[start1][start2].energy - 1  # a step requires 1 energy
                        grid[start1][start2].energy = 0

                        PREY[i] = (t1, t2)

                        foundClose = True
                        if grid[t1][t2].energy <= 0:  # the prey dies ~ has no energy left
                            grid[t1][t2].make_ground()
                            PREY.remove((t1, t2))
                        break
                    queue.put((r + d[0], c + d[1]))
                    been.add((r + d[0], c + d[1]))


def evolved_prey_move(grid):  # the evolved prey moves
    global PREY, PREY_ENERGY, GREEN, BLACK, PURPLE, ROWS, RED, ORANGE, TURQUOISE

    def dfs(graph, node, prev):
        if node not in graph:
            return prev
        return dfs(graph, graph[node], node)

    for i, prey in enumerate(EVOLVED_PREY):

        parent = {}
        start1, start2 = prey
        queue = Queue()
        been = set()
        t1, t2, foundClose = None, None, False
        been.add(prey)
        queue.put(prey)
        level = {prey: 0}
        if grid[start1][start2].energy >= 300:  # here the species reproduces itself
            for d in dir:
                if 0 <= start1 + d[0] < ROWS and 0 <= start2 + d[1] < ROWS and grid[start1 + d[0]][
                    start2 + d[1]].is_ground():
                    grid[start1 + d[0]][start2 + d[1]].make_prey()
                    grid[start1 + d[0]][start2 + d[1]].energy = PREY_ENERGY
                    PREY.append((start1 + d[0], start2 + d[1]))
                    grid[start1][start2].energy -= PREY_ENERGY * 6
                    break

        for d in dirAll:  # here the prey eats the plants
            if 0 <= start1 + d[0] < ROWS and 0 <= start2 + d[1] < ROWS and grid[start1 + d[0]][
                start2 + d[1]].color == GREEN:  # seek for a close one
                grid[start1 + d[0]][start2 + d[1]].make_evolved_prey()
                EVOLVED_PREY[i] = (start1 + d[0], start2 + d[1])
                foundClose = True
                PLANT.remove((start1 + d[0], start2 + d[1]))
                grid[start1 + d[0]][start2 + d[1]].energy += grid[start1][
                    start2].energy  # the new location of the prey + energy eaten from the plant
                grid[start1][start2].energy = 0
                grid[start1][start2].make_hard()
                break

        if grid[start1][start2].energy <= 10:
            grid[start1][start2].energy += 0.5
            continue

        while not queue.empty() and not foundClose:
            r, c = queue.get()

            if level[(r, c)] == 15:  # the maximum range of the prey's view
                break

            for d in dirAll:
                if (r + d[0], c + d[1]) not in been and 0 <= r + d[0] < ROWS and 0 <= c + d[1] < ROWS and \
                        grid[r + d[0]][c + d[1]].color not in (BLUE, RED, ORANGE, BLACK, PURPLE, TURQUOISE):
                    parent[(r + d[0], c + d[1])] = (r, c)
                    level[(r + d[0], c + d[1])] = level[(r, c)] + 1
                    if grid[r + d[0]][c + d[1]].color == GREEN:

                        t1, t2 = r + d[0], c + d[1]
                        t1, t2 = dfs(parent, (t1, t2), None)
                        grid[start1][start2].make_ground()
                        grid[t1][t2].make_evolved_prey()

                        grid[t1][t2].energy = grid[start1][start2].energy - 1  # a step requires 1 energy
                        grid[start1][start2].energy = 0

                        EVOLVED_PREY[i] = (t1, t2)
                        if grid[start1][start2].color == WHITE or grid[start1][start2].color == GREEN:
                            grid[start1][start2].make_hard()

                        foundClose = True
                        break
                    queue.put((r + d[0], c + d[1]))
                    been.add((r + d[0], c + d[1]))


def predator_spawn(win, grid):  # predator spawn
    global PREDATOR, PREDATOR_NUMBER, PREDATOR_ENERGY
    n = PREDATOR_NUMBER
    while n != 0:
        r = random.randrange(0, ROWS)
        c = random.randrange(0, ROWS)
        spot = grid[r][c]
        if spot.is_ground():
            PREDATOR.append((r, c))
            spot.make_predator()
            spot.energy = PREDATOR_ENERGY
            n -= 1


def predator_move(win, grid):  # the move made by the predator
    global PREY, PREY_ENERGY, GREEN, BLACK, PURPLE, ROWS, RED, ORANGE, TURQUOISE, PREDATOR, PREDATOR_ENERGY, EVOLVED_PREDATOR
    number = random.randrange(0, ROWS)
    to_remove = []
    if number % 8 == 0:  # chance of evolving
        chance_of_ev = True
    else:
        chance_of_ev = False

    def dfs(graph, node, prev):
        if node not in graph:
            return prev
        return dfs(graph, graph[node], node)

    for i, predator in enumerate(PREDATOR):
        evolved = False
        parent = {}
        start1, start2 = predator
        queue = Queue()
        been = set()
        t1, t2, foundClose = None, None, False
        been.add(predator)
        queue.put(predator)
        level = {predator: 0}

        if grid[start1][start2].energy <= 10:
            grid[start1][start2].energy += 0.5
            continue

        if grid[start1][start2].energy >= 170 and not chance_of_ev:  # here the species reproduces itself
            for d in dir:
                if 0 <= start1 + d[0] < ROWS and 0 <= start2 + d[1] < ROWS and grid[start1 + d[0]][
                    start2 + d[1]].is_ground():
                    grid[start1 + d[0]][start2 + d[1]].make_predator()
                    grid[start1 + d[0]][start2 + d[1]].energy = PREDATOR_ENERGY
                    PREDATOR.append((start1 + d[0], start2 + d[1]))
                    grid[start1][start2].energy -= PREDATOR_ENERGY * 2
                    break

        elif grid[start1][
            start2].energy >= 180 and chance_of_ev:  # here the predator has a chance to evolve in a superior species
            evolved = True
            grid[start1][start2].make_ev_predator()
            to_remove.append((start1, start2))
            EVOLVED_PREDATOR.append((start1, start2))

        if not evolved:
            for d in dirAll:  # here the predator eats the prey
                if 0 <= start1 + d[0] < ROWS and 0 <= start2 + d[1] < ROWS and grid[start1 + d[0]][
                    start2 + d[1]].color == BLUE:  # seek for a close one
                    grid[start1][start2].make_ground()
                    PREY.remove((start1 + d[0], start2 + d[1]))
                    grid[start1 + d[0]][start2 + d[1]].make_predator()
                    PREDATOR[i] = (start1 + d[0], start2 + d[1])
                    foundClose = True
                    grid[start1 + d[0]][start2 + d[1]].energy += grid[start1][start2].energy - (
                                PREY_ENERGY // 2)  # the new location of the prey + energy eaten from the plant
                    grid[start1][start2].energy = 0

                    start1, start2 = start1 + d[0], start2 + d[1]
                    break

            while not queue.empty() and not foundClose:
                r, c = queue.get()
                if level[(r, c)] == 20:  # the maximum range of the predator's view for prey
                    break

                for d in dirAll:
                    if (r + d[0], c + d[1]) not in been and 0 <= r + d[0] < ROWS and 0 <= c + d[1] < ROWS and \
                            grid[r + d[0]][c + d[1]].color not in (RED, ORANGE, BLACK, TURQUOISE):
                        parent[(r + d[0], c + d[1])] = (r, c)
                        level[(r + d[0], c + d[1])] = level[(r, c)] + 1

                        if grid[r + d[0]][c + d[1]].color == BLUE:
                            t1, t2 = r + d[0], c + d[1]
                            t1, t2 = dfs(parent, (t1, t2), None)
                            grid[start1][start2].make_ground()
                            grid[t1][t2].make_predator()

                            grid[t1][t2].energy = grid[start1][start2].energy - 1  # a step requires 1 energy
                            grid[start1][start2].energy = 0

                            PREDATOR[i] = (t1, t2)

                            foundClose = True

                            # if grid[t1][t2].energy <= 0:  # the predator dies ~ has no energy left
                            #    grid[t1][t2].make_ground()
                            #    PREDATOR.remove((t1, t2))
                            break
                        queue.put((r + d[0], c + d[1]))
                        been.add((r + d[0], c + d[1]))
    if to_remove:
        for element in to_remove:
            PREDATOR.remove(element)


def ev_predator_move(win, grid):  # evolved predator
    global PREY, PREY_ENERGY, GREEN, BLACK, PURPLE, ROWS, RED, ORANGE, TURQUOISE, EVOLVED_PREDATOR

    def dfs(graph, node, prev):
        if node not in graph:
            return prev
        return dfs(graph, graph[node], node)

    for i, predator in enumerate(EVOLVED_PREDATOR):
        start1, start2 = predator
        number = random.randrange(0, 1000)
        if number % 696 == 0:  # chance of regression
            grid[start1][start2].make_predator()
            EVOLVED_PREDATOR.remove((start1, start2))
            PREDATOR.append((start1, start2))
            continue
        parent = {}
        queue = Queue()
        been = set()
        t1, t2, foundClose = None, None, False
        been.add(predator)
        queue.put(predator)
        level = {predator: 0}

        if grid[start1][start2].energy <= 30:
            grid[start1][start2].energy += 0.25
            continue

        if grid[start1][start2].energy >= 200:  # here the species reproduces itself
            for d in dir:
                if 0 <= start1 + d[0] < ROWS and 0 <= start2 + d[1] < ROWS and grid[start1 + d[0]][
                    start2 + d[1]].is_ground():
                    grid[start1 + d[0]][start2 + d[1]].make_ev_predator()
                    grid[start1 + d[0]][start2 + d[1]].energy = EVOLVED_PREDATOR_ENERGY
                    EVOLVED_PREDATOR.append((start1 + d[0], start2 + d[1]))
                    grid[start1][start2].energy -= PREDATOR_ENERGY * 3
                    break

        for d in dirAll:  # here the predator eats the prey
            if 0 <= start1 + d[0] < ROWS and 0 <= start2 + d[1] < ROWS and grid[start1 + d[0]][start2 + d[1]].color in (
            BLUE, RED):  # seek for a close one
                grid[start1][start2].make_ground()
                if grid[start1 + d[0]][start2 + d[1]].color == BLUE:
                    PREY.remove((start1 + d[0], start2 + d[1]))
                else:
                    PREDATOR.remove((start1 + d[0], start2 + d[1]))
                grid[start1 + d[0]][start2 + d[1]].make_ev_predator()
                EVOLVED_PREDATOR.remove((start1, start2))
                EVOLVED_PREDATOR.append((start1 + d[0], start2 + d[1]))
                foundClose = True
                grid[start1 + d[0]][start2 + d[1]].energy += grid[start1][
                                                                 start2].energy - 15  # the new location of the prey + energy eaten from the plant
                grid[start1][start2].energy = 0
                start1, start2 = start1 + d[0], start2 + d[1]
                break

        while not queue.empty() and not foundClose:
            r, c = queue.get()
            if level[(r, c)] == 50:
                break

            for d in dirAll:
                if (r + d[0], c + d[1]) not in been and 0 <= r + d[0] < ROWS and 0 <= c + d[1] < ROWS and \
                        grid[r + d[0]][c + d[1]].color not in (ORANGE, BLACK, PURPLE, TURQUOISE):
                    parent[(r + d[0], c + d[1])] = (r, c)
                    level[(r + d[0], c + d[1])] = (r, c)

                    if grid[r + d[0]][c + d[1]].color in (BLUE, RED):
                        t1, t2 = r + d[0], c + d[1]
                        t1, t2 = dfs(parent, (t1, t2), None)
                        grid[start1][start2].make_ground()
                        grid[t1][t2].make_ev_predator()

                        grid[t1][t2].energy = grid[start1][start2].energy - 1.25  # a step requires 1 energy
                        grid[start1][start2].energy = 0

                        EVOLVED_PREDATOR[i] = (t1, t2)

                        foundClose = True
                        # if grid[t1][t2].energy <= 0:  # the predator dies ~ has no energy left
                        #    grid[t1][t2].make_ground()
                        #    PREDATOR.remove((t1, t2))
                        break
                    queue.put((r + d[0], c + d[1]))
                    been.add((r + d[0], c + d[1]))


def hard_terrain(win, grid):  # obstacles
    for i in range(2):
        n = 7
        while n != 0:
            r = random.randrange(0, ROWS)
            c = random.randrange(0, ROWS)
            for i in range(30):
                if 0 <= r + 1 < ROWS and 0 <= c < ROWS:
                    grid[r][c].make_hard()
                    grid[r + 1][c].make_hard()
                    r += dirAll[n][0]
                    c += dirAll[n][1]
            n -= 1


def cataclysm_spawn():  # spawn of the cataclysm ~ coordinates for the epicenter
    global DEQUE_CATACLYSM, LEVEL_CATACLYSM, CATACLYSM_BEEN, DEQUE_CATACLYSM_RELEASE, LEVEL_CATACLYSM_RELEASE, CATACLYSM_BEEN_RELEASE, CATACLYSM_PREV_LEVEL, CATACLYSM_PREV_LEVEL_RELEASE
    r = random.randrange(0, ROWS)
    c = random.randrange(0, ROWS)
    DEQUE_CATACLYSM = deque()
    LEVEL_CATACLYSM = {(r, c): 0}
    DEQUE_CATACLYSM.append((r, c))
    CATACLYSM_BEEN = set()
    CATACLYSM_PREV_LEVEL = 0

    DEQUE_CATACLYSM_RELEASE = deque()
    LEVEL_CATACLYSM_RELEASE = {(r, c): 0}
    DEQUE_CATACLYSM_RELEASE.append((r, c))
    CATACLYSM_BEEN_RELEASE = set()
    CATACLYSM_PREV_LEVEL_RELEASE = 0


def cataclysm(grid):  # the cataclysm propagation
    global CATACLYSM_PREV_LEVEL, DEQUE_CATACLYSM, CATACLYSM_PREV_LEVEL_RELEASE, DEQUE_CATACLYSM_RELEASE, CATACLYSM_BEEN, CATACLYSM_BEEN_RELEASE, CATACLYSM_PRODUCED

    while DEQUE_CATACLYSM:
        r, c = DEQUE_CATACLYSM.popleft()
        if LEVEL_CATACLYSM[(r, c)] == 10:
            while DEQUE_CATACLYSM:
                DEQUE_CATACLYSM.pop()
            break
        if LEVEL_CATACLYSM[(r, c)] != CATACLYSM_PREV_LEVEL:
            DEQUE_CATACLYSM.appendleft((r, c))
            CATACLYSM_PREV_LEVEL += 1
            break
        if grid[r][c].color == BLUE:
            PREY.remove((r, c))
        elif grid[r][c].color == RED:
            PREDATOR.remove((r, c))
        elif grid[r][c].color == PURPLE:
            EVOLVED_PREDATOR.remove((r, c))
        elif grid[r][c].color == TURQUOISE:
            EVOLVED_PREY.remove((r, c))
        grid[r][c].color = ORANGE
        for d in dir:
            if 0 <= r + d[0] < ROWS and 0 <= c + d[1] < ROWS and (r + d[0], c + d[1]) not in CATACLYSM_BEEN:
                LEVEL_CATACLYSM[(r + d[0], c + d[1])] = LEVEL_CATACLYSM[(r, c)] + 1
                CATACLYSM_BEEN.add((r + d[0], c + d[1]))
                DEQUE_CATACLYSM.append((r + d[0], c + d[1]))
        CATACLYSM_PREV_LEVEL = LEVEL_CATACLYSM[r, c]

    if not DEQUE_CATACLYSM:
        while DEQUE_CATACLYSM_RELEASE:
            r, c = DEQUE_CATACLYSM_RELEASE.popleft()
            if LEVEL_CATACLYSM_RELEASE[(r, c)] == 10:
                while DEQUE_CATACLYSM_RELEASE:
                    DEQUE_CATACLYSM_RELEASE.pop()
                break
            if LEVEL_CATACLYSM_RELEASE[(r, c)] != CATACLYSM_PREV_LEVEL_RELEASE:
                DEQUE_CATACLYSM_RELEASE.appendleft((r, c))
                CATACLYSM_PREV_LEVEL_RELEASE += 1
                break
            grid[r][c].color = WHITE
            for d in dir:
                if 0 <= r + d[0] < ROWS and 0 <= c + d[1] < ROWS and (r + d[0], c + d[1]) not in CATACLYSM_BEEN_RELEASE:
                    LEVEL_CATACLYSM_RELEASE[(r + d[0], c + d[1])] = LEVEL_CATACLYSM_RELEASE[(r, c)] + 1
                    CATACLYSM_BEEN_RELEASE.add((r + d[0], c + d[1]))
                    DEQUE_CATACLYSM_RELEASE.append((r + d[0], c + d[1]))
            CATACLYSM_PREV_LEVEL_RELEASE = LEVEL_CATACLYSM_RELEASE[r, c]

    if not DEQUE_CATACLYSM and not DEQUE_CATACLYSM_RELEASE:
        CATACLYSM_PRODUCED = False


def run_simulation():
    global CATACLYSM_PRODUCED, CATACLYSM_COUNTER

    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Evolution")

    grid = make_grid(ROWS, WIDTH)
    run = True

    hard_terrain(WIN, grid)  # obstacles???
    prey_spawn(WIN, grid)
    predator_spawn(WIN, grid)
    plant_spawn(WIN, grid)

    prev_timePlants = time.time()
    prev_timePrey = time.time()
    prev_timeEvPrey = time.time()
    prev_timePredator = time.time()
    prev_timeEvPredator = time.time()
    prev_timeCataclysm = time.time()


    # this will actually be a frame, 1 timestamp == 1 frame per second
    timestamp = 0

    information_over_time = [] # an element of this list is equal with [len(PLANT), len(PREY), len(PREDATOR), len(EVOLVED_PREY), len(EVOLVED_PREDATOR), cataclysm_counter, timestamp]

    while run:
        #print(f"Plants: {len(PLANT)}, Prey: {len(PREY)}, Predator: {len(PREDATOR)}, Evolved Prey: {len(EVOLVED_PREY)}, Evolved Predator {len(EVOLVED_PREDATOR)}, Timestamp: {timestamp}, Cataclysm: {CATACLYSM_COUNTER}")
        information_over_time.append((len(PLANT), len(PREY), len(PREDATOR), len(EVOLVED_PREY), len(EVOLVED_PREDATOR), timestamp, CATACLYSM_COUNTER))
        new_timePlants = time.time()
        new_timePrey = time.time()
        new_timeEvPrey = time.time()
        new_timePredator = time.time()
        new_timeEvPredator = time.time()
        new_timeCataclysm = time.time()
        cataclysm_p = time.time()

        if 0.700000 < cataclysm_p - int(cataclysm_p) < 0.70200 and not CATACLYSM_PRODUCED:
            CATACLYSM_PRODUCED = True
            CATACLYSM_COUNTER += 1
            cataclysm_spawn()

        if new_timePlants >= prev_timePlants + 0.7:  # + 1
            prev_timePlants = new_timePlants
            plant_spawn(WIN, grid)

        if CATACLYSM_PRODUCED and new_timeCataclysm >= prev_timeCataclysm + 0.05:
            prev_timeCataclysm = new_timeCataclysm
            cataclysm(grid)

        if new_timeEvPredator >= prev_timeEvPredator + 0.12:  # + 0.2
            prev_timeEvPredator = new_timeEvPredator
            ev_predator_move(WIN, grid)

        if new_timePredator >= prev_timePredator + 0.2:  # + 0.3
            prev_timePredator = new_timePredator
            predator_move(WIN, grid)

        if new_timePrey >= prev_timePrey + 0.25:  # + 0.35
            prev_timePrey = new_timePrey
            prey_move(WIN, grid)
            # print("BLUE:", len(PREY))

        if new_timeEvPrey >= prev_timeEvPrey + 0.65:
            prev_timeEvPrey = new_timeEvPrey
            evolved_prey_move(grid)

        draw(WIN, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        timestamp += 1

        pygame.display.update()

    pygame.quit()

