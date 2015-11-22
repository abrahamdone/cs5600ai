import numpy
import random
import sys
import pygame
from pygame.locals import *

MOORE = 1
VON_NEUMANN = 2


def lookup_rule(a, rule, neighborhood):
    xmax, ymax = a.shape
    b = a.copy()
    for x in range(xmax):
        for y in range(ymax):
            self = a[x, y]
            neighbors = []
            if neighborhood == MOORE:
                neighbors = moore_neighbors(a, x, y)
            elif neighborhood == VON_NEUMANN:
                neighbors = von_neuman_neighbors(a, x, y)
            sum = alive_neighbors(neighbors)

            row = rule[self]
            b[x, y] = row[sum]
    return b


def von_neuman_neighbors(a, x, y):
    xmax, ymax = a.shape
    x1 = x + 1
    y1 = y + 1
    if x1 >= xmax:
        x1 = 0
    if y1 >= ymax:
        y1 = 0
    return [a[x, y - 1], a[x - 1, y], a[x1, y], a[x, y1]]


def moore_neighbors(a, x, y):
    xmax, ymax = a.shape
    x1 = x + 1
    y1 = y + 1
    if x1 >= xmax:
        x1 = 0
    if y1 >= ymax:
        y1 = 0
    return [a[x - 1, y - 1], a[x, y - 1], a[x1, y - 1], a[x - 1, y], a[x1, y], a[x - 1, y1], a[x, y1], a[x1, y1]]


def alive_neighbors(n):
    sum = 0
    for cell in n:
        if cell == 1:
            sum += 1
    return sum


# this function does all the work
def play_life(a):
    xmax, ymax = a.shape
    b = a.copy() # copy grid & Rule 2
    for x in range(xmax):
        for y in range(ymax):
            n = numpy.sum(a[max(x - 1, 0):min(x + 2, xmax), max(y - 1, 0):min(y + 2, ymax)]) - a[x, y]
            if a[x, y]:
                if n < 2 or n > 3:
                    b[x, y] = 0 # Rule 1 and 3
            elif n == 3:
                b[x, y] = 1 # Rule 4
    return b


SEED_OF_LIFE = 42
FPS = 0                         # the frames per second
WINDOW_WIDTH = 100              # the width of the window
WINDOW_HEIGHT = 100             # the height of the window
CELL_SIZE = 2
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size."
CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

random.seed(SEED_OF_LIFE)

# color constants
#            R    G    B
WHITE     = (255, 255, 255)
BLACK     = (0,   0,   0)
RED       = (255, 0,   0)
GREEN     = (0,   255, 0)
DARKGREEN = (0,   155, 0)
BLUE      = (0,   0,   255)
DARKBLUE  = (0,   0,   155)
LIGHTGRAY = (150, 150, 150)
DARKGRAY  = (40,  40,  40)
BGCOLOR   = BLACK
PINK      = (209, 127, 168)
LAVENDER  = (152, 97,  188)
ORANGE    = (255, 108, 0)
LIGHTBLUE = (76,  176, 255)

GRAYS = [(0, 0, 0),
         (15, 15, 15),
         (30, 30, 30),
         (45, 45, 45),
         (60, 60, 60),
         (75, 75, 75),
         (90, 90, 90),
         (105, 105, 105),
         (120, 120, 120),
         (135, 135, 135),
         (150, 150, 150),
         (165, 165, 165),
         (180, 180, 180),
         (195, 195, 195),
         (210, 210, 210),
         (225, 225, 225),
         (240, 240, 240),
         (255, 255, 255)]

COLOR_WHEEL = [(0, 0, 0),
               (76, 176, 255),
               (76, 255, 199),
               (129, 255, 76),
               (233, 255, 76),
               (255, 240, 76),
               (255, 204, 76),
               (255, 168, 76),
               (255, 117, 76),
               (240, 71, 95),
               (221, 66, 200),
               (135, 65, 219),
               (65, 76, 219)]

HISTORY_LIFE_RULES = [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                      [2, 2, 1, 1, 2, 2, 2, 2, 2, 0],
                      [2, 2, 2, 1, 2, 2, 2, 2, 2, 0]]

LIFE_RULES = [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 1, 0, 0, 0, 0, 0, 0]]

BRAIN = [[0, 0, 1, 2, 0, 2, 2, 2, 2, 0],
         [2, 2, 2, 1, 0, 2, 2, 2, 2, 0],
         [0, 0, 0, 0, 1, 2, 2, 1, 2, 0]]

CHEOPS = [[0, 4, 1, 9, 8, 0, 0, 0, 0, 0],
          [5, 0, 9, 7, 0, 6, 0, 9, 8, 0],
          [8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 2, 0, 0, 6, 0, 0, 4, 0],
          [3, 0, 0, 0, 3, 0, 1, 0, 0, 0],
          [4, 0, 3, 0, 9, 0, 6, 1, 0, 0],
          [0, 5, 0, 0, 0, 0, 4, 1, 0, 0],
          [2, 7, 0, 2, 6, 3, 8, 4, 6, 0],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 6, 7, 0, 8, 5, 3, 0]]

