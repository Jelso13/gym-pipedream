import gym
from gym import spaces
import numpy as np
import random
from typing import Optional
from gym_pipedream.grid_elements import *

BOARD_WIDTH = 10
BOARD_HEIGHT = 7

OBS_LOW = -2
OBS_HIGH = 10

class PipeDreamEnv(gym.Env):
    # CHANGE THE METADATA
    metadata = {"render_modes": ["human", "rgb_array", "ascii"], "render_fps": 4}

    def __init__(self, render_mode: Optional[str] = None, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT):

        self.width = width  # width of the playing area
        self.height = height  # height of the playing area
        self.window_size = 512  # The size of the PyGame window

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

    def reset(self, seed=None, return_info=False, options=None):
        super().reset(seed=seed) # seed self.np_random

        # init tap location
        tap_location = get_random_location()
        while self.valid_tap()

        # init walls if any

        # init list of next blocks

    def valid_tap():
        return 

    def get_random_location(self, min_width=0, max_width=BOARD_WIDTH-1, min_height=0, max_height=BOARD_HEIGHT-1):
        return (random.randint(1,BOARD_WIDTH-2), random.randint(1,BOARD_HEIGHT-2))


                

if __name__ == "__main__":
    env = PipeDreamEnv()
    print(env.observation_space.shape)