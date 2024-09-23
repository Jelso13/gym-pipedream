import gymnasium as gym
from gymnasium import spaces
import numpy as np
from . import ImageObservation

class GrayScaleObservation(gym.ObservationWrapper):
    def __init__(self, env):
        env = ImageObservation(env)
        super().__init__(env)
        self.observation_space = spaces.Box(low=0, high=255, shape=env.observation_space.shape[:2], dtype=np.uint8)

    def observation(self, obs):
        import cv2
        obs = cv2.cvtColor(obs, cv2.COLOR_RGB2GRAY)
        return obs
