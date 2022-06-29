import gym
from gym_pipedream.grid_elements import *
from gym_pipedream.envs.pipedream_env import PipeDreamEnv
from gym_pipedream.wrappers import DelayedRewardWrapper
from gym_pipedream.wrappers import ImageObservation
from gym_pipedream.wrappers import GrayScaleObservation
from gym_pipedream.wrappers import SimplifiedImageObservation
from test_human_render import get_gif
import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from gym_pipedream.wrappers.gray_scale_observation import GrayScaleObservation

def random_wrapper_test(wrappers=None):

    env = gym.make("PipeDream-v0")
    if wrappers is not None:
        for wrapper in wrappers:
            env = wrapper(env)
    env.reset()
    total_reward = 0
    for e in range(100):
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        total_reward += reward
        env.render()
        if done:
            break
    env.close()
    return total_reward, state, reward, done, info


def core_wrappers(wrappers=None, actions = [[7,6], [7,5], [7,4],[8,4],[8,5],[6,5]], pipe_capacity=5, render_gif=False):
    random.seed(0)
    env = gym.make("PipeDream-v0", render_mode="human", pipe_capacity=pipe_capacity)

    if wrappers is not None:
        for wrapper in wrappers:
            env = wrapper(env)

    state = env.reset()
    #env.render()
    x = env
    while hasattr(x, "env"):
        x = x.env
    x.next_tiles = [LeftUpPipe(), CrossPipe(), RightDownPipe(), LeftDownPipe(), LeftUpPipe(), HorizontalPipe()]
    x.current_tile = env.next_tiles[0]

    total_reward = 0

    for i in range(100):
        if i in range(len(actions)):
            action = actions[i]
        else:
            action = [random.randint(0,5), random.randint(0,4)]
        state, reward, done, info = env.step(action)
        if render_gif:
            if wrappers[0]==GrayScaleObservation:
                matplotlib.image.imsave("temp{}.png".format(i), state, cmap="gray")
                #pygame.image.save(env.renderer.window, "temp{}.png".format(i))
            else:
                matplotlib.image.imsave("temp{}.png".format(i), state)
        total_reward += reward
        #env.render()
        if done:
            print("Game Over!")
            break
    env.close()
    return total_reward, state, reward, done, info

def test_delayed_reward(test_bed = core_wrappers, render_gif=False):
    total_reward, state, reward, done, info = test_bed([DelayedRewardWrapper], render_gif=render_gif)
    print("state = ", state)
    print("reward = ", reward)
    print("done = ", done)
    print("info = ", info, end="\n\n")
    assert total_reward == -3

def test_default_reward(test_bed = core_wrappers, render_gif=False):
    total_reward, state, reward, done, info = test_bed(render_gif=render_gif)
    print("state = ", state)
    print("reward = ", reward)
    print("done = ", done)
    print("info = ", info)
    print(total_reward, end="\n\n")
    assert total_reward == 29

def test_image_state(test_bed = core_wrappers, render_gif=False):
    total_reward, state, reward, done, info = test_bed([ImageObservation], render_gif=render_gif)
    print("state = ", state.shape)
    print("reward = ", reward)
    print("done = ", done)
    print("info = ", info, end="\n\n")
    img = np.array(state, dtype=int)
    plt.imshow(img)
    plt.show()

def test_image_grayscale_state(test_bed = core_wrappers, render_gif=False):
    #total_reward, state, reward, done, info = test_bed([ImageObservation, GrayScaleObservation])
    total_reward, state, reward, done, info = test_bed([GrayScaleObservation], render_gif=render_gif)
    print("state = ", state.shape)
    print("reward = ", reward)
    print("done = ", done)
    print("info = ", info, end="\n\n")
    img = np.array(state, dtype=int)
    plt.imshow(img, cmap="gray")
    plt.show()

def test_simplified_state(test_bed = core_wrappers, render_gif=False):
    total_reward, state, reward, done, info = test_bed([SimplifiedImageObservation], pipe_capacity = 3, render_gif=render_gif)
    print("state = ", state.shape)
    print("reward = ", reward)
    print("done = ", done)
    print("info = ", info, end="\n\n")
    img = np.array(state, dtype=int)
    plt.imshow(img)
    plt.show()

if __name__ == "__main__":
    #test_default_reward()
    #test_delayed_reward()
    #test_image_state()
    #test_image_grayscale_state()
    get_gif(test_simplified_state, "simplified_observation.gif")
    get_gif(test_image_grayscale_state, "grayscale_observation.gif")
    get_gif(test_image_state, "image_observation.gif")
    
    # test to make sure that there are no layered requirements between applications of wrappers
    #test_image_grayscale_state(random_wrapper_test)