import gym
from gym.envs.registration import register
import gym_pipedream
from gym_pipedream.wrappers import SimplifiedImageObservation

def default_env():
    env = gym.make('PipeDream-v0')
    #env = GrayScaleObservation(env)
    env = SimplifiedImageObservation(env)
    return env

#register(
#    'PipeDream-v1',
#    entry_point = 'gym_pipedream.envs:default_env'
#)
