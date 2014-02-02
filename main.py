import os
import sys
import pygame
from pygame.locals import *
import objects
from colors import *
import scramble

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
    
def draw_screen(surface, field):
    '''
    Draws the given field and its current state to the display surface.
    '''
    
    for i in range(field.num_rows):
        for j in range(field.num_columns):
            if field.cells[i][j]:
                cell_color = field.cells[i][j]['color']
                block_rect = pygame.Rect(j * CELL_WIDTH, i * CELL_HEIGHT, \
                                         CELL_WIDTH, CELL_HEIGHT)
                draw_outlined_rect(surface, cell_color, block_rect)
                
    # field boundaries
    pygame.draw.line(surface, BLACK, (FIELD_WIDTH, 0), \
        (FIELD_WIDTH, SCREEN_HEIGHT))
    pygame.draw.line(surface, BLACK, (FIELD_WIDTH, (SCREEN_HEIGHT / 4) * 3), \
        (SCREEN_WIDTH, (SCREEN_HEIGHT / 4) * 3))
        
    # draw the next block up
    nb_boundaries = (FIELD_WIDTH + ((SCREEN_WIDTH - FIELD_WIDTH) / 2), \
                    ((SCREEN_HEIGHT / 4) * 3) + ((SCREEN_HEIGHT - (SCREEN_HEIGHT / 4 * 3)) / 2))
    draw_next_block(surface, field, nb_boundaries)
    
def draw_outlined_rect(surface, color, rect):
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BLACK, rect, 1)
    
def draw_next_block(surface, field, init_loc):
    next_block = field.block_queue[0]
    offsets = next_block.get_offsets()
    next_block.locations = [init_loc]
    
    for offset in offsets:
        new_location = (init_loc[0] + offset[1] * CELL_HEIGHT, \
                        init_loc[1] + offset[0] * CELL_WIDTH)
        next_block.locations.append(new_location)
    
    for location in next_block.locations:
        row, column = location
        rect = pygame.Rect(row, column, CELL_WIDTH, CELL_HEIGHT)
        draw_outlined_rect(surface, next_block.color, rect)
    
def tick(field):
    if field.active_block_has_landed():
        field.deactivate_active_block()
        
    for i in range(len(field.cells)):
        if all(field.cells[i]):
            field.cells.pop(i)
            field.cells.insert(0, [None for j in range(field.num_columns)])
    
    if not field.active_block:
        field.get_block_from_queue()
        field.place_active_block((1,4))
    
    field.move_active_block([1,0])
            
def play():
    # load font and messages
    times = pygame.font.SysFont("Times New Roman", 72)
    pause_msg = "PAUSED"
    scrambler = scramble.Scrambler(pause_msg)
    pause_text = times.render(pause_msg, True, BLACK)
    pause_text_rect = pause_text.get_rect()
    pause_text_rect.centerx = SCREEN_WIDTH / 2
    pause_text_rect.centery = SCREEN_HEIGHT / 2
    
    # game-specific objects
    directions = {K_LEFT:[0,-1], K_RIGHT:[0,1]}
    field = objects.Field(NUM_ROWS, NUM_COLUMNS)
    field.place_active_block((1,4))
    time_counter = 0
    tick_delay = 600
    pause = False
    
    while True:
        if not pause:
            time_counter += FPS
        if time_counter >= tick_delay:
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
                if event.key == K_o:
                    print field.block_queue[0].orientation
                if event.key == K_p:
                    pause = not pause
                    if pause:
                        scrambled_msg = scrambler.get_scrambled_word()
                        pause_text = times.render(scrambled_msg, True, BLACK)
                if not pause:
                    if event.key == K_UP:
                        field.rotate_block()
                    if event.key in directions:
                        field.move_active_block(directions[event.key])
                    if event.key == K_DOWN:
                        time_counter = tick_delay
                    if event.key == K_SPACE:
                        field.drop_active_block()
                    
                    
        DISPLAYSURFACE.fill(LIGHT_GREY)
        if pause:
            DISPLAYSURFACE.blit(pause_text, pause_text_rect)
        else:
            draw_screen(DISPLAYSURFACE, field)
        
        pygame.display.update()
        clock.tick(FPS)
        
if __name__ == '__main__':
    play()
