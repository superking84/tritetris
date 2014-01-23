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
        self.queue_limit = 5

        for i in range(num_rows):
            self.cells.append([])
            for j in range(num_columns):
                self.cells[i].append(None)
                
    def __repr__(self):
        output = '\n'.join([str([cell for cell in row]) for row in self.cells])
        
        return "Field state:\n" + output
        
    __str__ = __repr__
    
    def create_block(self, type, color):
        return Block(self, type, color)
        
    def create_random_block(self):
        return Block(self, random.choice(Block._types), colors.get_random_color())
        
    def add_block_to_queue(self, block):
        # changed to take a block as a parameter rather than assuming a random block
        self.block_queue.append(block)
    
    def load_queue(self):
        while len(self.block_queue) < self.queue_limit:
            self.add_block_to_queue()
    
    def get_block_from_queue(self):
        if self.block_queue:
            return self.block_queue.pop(0)
        else:
            print "Queue is empty!"
            
    def place_block(self, block, location):
        block.set_locations(location)
        for coordinate in block.locations:
            row, column = coordinate
            self.cells[row][column] = block.color

    def rotate(self, block, clockwise=True):
        '''
        Tilts the Block clockwise 90 degrees if clockwise is set to True(set to True
        by default), counterclockwise if False.
        '''
        valid_offsets = Block._type_offsets[block.type].keys()
        current_index = valid_offsets.index(block.orientation)
        old_orientation = block.orientation
        
        if clockwise:
            new_index = current_index + 1
            if new_index >= len(valid_offsets):
                new_index = 0
        else:
            new_index = current_index - 1
            
        block.orientation = valid_offsets[new_index]
            
        # some blocks don't need different orientations;
        # 'O' only has one, and 'S' and 'Z' only have two
        if block.orientation != old_orientation:
            head_loc = block.locations[0]
            for coordinate in block.locations:
                row, column = coordinate
                block.field.cells[row][column] = None
            block.set_locations(block.locations[0])
            self.place_block(block, head_loc)

class Block(object):
    '''
    A Block object covering four squares (or cells) within its parent Field.
    Each block type has a keystone square from which the coordinates of the
    other three squares of the Block are determined.  For example, an 'I' 
    Block at 0 degree orientation and at coordinates (5,4) would have squares at:
        (5,4), (5,5), (5,6), (5,7) which represent the Block in vertical index.
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

    def __init__(self, field, block_type, color):
        self.locations = [] # this will hold four tuples indicating the block's location once init'd
        self.field = field
        self.color = color # this should be in RGB format (or a pygcolors constant)
        self.type = block_type
        self.orientation = 0
        
    def __repr__(self):
        return 'Block type %s' % self.type
        
    __str__ = __repr__

    def set_locations(self, init_location):
        '''
        Using the 
        Applies a Block's starting location so that it can appear on the
        game field.
        Each Block type has three offsets.  init_location and these three offsets
        represent the location of each of the Block's four pieces.
        '''
        if self.locations:
            self.locations = []
        self.locations.append(init_location)
        for offset in self._type_offsets[self.type][self.orientation]:
            new_location = (init_location[0]  + offset[0], init_location[1] + offset[1])
            self.locations.append(new_location)
            
