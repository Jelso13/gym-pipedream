import gymnasium as gym
import numpy as np

from gymnasium import spaces
class DiscreteActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = spaces.Discrete(int(self.width * self.height))

    def action(self, action):
        """
        Convert to original action space. int -> tuple[int, int]
        """
        coords = np.array([action % self.width, action // self.width]) # x, y coordinates.
        return coords
