import gymnasium as gym
from gymnasium import spaces
import numpy as np
from gym_pipedream.grid_elements import *
from gym_pipedream.rendering import Renderer

# ENV_DEFAULTS = {
#     "render_mode":      "human",
#     "width":            10,
#     "height":           7,
#     #"pipe_capacity":    7,
#     "pipe_capacity":    3,
#     "rewards":          {
#         "spill": -10,
#         "new_pipe": 1
#     },
#     "print_width":      50,
#     "window_size":      600,
#     "obs_low":          -2,
#     "obs_high":         15,
#     "tile_queue_len":   5,
#     "render_fps":       1,
# }

class PipeDreamEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array", "ascii"], "render_fps": 4}

    def __init__(self, **kwargs):
        for key in ENV_DEFAULTS.keys():
            if key in kwargs.keys():
                setattr(self, key, kwargs.get(key))
            else:
                setattr(self, key, ENV_DEFAULTS[key])


        self.board = Board(self.width, self.height, self.pipe_capacity, 0, self.render_mode, print_width=self.print_width)
        self.pipe_capacity = self.pipe_capacity
        self.next_tiles = [None] * self.tile_queue_len
        self.current_tile = None

        # observation space consists of grid representing every square
        #self.observation_space = spaces.Box(low=self.obs_low, high=self.obs_high, shape=(self.width, self.height), dtype=np.int8)
        self.observation_space = spaces.Box(low=self.obs_low, high=self.obs_high, shape=(self.width * self.height + 1, 2), dtype=np.int8)
        # one action for each position on the grid
        self.action_space = spaces.MultiDiscrete([self.width, self.height])
        self.rewards = self.rewards

        if "obs_mode" not in kwargs.keys():
            self.obs_mode = "default"
        else:
            self.obs_mode = kwargs["obs_mode"]

        # handle the pygame render if render mode is human
        if self.render_mode in ["human", "rgb_array"]:
            self.renderer = Renderer(self.window_size, self.render_fps, render_mode=self.render_mode)
        # Potentially include a curses rendering **

    def reset(self, seed=None, return_info=False, options=None):
        super().reset(seed=seed) # seed self.np_random
        if seed is not None:
            self.board.set_seed(seed)
        # Reset the board
        self.board.reset_board()

        # init walls if any

        # init list of next tiles
        self.next_tiles = [self.np_random.choice(PLAYING_TILES)(state=self.pipe_capacity) for i in range(self.tile_queue_len)]
        self.current_tile = self.next_tiles[0]

        return self._get_observation(), {}

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
            self.next_tiles.append(self.np_random.choice(PLAYING_TILES)(state=self.pipe_capacity))
            self.current_tile = self.next_tiles[0]

        pipe_filled, done = self.board.calc_next_state()
        #self.board.calc_next_state()
        next_state = self._get_observation()
        reward = -10 if done else self._get_reward()
        info = self._get_info(pipe_filled)

        return next_state, reward, done, False, info

    def render(self, mode=None, simplified=False):
        if mode == None:
            mode = self.render_mode
        if mode in ["human", "rgb_array"]:
            return self.renderer.render(self.board, self.next_tiles, mode=mode, simplified=simplified)
        else:
            print(self.board)
            print("")

    def _get_observation(self):
        if self.obs_mode == "default":
            x = np.array([np.array([0,0]) for i in range(len(self.board.get_tiles())+1)], dtype=np.int8)

            #print("board tiles = ", self.board.get_tiles())
            
            for i in range(len(self.board.get_tiles())):
                #print("len thing = ", len(self.board.get_tiles()))
                #print("encoding = ", self.board.get_tiles()[i].get_encoding())
                # if type(self.board.get_tiles()[i].get_encoding()[1]) != np.int8 or type(self.board.get_tiles()[i].get_encoding()[0]) != np.int8:
                #     print(":ASJKHFLKJHASFLKASJHFLKASJFHLK")
                #     print("type = ", type(self.board.get_tiles()[i].get_encoding()[0]))
                x[i][0], x[i][1] = self.board.get_tiles()[i].get_encoding()
                # if type(x[i][0]) != np.int8 or type(x[i][1]) != np.int8:
                #     print("type for first: ", type(x[i][0]))
                #     print("type for second: ", type(x[i][1]))
                #     print("LLLLLLLLLLLLLLLLLLLLLLLLLL")

            x[-1][0], x[-1][1] = self.current_tile.get_encoding()

            # print("type(x[-1][1]) = ", type(x[-1][1]))
            # print("x: ", x.shape)
            # print("obs shape: ", self.observation_space.shape)
            # print("x type: ", type(x))
            # print("obs type: ", type(self.observation_space))

            #return np.array([tile.get_encoding() for tile in self.board.get_tiles()]+[self.current_tile.get_encoding()[0]])
            tmp = [tile.get_encoding() for tile in self.board.get_tiles()]+[self.current_tile.get_encoding()[0]]
            #print("tmp shape = ", len(tmp))
            #print("tmp = ", tmp)
            tmp = [np.array([[tile.get_encoding()[0],tile.get_encoding()[1]]]) for tile in self.board.get_tiles()]
            #print("new temp = ", tmp)
            tmp = tmp + [np.array([self.current_tile.get_encoding()[0], 0], dtype=np.int8)]
            
            #x = np.array(tmp, dtype=np.int8)
            #x = np.array(tmp)
            #print("x shape = ", x.shape)
            #print("obs shape = ", self.observation_space.shape)
            #if True:
            #    return np.array([np.array([0,0]) for i in range(71)], dtype=np.int8)
            #x.astype(np.int8)
            return x
        else:
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
        if self.render_mode in ["human", "rgb_array"]:
            self.renderer.close()


if __name__ == "__main__":
    #env = PipeDreamEnv(render_mode="human", window_size=900)
    env = PipeDreamEnv(render_mode="human")
    #env = PipeDreamEnv(render_mode="ascii", window_size=600)
    state, info = env.reset(seed=0)
    env.render()

    env.next_tiles = [LeftUpPipe(), CrossPipe(), RightDownPipe(), LeftDownPipe(), RightUpPipe(), LeftUpPipe(), HorizontalPipe()]
    env.current_tile = env.next_tiles[0]

    #env.render()
    actions = [[8, 5], [7, 5], [6, 5], [7, 4], [6, 6], [7, 6], [6, 4]]
    for i in range(100):
        action = env.action_space.sample()
        if i < len(actions):
            action = actions[i] # x, y

        print("action = ", action)
        print("next tiles = ", [t.type for t in env.next_tiles])
        print("start state = ", env.board.tiles[2].state)
        state, reward, done, truncated, info = env.step(action)
        env.render()
        if done:
            print("Game Over!")
            break

    print("start state = ", env.board.tiles[42].state)
