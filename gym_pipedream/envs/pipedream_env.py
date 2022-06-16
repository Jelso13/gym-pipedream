import gym
from gym import spaces
import numpy as np
import random
from typing import Optional
from gym_pipedream.grid_elements import *
from gym_pipedream.rendering import Renderer

OBS_LOW = -2
OBS_HIGH = 10

class PipeDreamEnv(gym.Env):
    # CHANGE THE METADATA
    # human = pygame, rgb_array = curses, ascii = text descriptive = verbose.
    metadata = {"render_modes": ["human", "rgb_array", "ascii", "descriptive"], "render_fps": 4}

    def __init__(self, render_mode = "ascii", width = BOARD_WIDTH, height = BOARD_HEIGHT, pipe_capacity=PIPE_CAPACITY, rewards=REWARDS, print_width=PRINT_WIDTH, window_size=WINDOW_SIZE):
        assert render_mode in self.metadata["render_modes"]

        self.render_mode = render_mode

        self.board = Board(width, height, pipe_capacity, render_mode, print_width=print_width)
        self.pipe_capacity = pipe_capacity
        self.next_tiles = [None] * TILE_QUEUE_LEN
        self.current_tile = None

        # observation space consists of grid representing every square
        self.observation_space = spaces.Box(low=OBS_LOW, high=OBS_HIGH, shape=(width, height), dtype=np.int8)
        # one action for each position on the grid
        self.action_space = spaces.MultiDiscrete([width, height])
        self.rewards = rewards
        
        self.window_size = window_size  # The size of the PyGame window

        # handle the pygame render if render mode is human
        if render_mode == "human":
            self.renderer = Renderer(self.window_size)
        # Potentially include a curses rendering **

    def reset(self, seed=0, return_info=False, options=None):
        #super().reset(seed=seed) # seed self.np_random

        # Reset the board
        self.board.reset_board()

        # init walls if any

        # init list of next tiles
        self.next_tiles = [random.choice(PLAYING_TILES)(state=self.pipe_capacity) for i in range(TILE_QUEUE_LEN)]
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
        reward = self._get_reward(pipe_filled)
        info = self._get_info()

        return next_state, reward, done, info

    def render(self):
        if self.render_mode in ["human", "rgb_array"]:
            self.renderer.render(self.board)
        else:
            print(self.board)
            print("")

    #def _render_gui(self):
    #    import pygame
    #    if self.window is None:
    #        pygame.init()
    #        pygame.display.init()
    #        pygame.display.set_caption("Pipe Dream")
    #        if self.render_mode == "human":
    #            self.window = pygame.display.set_mode(WINDOW_SIZE)
    #        elif self.render_mode == "rgb_array":
    #            self.window = pygame.Surface(WINDOW_SIZE)
    #    if self.clock is None:
    #        self.clock = pygame.time.Clock()

    #    canvas = pygame.Surface((512, 512))
    #    
    #    canvas.fill((255, 255, 255))
    #    pix_square_size = (
    #        512 // self.board.width
    #    )  # The size of a single grid square in pixels

    #    self._target_location = [3,3]
    #    self._agent_location = [3,3]

    #    # First we draw the target
    #    pygame.draw.rect(
    #        canvas,
    #        (255, 0, 0),
    #        pygame.Rect(
    #            #pix_square_size * self._target_location,
    #            (3,3),
    #            (pix_square_size, pix_square_size),
    #        ),
    #    )
    #    # Now we draw the agent
    #    #pygame.draw.circle(
    #    #    canvas,
    #    #    (0, 0, 255),
    #    #    (self._agent_location) * pix_square_size,
    #    #    pix_square_size / 3,
    #    #)

    #    if self.render_mode == "human":
    #        # The following line copies our drawings from `canvas` to the visible window
    #        self.window.blit(canvas, canvas.get_rect())
    #        pygame.event.pump()
    #        pygame.display.update()

    #        # We need to ensure that human-rendering occurs at the predefined framerate.
    #        # The following line will automatically add a delay to keep the framerate stable.
    #        self.clock.tick(self.metadata["render_fps"])
    #    else:  # rgb_array
    #        return np.transpose(
    #            np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
    #        )

    def _get_observation(self):
        return {"board":[tile.get_encoding() for tile in self.board.get_tiles()], "current_tile": self.current_tile.get_encoding()}

    def _get_info(self):
        return {"next_tile_queue": [tile.get_encoding() for tile in self.next_tiles]}
    
    def _get_reward(self, pipe_filled=False):
        if pipe_filled:
            return 1
        
        return 0


    def set_board_position(self, loc, obj):
        self.board[loc[1]*self.width + loc[0]] = obj


if __name__ == "__main__":
    random.seed(0)
    env = PipeDreamEnv(render_mode="human", window_size=600)
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
    #print(state)
    #print(env.observation_space.shape)