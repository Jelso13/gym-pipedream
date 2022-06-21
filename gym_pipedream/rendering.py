import queue
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

    """
    max_width = 80% * screen width
    max_height = 80% * screen height

    self.width = board_border * 2 + self.tile_size * board.width 
    self.width = (queue_width + board.width + board_border * 2) * self.tile_size
    if board.width >= board.height:
        self.width = min(max_width, self.window_size)
        self.height = int((board.height/board.width) * self.width)
    else:
        self.height = min(max_height, self.window_size)
        self.width = int((board.width/board.height) * self.height)

    queue_width = 2 tiles
    poss_tile_width = max_width // (board_width + 1 + queue_width)
    poss_tile_height = max_height // (board_height + 1)
    tile_size = min(poss_tile_width, poss_tile_height)
    board_border = 0.5 * tile_size

    self.height = board_border * 2 + tile_size * board.height
    self.width = board_border * 2 + tile_size * board.width + queue_width
    """
    def render(self, board, next_tiles, interpolate=True):
        if self.window is None:
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Pipe Dream")
            self.refresh_values(board)

            if self.render_mode == "human":
                self.queue_tile_size = self.tile_size
                self.window = pygame.display.set_mode((self.width, self.height)) #, pygame.RESIZABLE)
                self.window.fill((195, 195, 195))
            elif self.render_mode == "rgb_array":
                self.window = pygame.Surface(self.window_size)
        if self.clock is None:
            self.clock = pygame.time.Clock()

        for y in range(0, board.height):
            for x in range(0, board.width):
                tile = board.tiles[y * board.width + x] 
                centering_vert = (5-board.height)/2 if board.height < 5 else 0
                cell = np.array([x*self.tile_size + self.queue_width, (y + centering_vert) * self.tile_size]) + self.board_border
                if tile.type[:5] == "start":
                    for k in tile.transition.keys():
                        self.fill_pipe2(0.0, k, tile.transition[k], cell, self.tile_size, (0,0,0))
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
        # render the queue
        for position, tile in enumerate(reversed(next_tiles[:5])):
            #queue_tile_size = self.tile_size
            queue_tile_size = min((self.height-self.board_border) // 5, self.tile_size)
            y_offset = (self.height - 5 * queue_tile_size) // 2

            #cell = np.array([self.queue_width // 2 - (queue_tile_size // 4), position*queue_tile_size + y_offset])
            w_start = (self.queue_width + self.board_border) // 2 - self.tile_size // 2
            h_start = (position*queue_tile_size + y_offset)
            cell = np.array([w_start, h_start])
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
                    self.fill_pipe2(0.0, k, tile.transition[k], cell, queue_tile_size, color)
            self.window.blit(
                pygame.transform.scale(PIPE_IMG[tile.type], (queue_tile_size, queue_tile_size)),
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

    def refresh_values(self, board):
        info = pygame.display.Info()
        screen_ratio = 0.8
        screen_width, screen_height = info.current_w * screen_ratio, info.current_h * screen_ratio
        screen_width = min(screen_width, self.window_size)
        #screen_height = min(screen_height, self.window_size)
        queue_width_in_tiles = 2
        board_border_in_tiles = 0.5

        width_in_tiles = board.width + queue_width_in_tiles + board_border_in_tiles * 2
        height_in_tiles = max(board.height, 5) + board_border_in_tiles * 2
        if width_in_tiles >= height_in_tiles:
            self.width = min(screen_width, self.window_size)
            self.height = int((height_in_tiles/width_in_tiles) * self.width)
            self.tile_size = self.width / width_in_tiles
        else:
            self.height = min(screen_height, self.window_size)
            self.width = int(((width_in_tiles)/height_in_tiles) * self.height)
            self.tile_size = self.height / height_in_tiles

        self.queue_width = self.tile_size * queue_width_in_tiles
        self.board_border = self.tile_size * board_border_in_tiles

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

