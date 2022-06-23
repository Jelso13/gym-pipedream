import gym
from gym import spaces
import numpy as np
import random
from typing import Optional
from gym_pipedream.grid_elements import *
from gym_pipedream.rendering import Renderer


class PipeDreamEnv(gym.Env):

    def __init__(self, **kwargs):
        for key in ENV_DEFAULTS.keys():
            if key in kwargs.keys():
                setattr(self, key, kwargs.get(key))
            else:
                setattr(self, key, ENV_DEFAULTS[key])

        self.board = Board(self.width, self.height, self.pipe_capacity, self.render_mode, print_width=self.print_width)
        self.pipe_capacity = self.pipe_capacity
        self.next_tiles = [None] * self.tile_queue_len
        self.current_tile = None

        # observation space consists of grid representing every square
        self.observation_space = spaces.Box(low=self.obs_low, high=self.obs_high, shape=(self.width, self.height), dtype=np.int8)
        # one action for each position on the grid
        self.action_space = spaces.MultiDiscrete([self.width, self.height])
        self.rewards = self.rewards
        

        # handle the pygame render if render mode is human
        if self.render_mode == "human":
            self.renderer = Renderer(self.window_size, self.render_fps)
        # Potentially include a curses rendering **

    def reset(self, seed=0, return_info=False, options=None):
        #super().reset(seed=seed) # seed self.np_random

        # Reset the board
        self.board.reset_board()

        # init walls if any

        # init list of next tiles
        self.next_tiles = [random.choice(PLAYING_TILES)(state=self.pipe_capacity) for i in range(self.tile_queue_len)]
        self.current_tile = self.next_tiles[0]

        return self._get_observation()

    def step(self, action):
        """
        This method takes an action in the current state by 
        placing/replacing a block on the grid then returns the 
        new state, the reward obtained and whether the next 
        state is terminal.

        actions are enumerated from 0 to board_width * board_height - 1 corresponding to grid positions
        """

        """
        if possible action:
            modify the board
            determine the reward given a get_reward method ** when new pipe fills then give reward next action
            determine if the environment is done (the pipe has failed)
            get the observation of the new state
            return all
        """

        # set the action if possible  
        if self.board.set_tile(action, self.current_tile):
            self.next_tiles.pop(0)
            self.next_tiles.append(random.choice(PLAYING_TILES)(state=self.pipe_capacity))
            self.current_tile = self.next_tiles[0]
        

        pipe_filled, done = self.board.calc_next_state()
        #self.board.calc_next_state()
        next_state = self._get_observation()
        reward = self._get_reward()
        info = self._get_info(pipe_filled)

        return next_state, reward, done, info

    def render(self, mode="human"):
        if self.render_mode in ["human", "rgb_array"]:
            return self.renderer.render(self.board, self.next_tiles)
        else:
            print(self.board)
            print("")

    def _get_observation(self):
        return {
            "board":[tile.get_encoding() for tile in self.board.get_tiles()],
            "next_tile_queue": [tile.get_encoding()[0] for tile in self.next_tiles], 
            "current_tile": self.current_tile.get_encoding()[0]
        }

    def _get_info(self, pipe_filled):
        return {
            "pipe_filled": pipe_filled
            }
    
    def _get_reward(self):
        return 1

    def set_board_position(self, loc, obj):
        self.board[loc[1]*self.width + loc[0]] = obj

    def close(self):
        self.renderer.close()


if __name__ == "__main__":
    random.seed(0)
    #env = PipeDreamEnv(render_mode="human", window_size=900)
    env = PipeDreamEnv(width=5, height=5, render_mode="human")
    #env = PipeDreamEnv(render_mode="ascii", window_size=600)
    state = env.reset()
    env.render()

    env.next_tiles = [LeftUpPipe(), CrossPipe(), RightDownPipe(), LeftDownPipe(), LeftUpPipe(), HorizontalPipe()]
    env.current_tile = env.next_tiles[0]

    #env.render()
    for i in range(100):
        action = env.action_space.sample()
        if i == 0:
            action = [7,6]
        if i == 1:
            action = [7,5]
        if i == 2:
            action = [7,4]
        if i == 3:
            random.seed(0)
            action = [8,4]
        if i == 4:
            action = [8,5]
        if i == 5:
            action = [6,5]
        
        print("action = ", action)
        print("next tiles = ", [t.type for t in env.next_tiles])
        print("start state = ", env.board.tiles[42].state)
        state, reward, done, info = env.step(action)
        env.render()
        if done:
            print("Game Over!")
            break

    print("start state = ", env.board.tiles[42].state)