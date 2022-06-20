import gym
import gym_pipedream
from gym_pipedream.grid_elements import *
from gym_pipedream.envs.pipedream_env import PipeDreamEnv
import random
import pygame
import numpy as np
import subprocess, os
import glob

def test_random_agent_render(steps=100):
    env = gym.make("PipeDream-v0")
    env.reset()
    env.render()
    for e in range(steps):
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        env.render()
        if done:
            break
    print("env.render_mode = ", env.render_mode)
    env.close()

def test_working_loop(steps=100, debug=False, **kwargs):
    random.seed(0)
    #env = PipeDreamEnv(**kwargs)
    env = gym.make("PipeDream-v0", **kwargs)
    state = env.reset()
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
        if debug:
            pygame.image.save(env.renderer.window, "temp{}.png".format(i))
        if done:
            last_state = env.render()
            break

    c = get_cell_center_col(env, 6, 5, last_state)
    # check that the end of the loop contains water
    assert np.array_equal(c, [9, 195, 255])
    env.close()

def get_cell_center_col(env, x, y, last_state):
    queue_width = env.renderer.queue_width
    tile_size = (env.renderer.width - env.renderer.board_border) // env.board.width
    cell = np.array([x*tile_size + queue_width, y * tile_size]) + env.renderer.board_border // 2
    center = np.array([cell[0] + tile_size // 2, cell[1] + tile_size // 2])
    return last_state[center[1]][center[0]]

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

def test_pipe_capacity_10():
    test_working_loop(pipe_capacity=10, render_fps=8)

def test_pipe_capacity_2():
    test_working_loop(pipe_capacity=2)

def test_pipe_capacity_1():
    test_working_loop(pipe_capacity=1)

def convert_to_gif():
    directory = os.path.dirname(os.path.realpath(__file__))
    num_frames = 200
    filename_list = [os.path.join(directory, "temp" + str(n) + ".png") for n in range(num_frames)]

    random.seed(0)
    env = gym.make("PipeDream-v0")
    state = env.reset()
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
        pygame.image.save(env.renderer.window, "temp{}.png".format(i))
        if done:
            last_state = env.render()
            break


        #pygame.image.save(env.renderer.window, filename_list[e])
    anim_seconds = 5
    seconds_per_frame = anim_seconds / num_frames
    frame_delay = str(int(seconds_per_frame * 100))
    command_list = ["convert", "-delay", frame_delay, "-loop", "0"] + filename_list + ["anim.gif"]
    subprocess.call(command_list, cwd=directory)
    for filename in filename_list:
        os.remove(filename)
    env.close()

def get_gif(func, gif_name):
    directory = os.path.dirname(os.path.realpath(__file__))
    num_frames = 200
    filename_list = [os.path.join(directory, "temp" + str(n) + ".png") for n in range(num_frames)]

    func(200, debug=True)

    anim_seconds = 5
    # glob the files with the specified regex sorted by time created
    files = sorted(glob.glob("temp?*.png"), key=os.path.getmtime)
    files = [os.path.join(directory, file) for file in files]
    seconds_per_frame = anim_seconds / num_frames
    print("seconds_per_frame = ", seconds_per_frame)
    frame_delay = str(int(seconds_per_frame * 500))
    print("frame_delay = ", frame_delay)
    #frame_delay = 2
    frame_delay = "120"
    print("filename_list = ", filename_list)
    print("files = ", files)
    command_list = ["convert", "-delay", frame_delay, "-loop", "0"] + files + [gif_name]
    subprocess.call(command_list, cwd=directory)
    for filename in files:
        os.remove(filename)


if __name__=="__main__":
    get_gif(test_working_loop, "test_working_loop.gif")
    #convert_to_gif()
    #test_working_loop(render_fps=8)
    #print("Starting capacity 4 test")
    #test_pipe_capacity_4()
    #print("Starting capacity 3 test")
    #test_pipe_capacity_3()
    #print("Starting capacity 2 test")
    #test_pipe_capacity_2()
    #print("Starting capacity 1 test")
    #test_pipe_capacity_1()