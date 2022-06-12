import random

BOARD_WIDTH = 10
BOARD_HEIGHT = 7
PIPE_CAPACITY = 4

TILE_QUEUE_LEN = 5

REWARDS = {
    "spill": -10,
    "new_pipe": 1
}


ENCODE_TILE = {
    "floor":             0,
    "vertical":         1,
    "horizontal":       2,
    "cross":            3,
    "leftup":           4,
    "leftdown":         5,
    "rightup":          6,
    "rightdown":        7,
    "wall":             8,
    "startdown":        9,
    "startup":          10,
    "startleft":        11,
    "startright":       12
}

ENCODE_ASCII = {
    "floor":             "",
    "vertical":         "║",
    "horizontal":       "═",
    "cross":            "╬",
    "leftup":           "╝",
    "leftdown":         "╗",
    "rightup":          "╚",
    "rightdown":        "╔",
    "wall":             "█",
    "startdown":        "v",
    "startup":          "^",
    "startleft":        "<",
    "startright":       ">"
}

ENCODE_STATE = {
    "empty":            0,
    "full":             1,
    "none":             -1
}

# Base class for all tilesl
################################################## maybe remove this one
class Tile:
    def __init__(self, type, state):
        self.type = type
        self.state = state
        self.can_receive_water = False

    def get_encoding(self):
        if isinstance(self.state, str):
            return (ENCODE_TILE[self.type], ENCODE_STATE[self.state])
        else:
            return (ENCODE_TILE[self.type], self.state)

class Wall(Tile):
    def __init__(self):
        self.type = "wall"
        self.state = -1
        super().__init__(self.type, self.state)

class Floor(Tile):
    def __init__(self):
        self.type = "floor"
        self.state = -1
        super().__init__(self.type, self.state)


class Pipe(Tile):
    def __init__(self, type):
        self.state = PIPE_CAPACITY
        super().__init__(type, self.state)
        self.type = type
        self.transition = {}
        self.can_receive_water = True
        self.water_entrance = "none"

class VerticalPipe(Pipe):
    def __init__(self, type="vertical"):
        #super().__init__("vertical")
        super().__init__(type)
        self.transition["up"] = "down"
        self.transition["down"] = "up"

class HorizontalPipe(Pipe):
    def __init__(self, type = "horizontal"):
        #super().__init__("horizontal")
        super().__init__(type)
        self.transition["left"] = "right"
        self.transition["right"] = "left"
    
class CrossPipe(VerticalPipe, HorizontalPipe):
    def __init__(self):
        super(CrossPipe, self).__init__(type="cross")
        self.state2 = PIPE_CAPACITY

class LeftUpPipe(Pipe):
    def __init__(self, type="leftup"):
        super().__init__(type)
        self.transition["left"] = "up"
        self.transition["up"] = "left"

class LeftDownPipe(Pipe):
    def __init__(self, type="leftdown"):
        super().__init__(type)
        self.transition["left"] = "down"
        self.transition["down"] = "left"

class RightUpPipe(Pipe):
    def __init__(self, type="rightup"):
        super().__init__(type)
        self.transition["right"] = "up"
        self.transition["up"] = "right"

class RightDownPipe(Pipe):
    def __init__(self, type="rightdown"):
        super().__init__(type)
        self.transition["right"] = "down"
        self.transition["down"] = "right"

class StartingPipe(Pipe):
    def __init__(self, direction="down"):
        super().__init__("start"+direction)
        self.transition[direction] = direction
        self.water_entrance = direction

PLAYING_TILES = [
    VerticalPipe,
    HorizontalPipe,
    CrossPipe,
    LeftUpPipe,
    LeftDownPipe,
    RightUpPipe,
    RightDownPipe
]

