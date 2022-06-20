import gym
import gym_pipedream
from gym_pipedream.grid_elements import *
from gym_pipedream.envs.pipedream_env import PipeDreamEnv
import random
import pygame

def test_random_agent(steps=100):
    env = gym.make("PipeDream-v0")
    env.reset()
    env.render()
    for e in range(steps):
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        env.render()
        if done:
            break
    env.close()

def test_working_loop(steps=100, pipe_capacity=5):
    random.seed(0)
    env = PipeDreamEnv(render_mode="human", pipe_capacity=pipe_capacity)
    state = env.reset()
    env.render()
    env.next_tiles = [LeftUpPipe(), CrossPipe(), RightDownPipe(), LeftDownPipe(), LeftUpPipe(), HorizontalPipe()]
    actions = [[7,6], [7,5], [7,4], [8,4], [8,5], [6,5]]
    env.current_tile = env.next_tiles[0]
    for i in range(100):
        action = env.action_space.sample()
        if i in range(len(actions)):
            action = actions[i]
        else:
            action = [random.randrange(0, 6) for i in range(2)]
        state, reward, done, info = env.step(action)
        env.render()
        if done:
            break
    env.close()

def test_5x5_board(steps=100):
    env = gym.make("PipeDream-v0", width=5, height=5)
    env.reset()
    env.render()
    for e in range(steps):
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        env.render()
        if done:
            break
    env.close()

def test_minimum_3x3_board(steps=100):
    env = gym.make("PipeDream-v0", width=3, height=3)
    env.reset()
    env.render()
    for e in range(steps):
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        env.render()
        if done:
            break
    env.close()

def test_20x20_board(steps=100):
    env = gym.make("PipeDream-v0", width=20, height=20)
    env.reset()
    env.render()
    for e in range(steps):
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        env.render()
        if done:
            break
    env.close()

def test_pipe_capacity_10(steps=100):
    test_working_loop(pipe_capacity=5)

def test_pipe_capacity_5(steps=100):
    test_working_loop(pipe_capacity=4)

def test_pipe_capacity_2(steps=100):
    test_working_loop(pipe_capacity=3)

def test_pipe_capacity_1(steps=100):
    test_working_loop(pipe_capacity=2)

if __name__=="__main__":
    print("Starting capacity 5 test")
    test_pipe_capacity_5()
    #print("Starting capacity 4 test")
    #test_pipe_capacity_4()
    #print("Starting capacity 3 test")
    #test_pipe_capacity_3()
    #print("Starting capacity 2 test")
    #test_pipe_capacity_2()
    #print("Starting capacity 1 test")
    #test_pipe_capacity_1()