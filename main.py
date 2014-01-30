import os
import sys
import pygame
from pygame.locals import *
import objects
from colors import *

# set the window's position onscreen
x = 450
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (x, y)

pygame.init()
clock = pygame.time.Clock()
FPS = 40

# draw constants
# a lot of the constants are related to one another to create
# proportionality
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 600
FIELD_WIDTH = SCREEN_WIDTH * 5 / 8
NUM_COLUMNS = 15
CELL_HEIGHT = CELL_WIDTH = FIELD_WIDTH / NUM_COLUMNS
NUM_ROWS = SCREEN_HEIGHT / CELL_HEIGHT

DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TriteTris!")

def terminate():
    pygame.quit()
    sys.exit()
    
def draw_field(surface, field):
    '''
    Draws the given field and its current state to the display surface.
    '''
    
    for i in range(field.num_rows):
        for j in range(field.num_columns):
            if field.cells[i][j]:
                cell_color = field.cells[i][j]['color']
                pygame.draw.rect(surface, cell_color, pygame.Rect(j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                pygame.draw.rect(surface, BLACK, pygame.Rect(j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 1)
    
def tick(field):
    field.move_active_block([1,0])
    
    # something may not be quite right here-- examine tomorrow
    for i in range(len(field.cells)):
        if all(field.cells[i]):
            field.cells.pop(i)
            field.cells.insert(0, [None for j in range(field.num_columns)])
    
def play():
    directions = {K_LEFT:[0,-1], K_RIGHT:[0,1]}
    field = objects.Field(NUM_ROWS, NUM_COLUMNS)
    # field.load_queue()
    # field.get_block_from_queue()
    time_counter = 0
    tick_delay = 600
    pause = False
    while True:
        if not pause:
            time_counter += FPS
        if time_counter >= tick_delay:
            if field.active_block_has_landed():
                print "True"
                field.drop_active_block()
                field.get_block_from_queue()
            tick(field)
            time_counter = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_l:
                    print field.block_queue
                if event.key == K_p:
                    pause = not pause
                if not pause:
                    if event.key == K_UP:
                        field.rotate_block()
                    if event.key in directions.keys():
                        field.move_active_block(directions[event.key])
                    if event.key == K_DOWN:
                        time_counter = tick_delay
                    if event.key == K_SPACE:
                        while not field.active_block_has_landed():
                            tick(field)
                    
                    
        DISPLAYSURFACE.fill(WHITE)
        draw_field(DISPLAYSURFACE, field)
        
        pygame.display.update()
        clock.tick(FPS)
        
if __name__ == '__main__':
    play()
