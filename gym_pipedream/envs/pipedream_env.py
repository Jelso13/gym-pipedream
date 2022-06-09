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
    metadata = {"render_modes": ["human", "rgb_array", "ascii", "descriptive"], "render_fps": 4}

    def __init__(self, render_mode = "ascii", width = BOARD_WIDTH, height = BOARD_HEIGHT):
        assert render_mode in self.metadata["render_modes"]

        self.render_mode = render_mode

        self.board = Board(width, height, render_mode)
        self.next_tiles = [None] * TILE_QUEUE_LEN
        self.current_tile = None

        # observation space consists of grid representing every square
        self.observation_space = spaces.Box(low=OBS_LOW, high=OBS_HIGH, shape=(width, height), dtype=np.int8)
        # one action for each position on the grid
        self.action_space = spaces.MultiDiscrete([width, height])
        
        self.window_size = 512  # The size of the PyGame window

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
        self.board.reset_board()

        # init tap location
        self.board.init_tap()

        # init walls if any

        # init list of next tiles
        self.next_tiles = [random.choice(PLAYING_TILES)() for i in range(TILE_QUEUE_LEN)]
        self.current_tile = self.next_tiles[-1]

        return self._get_observation()

    def step(self, action):
        """
        This method takes an action in the current state by 
        placing/replacing a block on the grid then returns the 
        new state, the reward obtained and whether the next 
        state is terminal.

        actions are enumerated from 0 to board_width * board_height - 1 corresponding to grid positions
        """
        assert action >= 0 and action <= self.width * self.height -1 

        """
        if possible action:
            modify the board
            determine the reward given a get_reward method ** when new pipe fills then give reward next action
            determine if the environment is done (the pipe has failed)
            get the observation of the new state
            return all
        """


        raise NotImplementedError

    def render(self):
        if self.render_mode == "ascii":
            print(self.board)
        else:
            raise NotImplementedError

    def _get_observation(self):
        return {"board":[tile.get_encoding() for tile in self.board.get_tiles()], "current_tile": self.current_tile.get_encoding()}


    def set_board_position(self, loc, obj):
        self.board[loc[1]*self.width + loc[0]] = obj


if __name__ == "__main__":
    env = PipeDreamEnv(render_mode="ascii")
    state = env.reset()
    env.render()
    #print(state)
    #print(env.observation_space.shape)