class Board:
    """
    Board Class

    Handles the interactions with the board.

    Attributes:
        width:          the width of the board
        height:         the height of the board
        print_style:    the style with which the board is rendered
        pipe_capacity:  the rate the water flows such that each step
                        the capacity remaining is decremented by 1.
                            pipe_capacity=4 means a new tile is filled
                            every 4 steps.
    """

    def __init__(self, width=BOARD_WIDTH, height=BOARD_HEIGHT, pipe_capacity=PIPE_CAPACITY, print_style="ascii"):
        self.width = width
        self.height = height
        self.tiles = [Floor()] * self.width * self.height
        self.print_style=print_style
        self.current_water_position = None
        self.pipe_capacity = pipe_capacity

    def get_tiles(self):
        return self.tiles

    def set_tile(self, location, object):
        # can only set tile if in grid, the floor or pipe with full capacity.
        previous_tile = self.tiles[self._coords_to_index(location)]

        in_grid = not (location[0] < 0 or location[0] > self.width or \
            location[1] < 0 or location[1] > self.height)

        is_floor = previous_tile.type == "floor"

        is_available_pipe = previous_tile.can_receive_water and previous_tile.state == self.pipe_capacity

        if in_grid and (is_floor or is_available_pipe):
            self.tiles[self._coords_to_index(location)] = object
            return True
        return False

    def reset_board(self):
        self.tiles = [Floor()] * self.width * self.height
        self.init_tap()

    def init_tap(self):
        tap_location = list(self.get_random_location())
        tap_direction = self.get_valid_tap_direction(tap_location)
        self.set_tile(tap_location, StartingPipe(direction=tap_direction))
        self.current_water_position = self._coords_to_index(tap_location)

    def calc_next_state(self):
        """
        Increase the ratio of pipe filled given flow_rate
        if pipe state == 1 (the pipe is filled):
            calculate the next pipe to start
            if the next pipe does not exist:
                return failed.
            else:
                set state to capacity - 1 or some other value so its started to be filled
                and cannot be changed
        """
        done = False
        pipe_filled = False

        self.tiles[self.current_water_position].state -= 1
        # if the current water position is full move to next one
        if self.tiles[self.current_water_position].state == 0:
            next_water_position, water_entrance = self._get_next_water_position()

            # if the new water position is impossible or already full then water leaking
            if next_water_position < 0:
                done = True
            else: # the new pipe is correct - indicate it is being filled by reducing by -1
                self.current_water_position = next_water_position
                self.tiles[self.current_water_position].state -= 1
                self.tiles[self.current_water_position].water_entrance = water_entrance
                pipe_filled = True

        return pipe_filled, done


    def _get_next_water_position(self, water_direction=None):
        """
        Gets the valid index in the tiles array of the next pipe to fill with water.
        If an empty pipe is not in the next section of the water flow then the episode is over.
        """

        dir_to_index = {
            "up": -self.width,
            "right": 1,
            "down": self.width,
            "left": -1
        }
        switch_dir_perspective = {"up":"down", "down":"up", "left":"right", "right":"left"}

        # the water_entrance attribute provides the key to the transitions - set it when next water location hit.
        current_pipe = self.tiles[self.current_water_position]
        water_direction = current_pipe.transition[current_pipe.water_entrance]

        # determine if the next position is on the board
        next_position_index = -1
        print("water_direction = ", water_direction)
        if water_direction == "up" or water_direction == "down" or \
            (water_direction == "right" and (self.current_water_position + 1) % self.width != 0) or \
            (water_direction == "left" and self.current_water_position % self.width != 0):
            next_position_index = self.current_water_position + dir_to_index[water_direction]
            print("HIT")

        print("next_position_index = ", next_position_index)

        if next_position_index > len(self.tiles)-1 or not self.tiles[next_position_index].can_receive_water:
            return -1, switch_dir_perspective[water_direction]

        next_pipe = self.tiles[next_position_index]
        # if the next position is not an empty pipe or does not have entrance in correct direction
        if next_pipe.state != self.pipe_capacity or \
            switch_dir_perspective[water_direction] not in next_pipe.transition.keys():
            if next_pipe.type == "cross":
                # make state2 be full to utilise .state
                next_pipe.state2 = next_pipe.state
                next_pipe.state = self.pipe_capacity
            else:
                # make sure it isnt a cross pipe
                return -1, switch_dir_perspective[water_direction]

        return next_position_index, switch_dir_perspective[water_direction]


    def get_valid_tap_direction(self, location, return_directions=False):
        edges = [0, self.width-1, self.height-1]
        directions = ["up", "right", "down", "left"]
        x,y = location
        if x not in range(0, self.width) or y not in range(0,self.height):
            return [[],[]]
        if x == 0:
            directions.pop(3)
        if y == edges[2]:
            directions.pop(2)
        if x == edges[1]:
            directions.pop(1)
        if y == 0:
            directions.pop(0)
        if return_directions: return (random.choice(directions), directions)
        return random.choice(directions)

    def get_random_location(self, min_width=0, max_width=None, min_height=0, max_height=None):
        """ Get a random location from within the specified range """
        max_defaults = [self.width-1, self.height-1]
        max_vars = [max_width, max_height]
        max_width, max_height = [max_defaults[i] if max_vars[i] == None else max_vars[i] for i in range(2)]
        return (random.randint(min_width, max_width), random.randint(min_height, max_height))

    def _coords_to_index(self, coords):
        return coords[1] * self.width + coords[0]

    def __str__(self):
        # fix this as currently just sets everything to blue
        if self.print_style == "ascii":
            strt = "\033[36m"
            white = ""
            nd = "\033[0m"
            return_string = "-"*130 + "\n"
            for i in range(self.height):
                for j in range(self.width):
                    current_tile = self.tiles[i*self.width +j]
                    chr_val = ENCODE_ASCII[current_tile.type]
                    # if the pipe is currently being filled the show value
                    if current_tile.state < self.pipe_capacity and current_tile.state >0:
                        chr_val += str(current_tile.state)
                    # if full of water:
                    if self.tiles[i*self.width + j].state <= 0:
                        return_string += "| " + strt + "{:^10s} ".format(chr_val) + nd
                    else:
                        return_string += "| {:^10s} ".format(chr_val)
                return_string += "|\n" + "-"*130 + "\n"

        elif self.print_style == "descriptive":
            return_string = "-"*130 + "\n"
            for i in range(self.height):
                for j in range(self.width):
                    return_string += "| {:^10s} ".format(self.tiles[i*self.width + j].type)
                return_string += "|\n" + "-"*130 + "\n"
        else:
            strt = "\033[36m"
            nd = "\033[0m"
            return_string = "\n"
            #return_string = "-"*5 + "\n"
            for i in range(self.height):
                for j in range(self.width):
                    return_string += strt + str(ENCODE_ASCII[self.tiles[i*self.width + j].type]) + nd
                #return_string += "|\n" + "-"*5 + "\n"
                return_string += "\n"

        return return_string
    