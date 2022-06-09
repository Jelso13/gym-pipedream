import gym
from gym import spaces
import numpy as np
import random
from typing import Optional
from gym_pipedream.grid_elements import *

OBS_LOW = -2
OBS_HIGH = 10

class PipeDreamEnv(gym.Env):
    # CHANGE THE METADATA
    metadata = {"render_modes": ["human", "rgb_array", "ascii"], "render_fps": 4}

    def __init__(self, render_mode = "ascii", width = BOARD_WIDTH, height = BOARD_HEIGHT):
        assert render_mode in self.metadata["render_modes"]

        self.width = width  # width of the playing area
        self.height = height  # height of the playing area
        self.window_size = 512  # The size of the PyGame window
        #self.board = [[(0, 'none') for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)]
        self.board = [Floor()] * self.width * self.height
        self.next_tiles = [None] * TILE_QUEUE_LEN
        self.current_tile = None

        # observation space consists of grid representing every square
        self.observation_space = spaces.Box(low=OBS_LOW, high=OBS_HIGH, shape=(self.width, self.height), dtype=np.int8)

        # one action for each position on the grid
        self.action_space = spaces.MultiDiscrete([self.width, self.height])
        
        # handle the pygame render if render mode is human
        if render_mode == "human":
            import pygame  # import here to avoid pygame dependency

            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
            self.clock = pygame.time.Clock()
        # Potentially include a curses rendering **

    def reset(self, seed=0, return_info=False, options=None):
        #super().reset(seed=seed) # seed self.np_random

        # Reset the board
        self.board = [Floor()] * self.width * self.height

        # init tap location
        self.init_tap()

        # init walls if any

        # init list of next tiles
        self.next_tiles = [random.choice(PLAYING_TILES) for i in range(TILE_QUEUE_LEN)]
        self.current_tile = self.next_tiles[-1]

        return self._get_observation()

    def render(self):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def _get_observation(self):
        return {"board":[tile.get_encoding() for tile in self.board], "current_tile":self.current_tile.get_encoding()}

    def init_tap(self):
        tap_location = list(self.get_random_location())
        tap_direction = self.get_valid_tap_direction(tap_location)
        self.set_board_position(tap_location, Starting(direction=tap_direction))


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

    def set_board_position(self, loc, obj):
        self.board[loc[1]*self.width + loc[0]] = obj

    def print_board(self):
        print("-"*130)
        for i in range(self.height):
            for j in range(self.width):
                #print("| {:^10s} ".format(self.board[i*self.width + j].type), end="")
                print("| {:^10s} ".format(ENCODE_ASCII[self.board[i*self.width + j].type]), end="")
            print("|\n" + "-"*130)


if __name__ == "__main__":
    env = PipeDreamEnv()
    state = env.reset()
    env.get_random_location()
    env.print_board()
    print(state)

    print(env.observation_space.shape)