import os
import sys
import pygame
from pygame.locals import *
import objects
from colors import *

x = 450
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (x, y)

pygame.init()
clock = pygame.time.Clock()

# draw constants
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 600
FIELD_WIDTH = SCREEN_WIDTH * 5 / 8
NUM_COLUMNS = 20
NUM_ROWS = 50
CELL_HEIGHT = CELL_WIDTH = FIELD_WIDTH / NUM_COLUMNS

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
                cell_color = field.cells[i][j]
                pygame.draw.rect(surface, cell_color, pygame.Rect(j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                pygame.draw.rect(surface, BLACK, pygame.Rect(j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 1)
    
    
def play():
    field = objects.Field(NUM_ROWS, NUM_COLUMNS)
    block = objects.Block(field, 'S', YELLOW) # just an example
    field.place_block(block,(3,4))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_r:
                    field.rotate(block)
                    
                    
        DISPLAYSURFACE.fill(WHITE)
        draw_field(DISPLAYSURFACE, field)
        
        pygame.display.update()
        
if __name__ == '__main__':
    play()
