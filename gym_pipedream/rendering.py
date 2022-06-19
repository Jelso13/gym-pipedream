import pygame
import numpy as np
import random
import os

#base_path = os.path.dirname(__file__)
base_path = os.path.join(os.path.dirname(__file__), "../images/pieces/")

PIPE_IMG = {
    "floor":            pygame.image.load(os.path.join(base_path, "floor.png")),
    "vertical":         pygame.image.load(os.path.join(base_path, "vert.png")),
    "horizontal":       pygame.image.load(os.path.join(base_path, "horiz.png")),
    "cross":            pygame.image.load(os.path.join(base_path, "cross.png")),
    "leftup":           pygame.image.load(os.path.join(base_path, "leftup.png")),
    "leftdown":         pygame.image.load(os.path.join(base_path, "leftdown.png")),
    "rightup":          pygame.image.load(os.path.join(base_path, "rightup.png")),
    "rightdown":        pygame.image.load(os.path.join(base_path, "rightdown.png")),
    "wall":             pygame.image.load(os.path.join(base_path, "wall.png")),
    "startdown":        pygame.image.load(os.path.join(base_path, "startdown.png")),
    "startup":          pygame.image.load(os.path.join(base_path, "startup.png")),
    "startleft":        pygame.image.load(os.path.join(base_path, "startleft.png")),
    "startright":       pygame.image.load(os.path.join(base_path, "startright.png"))
}

class Renderer:
    metadata = {"render_modes": ["human", "rgb_array", "ascii", "descriptive"], "render_fps": 1}
    def __init__(self, window_size=512):
        self.window_size = window_size
        pygame.init()
        pygame.display.init()
        self.window = None
        self.clock = pygame.time.Clock()
        self.board = None
        self.render_mode = "human"
        self.width = None
        self.height = None

    def render(self, board):
        if self.window is None:
            self.height = int((board.height / board.width)*self.window_size)
            self.width = self.window_size
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Pipe Dream")
            if self.render_mode == "human":
                self.window = pygame.display.set_mode((self.width, self.height))
            elif self.render_mode == "rgb_array":
                self.window = pygame.Surface(self.window_size)
        if self.clock is None:
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.width, self.height))
        
        #self.window.fill((0,0,0))
        tile_size = (
            self.width // board.width
        )  # The size of a single grid square in pixels
        #tile_size = 49

        for y in range(0, board.height):
            for x in range(0, board.width):
                tile = board.tiles[y * board.width + x] 
                cell = (x*tile_size, y * tile_size)

                #if tile.state == 0:
                #    self.fill_pipe2("","","", cell, tile_size, (0, 255, 0))
                #elif tile.state == board.pipe_capacity:
                #    self.fill_pipe2("","","", cell, tile_size)
                #elif tile.state >0 and tile.state < board.pipe_capacity: # pipe is being filled
                #    current_water = board.tiles[board.current_water_position]
                #    water_direction = current_water.transition[current_water.water_entrance]
                #    water_origin = current_water.water_entrance
                #    filled_ratio = (tile.state-1)/board.pipe_capacity
                #    self.fill_pipe2(filled_ratio, water_origin, water_direction, cell, tile_size, (255,0,0))
                if tile.state == 0: # if waterlogged
                    color = (0, 0, 255)
                    filled_ratio = 1
                    for k in tile.transition.keys():
                        if tile.water_entrance == k:
                            self.fill_pipe2(0, k, tile.transition[k], cell, tile_size, color)

                        print("k = ", k, "\ttile.transition[k] = ", tile.transition[k])
                        #self.fill_pipe2(0, k, tile.transition[k], cell, tile_size, color)
                elif tile.state == board.pipe_capacity or not tile.can_receive_water: # if empty
                    if tile.can_receive_water:
                        color = (0,0,0)
                        filled_ratio = 0
                        for k in tile.transition.keys():
                            print("k = ", k, "\ttile.transition[k] = ", tile.transition[k])
                            self.fill_pipe2(0.5, k, tile.transition[k], cell, tile_size, color)
                    #destination = current_water.transition[current_water.water_entrance]
                    #origin = current_water.water_entrance
                    #self.fill_pipe2(filled_ratio, origin, destination, cell, tile_size, color)
                else: # if being filled 
                    color = (0, 0, 255)
                    filled_ratio = (tile.state-1)/board.pipe_capacity
                    current_water = board.tiles[board.current_water_position]
                    destination = current_water.transition[current_water.water_entrance]
                    origin = current_water.water_entrance
                    
                    self.fill_pipe2(filled_ratio, origin, destination, cell, tile_size, color)


                tile_type = tile.type
                self.window.blit(
                    pygame.transform.scale(PIPE_IMG[tile_type], (tile_size, tile_size)), 
                    cell
                )

        if self.render_mode == "human":
            #self.window.blit(canvas, canvas.get_rect())
            #pygame.draw.arc(
            #    self.window,
            #    (0,255,0),
            #    pygame.Rect(0,0,49,49),
            #    45 * 3.14159/180,
            #    127 * 3.14159/180,
            #    width=6
            #)
            #pygame.draw.line(
            #    self.window,
            #    (0,255,0),
            #    (6 * tile_size, 6*tile_size + tile_size //2),
            #    (7 * tile_size, 6*tile_size + tile_size //2),
            #    width= int(tile_size * 1.0/4.0)
            #)
            pygame.event.pump()
            pygame.display.update()

            # handle framerate
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def fill_pipe2(self, ratio, origin, direction, cell, tile_size, color=(0,0,0)):
        if ratio == direction and direction == "":
            pygame.draw.rect(
                self.window,
                color,
                pygame.Rect(
                    cell,
                    (tile_size, tile_size)
                )
            )
        else:
            dir_coords = {
                "up":       np.array([cell[0] + tile_size // 2, cell[1]]),
                "right":    np.array([cell[0] + tile_size, cell[1] + tile_size // 2]),
                "down":     np.array([cell[0] + tile_size // 2, cell[1] + tile_size]),
                "left":     np.array([cell[0], cell[1] + tile_size // 2])
            }

            center = np.array([cell[0] + tile_size // 2, cell[1] + tile_size // 2])

            ratio = 1-ratio
            line_width = int(tile_size / 4.0)
            self.draw_line(dir_coords[origin], dir_coords[direction], center, ratio, color = color, line_width=line_width)


    def draw_line(self, origin, destination, center, ratio, color, line_width):
        if np.array_equal(origin, destination):
            origin = center
            center = ((center[0] + destination[0])//2, (center[1] + destination[1])//2)
        if ratio < 0.5:
            center = origin + ratio * (center - origin)
            pygame.draw.line(
                self.window,
                color,
                origin,
                center,
                width = line_width
            )
        else:
            pygame.draw.line(
                self.window,
                color,
                origin,
                center,
                width = line_width
            )
            ratio = (ratio - 0.5) / 0.5
            destination = center + ratio*(destination - center)
            pygame.draw.line(
                self.window,
                color,
                center,
                destination,
                width = line_width
            )

