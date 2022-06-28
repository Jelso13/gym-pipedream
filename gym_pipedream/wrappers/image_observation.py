import gym

class ImageObservation(gym.ObservationWrapper):

    def __init__(self, env):
        super().__init__(env)

    def observation(self, obs):
        obs = self.env.render(mode="rgb_array")
        return obs