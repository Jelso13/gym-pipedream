import gymnasium as gym
import gym_pipedream
from gym_pipedream.grid_elements import *
from gym_pipedream.envs.pipedream_env import PipeDreamEnv

#from gym.wrappers.compatibility import EnvCompatibility
import random
from gym_pipedream.wrappers import ImageObservation, GrayScaleObservation
from gym_pipedream.envs.pipedream_env import PipeDreamEnv

#from stable_baselines.deepq.policies import MlpPolicy
#from stable_baselines import DQN

def test_random_agent(steps=100):
    #env = gym.make("PipeDream-v0")
    env = gym.make("PipeDream-v1")
    env.reset()
    #env.render()
    for e in range(steps):
        action = env.action_space.sample()
        #print("action = ", action)
        state, reward, done, truncated, info = env.step(action)
        env.render()
        #print("state = ", state)
        #print("reward = ", reward)
        if done:
            break
    # print("state =", state)

def test_ppo():
    # stable baselines 3
    from stable_baselines3 import PPO
    from stable_baselines3.common.env_checker import check_env

    # env = GrayScaleObservation(ImageObservation(gym.make("PipeDream-v0", render_mode="human")))
    # env = gym.make("PipeDream-v1", pipe_capacity=2, render_gif=True)
    env = PipeDreamEnv(render_gif=True, width=4, height=3, pipe_capacity=5, render_mode="human", fixed_tap_location=True)
    # env = GrayScaleObservation(PipeDreamEnv(render_gif=True, width=4, height=3, pipe_capacity=5, render_mode="rgb_array"))
    # self.observation_space = gym.spaces.Box(low=0, high=255, shape=obs.shape, dtype=obs.dtype)
    # s,_ = env.reset()
    # env.observation_space = gym.spaces.Box(low=0, high=50, shape=s.shape, dtype=s.dtype)

    # check_env(env)
    env.reset()
    model = PPO("MlpPolicy", env, verbose=1)
    tsps = 1_000_000
    model.learn(total_timesteps=tsps, progress_bar=True)
    model.save("deepq_pipedream"+str(tsps))

    obs, info = env.reset()
    print(f"obs = {obs}")
    total_reward = 0
    for i in range(1000):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, truncated, info = env.step(action)
        total_reward += reward
        env.render()
        if done:
            obs,_ = env.reset()

    print(f"total reward = {total_reward}")

    #env.reset()

    #model = DQN(MlpPolicy, env, verbose=1)
    #model.learn(total_timesteps=25000)
    #model.save("deepq_pipedream")

    #obs = env.reset()
    #while True:
    #    action, _states = model.predict(obs)
    #    obs, rewards, dones, info = env.step(action)
    #    env.render()



if __name__=="__main__":
    #test_random_agent()
    test_ppo()
