

BOARD_WIDTH = 10
BOARD_HEIGHT = 7

TILE_QUEUE_LEN = 5

PLAYING_TILES = [
    "vertical",
    "horizontal",
    "cross",
    "leftup",
    "leftdown",
    "rightup",
    "rightdown"
]

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

ENCODE_DIRECTIONS = {
    "up":               0,
    "right":            1,
    "down":             2,
    "left":             3
}

# Base class for all tilesl
################################################## maybe remove this one
class Tile:
    def __init__(self, type, state):
        self.type = type
        self.state = state

    def get_encoding(self):
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
    
class Cross(VerticalPipe, HorizontalPipe):
    def __init__(self):
        super(Cross, self).__init__(type="cross")

class LeftUp(Pipe):
    def __init__(self):
        super().__init__("leftup")
        self.transition["left"] = "up"
        self.transition["up"] = "left"

class LeftDown(Pipe):
    def __init__(self):
        super().__init__("leftdown")
        self.transition["left"] = "down"
        self.transition["down"] = "left"

class RightUp(Pipe):
    def __init__(self):
        super().__init__("rightup")
        self.transition["right"] = "up"
        self.transition["up"] = "right"

class RightDown(Pipe):
    def __init__(self):
        super().__init__("rightdown")
        self.transition["right"] = "down"
        self.transition["down"] = "right"

class Starting(Pipe):
    def __init__(self, direction="down"):
        super().__init__("start"+direction)
        self.transition = direction
        self.state = 0.0001 # slight offset from 0 so it isnt empty
