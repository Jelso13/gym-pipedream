

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

ENCODE_STATE = {
    "empty":            0,
    "full":             1
}

# Base class for all tiles
class Tile:
    
    def __init__(self, type):
        self.type = type


class Pipe:
    def __init__(self, type):
        self.type = type
        self.state = "empty"
        self.transition = {}

class VerticalPipe(Pipe):
    def __init__(self):
        super().__init__("vertical")
        self.transition["top"] = "bottom"
        self.transition["bottom"] = "top"

class HorizontalPipe(Pipe):
    def __init__(self):
        super().__init__("horizontal")
        self.transition["left"] = "right"
        self.transition["right"] = "left"
    
class Cross(VerticalPipe, HorizontalPipe):
    def __init__(self):
        super(Cross, self).__init__()

class LeftUp(Pipe):
    def __init__(self):
        super().__init__("leftup")
        self.transition["left"] = "top"
        self.transition["top"] = "left"

class LeftDown(Pipe):
    def __init__(self):
        super().__init__("leftdown")
        self.transition["left"] = "bottom"
        self.transition["bottom"] = "left"

class RightUp(Pipe):
    def __init__(self):
        super().__init__("rightup")
        self.transition["right"] = "top"
        self.transition["top"] = "right"

class RightDown(Pipe):
    def __init__(self):
        super().__init__("rightdown")
        self.transition["right"] = "bottom"
        self.transition["bottom"] = "right"