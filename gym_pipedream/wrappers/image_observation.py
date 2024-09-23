
import numpy as np
import gymnasium as gym
from gym_pipedream.rendering import Renderer
from gymnasium import spaces


class ImageObservation(gym.ObservationWrapper):

    def __init__(self, env):
        super().__init__(env)
        self._obs_renderer = Renderer(self.window_size, self.render_fps, render_mode="rgb_array")
        # Have to call this to ensure the _obs_renderer has height and width calculated.
        self._obs_renderer.refresh_values(self.board)# TODO: Maybe standardise the width and height.
        self.observation_space = spaces.Box(low=0, high=255, shape=(self._obs_renderer.height, self._obs_renderer.width, 3), dtype=np.uint8)

    def observation(self, obs):
        obs = self._obs_renderer.render(self.board, self.next_tiles, mode="rgb_array", simplified=False)
        return obs
