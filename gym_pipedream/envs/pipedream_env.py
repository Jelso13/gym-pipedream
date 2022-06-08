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

    def __init__(self, render_mode: Optional[str] = None, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT):

        self.width = width  # width of the playing area
        self.height = height  # height of the playing area
        self.window_size = 512  # The size of the PyGame window
        #self.board = [[(0, 'none') for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)]
        self.board = [Floor()] * BOARD_WIDTH * BOARD_HEIGHT

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

        # init tap location
        self.init_tap()

        # init walls if any

        # init list of next blocks

    def init_tap(self):
        tap_location = list(self.get_random_location())
        tap_direction = self.get_valid_tap_direction(tap_location)
        self.set_board_position(tap_location, Starting(direction=tap_direction))


    def get_valid_tap_direction(self, location, return_directions=False):
        edges = [0, BOARD_WIDTH-1, BOARD_HEIGHT-1]
        directions = ["up", "right", "down", "left"]
        x,y = location
        if x == 0:
            directions.pop(3)
        if y == 0:
            directions.pop(0)
        if x == edges[1]:
            directions.pop(1)
        if y == edges[2]:
            directions.pop(2)
        if return_directions: return (random.choice(directions), directions)
        return random.choice(directions)

    def get_random_location(self, min_width=0, max_width=BOARD_WIDTH-1, min_height=0, max_height=BOARD_HEIGHT-1):
        return (random.randint(min_width, max_width), random.randint(min_height, max_height))

    def set_board_position(self, loc, obj):
        self.board[loc[1]*BOARD_WIDTH + loc[0]] = obj

    def print_board(self):
        print("-"*130)
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                #print("| {:^10s} ".format(self.board[i*BOARD_WIDTH + j].type), end="")
                print("| {:^10s} ".format(ENCODE_ASCII[self.board[i*BOARD_WIDTH + j].type]), end="")
            print("|\n" + "-"*130)


if __name__ == "__main__":
    env = PipeDreamEnv()
    state = env.reset()
    env.print_board()
    print(env.observation_space.shape)