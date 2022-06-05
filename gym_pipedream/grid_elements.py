

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


if __name__=="__main__":

    def all_subclasses(cls):
        return list(set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in all_subclasses(c)]))

    subcls = [cl for cl in all_subclasses(Tile) if cl.__name__ != "Pipe"]

    print(subcls)

    for cl in subcls:
        x = cl()
        print("type {:<20s} encoding {:<10s}".format(str(x.type), str(x.get_encoding())))

