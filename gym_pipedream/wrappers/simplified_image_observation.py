import gymnasium as gym
from . import ImageObservation

class SimplifiedImageObservation(gym.ObservationWrapper):
    def __init__(self, env):
        #env = ImageObservation(env)
        super().__init__(env)

    def observation(self, obs):
        #obs = self.env.render(mode="rgb_array", simplified=True)
        obs = self.env.render(mode="rgb_array", simplified=True)
        return obs
