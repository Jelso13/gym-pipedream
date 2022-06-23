import gym

class DelayedRewardWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)

    def step(self, action):
        obs, _, done, info = self.env.step(action)
        # if new pipe filled then reward = 1 else 0: (int(True) = 1)
        reward = -10 if done else int(info['pipe_filled'])
        return obs, reward, done, info
    def close(self):
        self.env.close()