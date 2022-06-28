import gym
from . import ImageObservation

class GrayScaleObservation(gym.ObservationWrapper):
    def __init__(self, env):
        env = ImageObservation(env)
        super().__init__(env)

    def observation(self, obs):
        import cv2
        obs = cv2.cvtColor(obs, cv2.COLOR_RGB2GRAY)
        return obs
