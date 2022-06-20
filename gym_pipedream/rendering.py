from tkinter import W
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
    def __init__(self, window_size=512, render_fps=4):
        self.window_size = window_size
        self.render_fps = render_fps
        pygame.init()
        pygame.display.init()
        self.window = None
        self.clock = pygame.time.Clock()
        self.board = None
        self.render_mode = "human"
        self.width = None
        self.height = None

    def render(self, board, next_tiles, interpolate=True):
        if self.window is None:
            self.height = int((board.height / board.width)*self.window_size)
            self.width = self.window_size 
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Pipe Dream")
            if self.render_mode == "human":
                self.queue_width = (self.window_size // board.width) #* 2
                self.window = pygame.display.set_mode((self.width + self.queue_width, self.height))
                #self.window = pygame.display.set_mode((self.width, self.height))
                self.window.fill((195, 195, 195))
                self.board_border = ((self.window_size-1) // board.width)
                self.tile_size = (
                    (self.width-self.board_border) // board.width
                )  # The size of a single grid square in pixels
            elif self.render_mode == "rgb_array":
                self.window = pygame.Surface(self.window_size)
        if self.clock is None:
            self.clock = pygame.time.Clock()

        for y in range(0, board.height):
            for x in range(0, board.width):
                tile = board.tiles[y * board.width + x] 
                cell = np.array([x*self.tile_size + self.queue_width, y * self.tile_size]) + self.board_border // 2
                if y == 5 and x == 7:
                    print("5,7 = ", cell)
                if tile.state == 0: # if waterlogged
                    color = (9, 195, 255)
                    filled_ratio = 1
                    for k in tile.transition.keys():
                        if tile.water_entrance == k:
                            self.fill_pipe2(0, k, tile.transition[k], cell, self.tile_size, color)
                elif tile.state == board.pipe_capacity or not tile.can_receive_water: # if empty
                    if tile.can_receive_water and tile.state2 != 0:
                        color = (0,0,0)
                        filled_ratio = 0
                        for k in tile.transition.keys():
                            self.fill_pipe2(0.0, k, tile.transition[k], cell, self.tile_size, color)
                else: # if being filled 
                    color = (9, 195, 255)
                    filled_ratio = (tile.state)/board.pipe_capacity
                    current_water = board.tiles[board.current_water_position]
                    destination = current_water.transition[current_water.water_entrance]
                    origin = current_water.water_entrance
                    self.fill_pipe2(filled_ratio, origin, destination, cell, self.tile_size, color)

                tile_type = tile.type
                self.window.blit(
                    pygame.transform.scale(PIPE_IMG[tile_type], (self.tile_size, self.tile_size)), 
                    cell
                )

        for position, tile in enumerate(reversed(next_tiles[:5])):
            y_offset = (self.height - 5 * self.tile_size) // 2
            cell = np.array([self.queue_width // 2 - (self.tile_size // 4), position*self.tile_size + y_offset])
            pygame.draw.rect(
                self.window,
                (195, 195, 195),
                pygame.Rect(
                    cell,
                    (self.tile_size+2, self.tile_size+2)
                )
            )
            if tile.can_receive_water:
                color = (0,0,0)
                filled_ratio = 0
                for k in tile.transition.keys():
                    self.fill_pipe2(0.0, k, tile.transition[k], cell, self.tile_size, color)
            self.window.blit(
                pygame.transform.scale(PIPE_IMG[tile.type], (self.tile_size, self.tile_size)),
                cell
            )


        if self.render_mode == "human":
            pygame.event.pump()
            pygame.display.update()
            # handle framerate
            self.clock.tick(self.render_fps)
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.window)), axes=(1, 0, 2)
            )
        return np.transpose(
            np.array(pygame.surfarray.pixels3d(self.window)), axes=(1, 0, 2)
        )

    def fill_pipe2(self, ratio, origin, direction, cell, tile_size, color=(0,0,0)):
        dir_coords = {
            "up":       np.array([cell[0] + tile_size // 2, cell[1]]),
            "right":    np.array([cell[0] + tile_size, cell[1] + tile_size // 2]),
            "down":     np.array([cell[0] + tile_size // 2, cell[1] + tile_size]),
            "left":     np.array([cell[0], cell[1] + tile_size // 2])
        }

        center = np.array([cell[0] + tile_size // 2, cell[1] + tile_size // 2])
        ratio = 1-ratio
        line_width = int(tile_size / 5.5)
        self.draw_line(dir_coords[origin], dir_coords[direction], center, ratio, color = color, line_width=line_width)


    def draw_line(self, origin, destination, center, ratio, color, line_width):
        if np.array_equal(origin, destination):
            origin = center
            center = ((center[0] + destination[0])//2, (center[1] + destination[1])//2)
        if ratio <= 0.5:
            ratio = ratio * 2
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
            ratio = (ratio - 0.5) * 2
            destination = center + ratio*(destination - center)
            pygame.draw.line(
                self.window,
                color,
                center,
                destination,
                width = line_width
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

