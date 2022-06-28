import gym
from gym_pipedream.grid_elements import *
from gym_pipedream.envs.pipedream_env import PipeDreamEnv
from gym_pipedream.wrappers import DelayedRewardWrapper
from gym_pipedream.wrappers import ImageObservation
import random


def core_wrappers(wrapper=None, actions = [[7,6], [7,5], [7,4],[8,4],[8,5],[6,5]], pipe_capacity=5):
    random.seed(0)
    env = gym.make("PipeDream-v0", render_mode="human", pipe_capacity=pipe_capacity)

    if wrapper is not None:
        env = wrapper(env)

    state = env.reset()
    #env.render()
    if wrapper is not None:
        env.env.next_tiles = [LeftUpPipe(), CrossPipe(), RightDownPipe(), LeftDownPipe(), LeftUpPipe(), HorizontalPipe()]
        env.env.current_tile = env.next_tiles[0]
    else:  
        env.next_tiles = [LeftUpPipe(), CrossPipe(), RightDownPipe(), LeftDownPipe(), LeftUpPipe(), HorizontalPipe()]
        env.current_tile = env.next_tiles[0]

    total_reward = 0

    for i in range(100):
        if i in range(len(actions)):
            action = actions[i]
        else:
            action = [random.randint(0,5), random.randint(0,4)]
        state, reward, done, info = env.step(action)
        total_reward += reward
        #env.render()
        if done:
            print("Game Over!")
            break
    env.close()
    return total_reward, state, reward, done, info

def test_delayed_reward():
    total_reward, state, reward, done, info = core_wrappers(DelayedRewardWrapper)
    print("state = ", state)
    print("reward = ", reward)
    print("done = ", done)
    print("info = ", info, end="\n\n")
    assert total_reward == -3

def test_default_reward():
    total_reward, state, reward, done, info = core_wrappers()
    print("state = ", state)
    print("reward = ", reward)
    print("done = ", done)
    print("info = ", info)
    print(total_reward, end="\n\n")
    assert total_reward == 29

def test_image_state():
    total_reward, state, reward, done, info = core_wrappers(ImageObservation)
    print("state = ", state.shape)
    print("reward = ", reward)
    print("done = ", done)
    print("info = ", info, end="\n\n")


if __name__ == "__main__":
    test_default_reward()
    test_delayed_reward()
    test_image_state()