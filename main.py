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
    
    # DEBUG CODE: Show grid as a visual aid during coding
    for i in range(1,field.num_rows+1):
        pygame.draw.line(surface, BLACK, (0, CELL_HEIGHT * i), (FIELD_WIDTH, CELL_HEIGHT * i))
    for j in range(1,field.num_columns+1):
        pygame.draw.line(surface, BLACK, (CELL_WIDTH * j, 0), (CELL_WIDTH  * j, SCREEN_HEIGHT))
    # END DEBUG CODE
    
    
def play():
    field = objects.Field(NUM_ROWS, NUM_COLUMNS)
    block = objects.Block(field, 'I', RED) # just an example
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                    
        DISPLAYSURFACE.fill(WHITE)
        draw_field(DISPLAYSURFACE, field)
        
        pygame.display.update()
        
if __name__ == '__main__':
    play()
