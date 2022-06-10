import random

BOARD_WIDTH = 10
BOARD_HEIGHT = 7
PIPE_CAPACITY = 4

TILE_QUEUE_LEN = 5


ENCODE_TILE = {
    "none":             0,
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
    "none":             "",
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

    def get_encoding(self):
        if isinstance(self.state, str):
            return (ENCODE_TILE[self.type], ENCODE_STATE[self.state])
        else:
            return (ENCODE_TILE[self.type], self.state)

class Wall(Tile):
    def __init__(self):
        self.type = "wall"
        self.state = "none"
        super().__init__(self.type, self.state)

class Floor(Tile):
    def __init__(self):
        self.type = "none"
        self.state = "none"
        super().__init__(self.type, self.state)


class Pipe(Tile):
    def __init__(self, type):
        self.state = 0
        super().__init__(type, self.state)
        self.type = type
        self.transition = {}

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
        self.transition = direction

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
        if (location[0] < 0 or location[0] > self.width) and \
            (location[1] < 0 or location[1] > self.height):
            return False
        self.tiles[self._coords_to_index(location)] = object
        return True

    def reset_board(self):
        self.tiles = [Floor()] * self.width * self.height
        self.init_tap()

    def calc_next_state(self):
        """
        Increase the ratio of pipe filled given flow_rate
        if pipe state == 1 (the pipe is filled):
            calculate the next pipe to start
            if the next pipe does not exist:
                return failed.
            else:
                set state to 0.01 or some other value so its started to be filled
                and cannot be changed
        """
        self.tiles[self.current_water_position].state -= 1
        if self.tiles[self.current_water_position].state == 0:
            self.current_water_position = self._get_next_water_position()
            
        raise NotImplementedError

    def init_tap(self):
        tap_location = list(self.get_random_location())
        tap_direction = self.get_valid_tap_direction(tap_location)
        self.set_tile(tap_location, StartingPipe(direction=tap_direction))
        self.current_water_position = self._coords_to_index(tap_location)


    def _get_next_water_position(self):
        #potential_next_position = self.tiles[self.current_water_position].transition
        water_direction = self.tiles[self.current_water_position].transition
        next_position_index = -1
        #if water_direction == "up":
            #next_position_index = 



        raise NotImplementedError


    def get_valid_tap_direction(self, location, return_directions=False):
        edges = [0, self.width-1, self.height-1]
        directions = ["up", "right", "down", "left"]
        x,y = location
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
            return_string = "-"*130 + "\n"
            for i in range(self.height):
                for j in range(self.width):
                    return_string += "| {:^10s} ".format(ENCODE_ASCII[self.tiles[i*self.width + j].type])
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

        #print("-"*130)
        #for i in range(self.height):
        #    for j in range(self.width):
        #        #print("| {:^10s} ".format(self.board[i*self.width + j].type), end="")
        #        print("| {:^10s} ".format(ENCODE_ASCII[self.tiles[i*self.width + j].type]), end="")
        #    print("|\n" + "-"*130)
        return return_string
    