STRANGERS = [[0, 4, 1, 9, 8, 0, 0, 0, 0, 0],
             [5, 0, 9, 7, 0, 6, 0, 9, 8, 0],
             [2, 5, 0, 4, 0, 0, 0, 0, 0, 0],
             [0,10, 2,10, 0, 6, 0, 0, 4, 0],
             [3, 0,10, 0, 3, 0, 1,10, 0, 0],
             [4, 0, 3,10, 9, 0, 6, 1, 0, 0],
             [0, 5, 0, 0, 0, 0, 4, 1, 0, 0],
             [2, 7, 0, 2, 6, 3, 8, 4, 6, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 6, 7, 0, 8, 5, 3, 0],
             [9, 0, 0, 5, 0, 4, 0, 0, 5, 0],
             [0, 0, 0, 0, 0, 0, 9, 0, 0, 0]]

BALLOONS = [[0, 0,15, 0, 0, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 4, 8, 4, 4, 4, 4, 4, 4, 0],
            [5, 5, 5, 5, 5, 7, 7, 9,11, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
            [5, 5, 5, 5, 5,13,13, 9,11, 0],
            [8, 8,10, 8, 8, 8, 8, 8, 8, 0],
            [2, 2, 2, 2, 2, 9,13, 9,11, 0],
            [10,10, 0,10,10,10,10,10,10, 0],
            [4,14,14,14,14,14,14,14,11, 0],
            [2,12, 4,12,12,12,12,12,12, 0],
            [6, 6, 6, 6,13,13,13, 9,11, 0],
            [14,14,14,12,14,14,14,14,14, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 0]]

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()


def run_game():

    # replace (5, 5) with the desired dimensions
    life = numpy.zeros((WINDOW_WIDTH/CELL_SIZE, WINDOW_HEIGHT/CELL_SIZE), dtype=numpy.byte)

    # place starting conditions here
    # life[2, 1:4] = 1 # a simple "spinner"
    # life[3, 2] = 1
    # life[1, 1] = 1
    # for x in xrange(len(life)):
    #     for y in xrange(len(life)):
    #         life[x][y] = random.randint(0, 2)
    life[2:4, 6:8] = 1
    life[36:38, 4:6] = 1
    life[12:13, 6:9] = 1
    life[13:14, 5:6] = 1
    life[13:14, 9:10] = 1
    life[14:16, 4:5] = 1
    life[14:16, 10:11] = 1
    life[16:17, 7:8] = 1
    life[17:18, 5:6] = 1
    life[17:18, 9:10] = 1
    life[18:19, 6:9] = 1
    life[19:20, 7:8] = 1

    life[22:24, 4:7] = 1
    life[24:25, 3:4] = 1
    life[24:25, 7:8] = 1
    life[26:27, 2:4] = 1
    life[26:27, 7:9] = 1

    tick = 0
    while True:  # main game loop
        print(tick)
        tick += 1
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        DISPLAYSURF.fill(BGCOLOR)
        draw_grid()

        for x in xrange(len(life)):
            for y in xrange(len(life)):
                draw_cell(x, y, GRAYS[life[x, y]])

        life = lookup_rule(life, BALLOONS, MOORE)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def show_start_screen():
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surf1 = title_font.render('Life!', True, WHITE, DARKGREEN)
    title_surf2 = title_font.render('Life!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotated_surf1 = pygame.transform.rotate(title_surf1, degrees1)
        rotated_rect1 = rotated_surf1.get_rect()
        rotated_rect1.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DISPLAYSURF.blit(rotated_surf1, rotated_rect1)

        rotated_surf2 = pygame.transform.rotate(title_surf2, degrees2)
        rotated_rect2 = rotated_surf2.get_rect()
        rotated_rect2.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DISPLAYSURF.blit(rotated_surf2, rotated_rect2)

        draw_press_key_msg()

        if check_for_key_press():
            pygame.event.get()  # clear event queue
            return

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def draw_press_key_msg():
    press_key_surf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
    DISPLAYSURF.blit(press_key_surf, press_key_rect)


def check_for_key_press():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key


def show_game_over_screen():
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surf = game_over_font.render('Game', True, WHITE)
    over_surf = game_over_font.render('Over', True, WHITE)
    game_rect = game_surf.get_rect()
    over_rect = over_surf.get_rect()
    game_rect.midtop = (WINDOW_WIDTH / 2, 10)
    over_rect.midtop = (WINDOW_WIDTH / 2, game_rect.height + 10 + 25)

    DISPLAYSURF.blit(game_surf, game_rect)
    DISPLAYSURF.blit(over_surf, over_rect)
    draw_press_key_msg()
    pygame.display.update()
    pygame.time.wait(500)
    check_for_key_press()  # clear out any key presses in the event queue

    while True:
        if check_for_key_press():
            pygame.event.get()  # clear event queue
            return


def draw_cell(x, y, color):
    x *= CELL_SIZE
    y *= CELL_SIZE
    cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAYSURF, color, cell_rect)


def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOW_WIDTH, y))


if __name__ == '__main__':
    main()
