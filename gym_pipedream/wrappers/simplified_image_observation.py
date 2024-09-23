import gymnasium as gym
from gym_pipedream.rendering import Renderer
from gymnasium import spaces
import numpy as np

class SimplifiedImageObservation(gym.ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        self._obs_renderer = Renderer(self.window_size, self.render_fps, render_mode="rgb_array")
        # This is taken from what is calculated in Renderer._render_simplified.
        #  TODO: Decouple this when simplified rendering is fixed.
        self.width = self.board.width * 3
        self.height = self.board.height * 3
        self.observation_space = spaces.Box(low=0, high=255,shape=(self.height, self.width, 3), dtype=np.uint8)

    def observation(self, obs):
        obs = self._obs_renderer.render(self.board, self.next_tiles, mode="rgb_array", simplified=True)
        return obs
