import gym
from gym_pipedream.grid_elements import *
from gym_pipedream.envs.pipedream_env import PipeDreamEnv
from gym_pipedream.wrappers import DelayedRewardWrapper
import random


def core_wrappers(wrapper, actions = [[7,6], [7,5], [7,4],[8,4],[8,5],[6,5]], pipe_capacity=5):
    random.seed(0)
    env = gym.make("PipeDream-v0", render_mode="ascii", pipe_capacity=pipe_capacity)

    env = wrapper(env)

    state = env.reset()
    env.render()
    env.env.next_tiles = [LeftUpPipe(), CrossPipe(), RightDownPipe(), LeftDownPipe(), LeftUpPipe(), HorizontalPipe()]
    env.env.current_tile = env.next_tiles[0]

    total_reward = 0

    for i in range(100):
        if i in range(len(actions)):
            action = actions[i]
            env.current_tile = LeftUpPipe()
        else:
            action = [random.randint(0,5), random.randint(0,4)]
        state, reward, done, info = env.step(action)
        total_reward += reward
        env.render()
        if done:
            print("Game Over!")
            break
    print("total reward = ", total_reward)
    return total_reward

def test_delayed_reward():
    total_reward = core_wrappers(DelayedRewardWrapper)
    assert total_reward == -3


if __name__ == "__main__":
    test_delayed_reward()