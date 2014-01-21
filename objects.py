import random
import colors

class Field(object):
    '''
    The Field is the data structure that will hold all blocks
    currently on-screen, as well as the block currently falling.
    It is a list of lists, where for any <self.cells[i][j]>, i represents
    the row and j represents the column.
    '''

    def __init__(self, num_rows, num_columns):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.cells = []
        self.active_block = None
        self.block_queue = []

        for i in range(num_rows):
            self.cells.append([])
            for j in range(num_columns):
                self.cells[i].append(None)
                
    def __repr__(self):
        output = '\n'.join([str([cell for cell in row]) for row in self.cells])
        
        return "Field state:\n" + output
        
    def _create_random_block(self):
        return Block(self, random.choice(Block._types), colors.get_random_color())
        
    def get_block_from_queue(self):
        if self.block_queue:
            return self.block_queue.pop(0)
        else:
            print "Queue is empty!"
        
    def add_block_to_queue(self):
        self.block_queue.append(self._create_random_block())
    
    __str__ = __repr__
    
    


class Block(object):
    '''
    It is important to note that the Block object is not initialized with a location.
    Since Blocks are initially off-screen, in queue and waiting to be placed, they
    start off without a location.  Only when the game logic pulls them to the
    front of the queue are they given a location in the place_on_field method.
    '''

    _type_offsets = {
                     'I': {0:  [(0,1),(0,2),(0,3)],      90: [(1,0),(2,0),(3,0)]},
                     'O': {0:  [(0,1),(1,0),(1,1)]},
                     'T': {0:  [(1,-1),(1,0),(1,1)],     90: [(-1,-1),(0,-1),(1,-1)],
                          180: [(-1,-1),(-1,0),(-1,1)], 270: [(-1,1),(0,1),(1,1)]},
                     'S': {0:  [(0,1),(1,-1),(1,0)],     90: [(-1,0),(0,1),(1,1)]},
                     'Z': {0:  [(0,1),(1,1),(1,2)],      90: [(1,-1),(1,0),(2,-1)]},
                     'J': {0:  [(1,0),(2,-1),(2,0)],     90: [(-1,-2),(0,-2),(0,-1)],
                          180: [(-2,0),(-2,1),(-1,0)],  270: [(0,1),(0,2),(1,2)]},
                     'L': {0:  [(1,0),(2,0),(2,1)],      90: [(0,-2),(0,-1),(1,-2)],
                          180: [(-2,-1),(-2,0),(-1,0)], 270: [(-1,2),(0,1),(0,2)]}
                     }
    _types = _type_offsets.keys()

    def __init__(self, field, type, color):
        self.locations = [] # this will hold four tuples indicating the block's location once init'd
        self.field = field
        self.color = color # this should be in RGB format (or a pygcolors constant)
        self.type = type
        self.orientation = 0
        
    def __repr__(self):
        return 'Block type %s' % self.type
        
    __str__ = __repr__

    def _set_locations(self, init_location):
        '''
        This function applies a Block's starting location so that it can appear on the
        game field.
        Each Block type has three offsets.  init_location and these three offsets
        represent the location of each of the Block's four pieces.
        '''
        self.locations = []
        self.locations.append(init_location)
        for offset in _type_offsets[self.type][self.orientation]:
            new_location = (init_location[0]  + offset[0], init_location[1] + offset[1])
            self.locations.append(new_location)
            
    def rotate(self, clockwise=True):
        '''
        Tilts the Block clockwise 90 degrees if clockwise is set to True(set to True
        by default), counterclockwise if False.
        '''
        if clockwise:
            self.orientation = (self.orientation + 90) % 360
        else:
            self.orientation = (self.orientation - 90) % 360