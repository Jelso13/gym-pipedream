import gymnasium as gym
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
    env.reset(seed=0)
    env.render()
    for e in range(steps):
        action = env.action_space.sample()
        state, reward, done, truncated, info = env.step(action)
        env.render()
        if done:
            break
    print("env.render_mode = ", env.render_mode)
    env.close()

def test_working_loop(steps=100, render_gif=False, **kwargs):

    #env = PipeDreamEnv(**kwargs)
    env = gym.make("PipeDream-v0", **kwargs)
    state, _ = env.reset(seed=0)
    env.next_tiles = [LeftUpPipe(), CrossPipe(), RightDownPipe(), LeftDownPipe(), LeftUpPipe(), HorizontalPipe()]
    env.next_tiles[1].state2 = env.pipe_capacity
    actions = [[7,6], [7,5], [7,4], [8,4], [8,5], [6,5]]
    env.current_tile = env.next_tiles[0]
    for i in range(100):
        action = env.action_space.sample()
        if i in range(len(actions)):
            action = actions[i]
        else:
            action = [random.randrange(0, 6) for i in range(2)]
        env.render()
        state, reward, done, truncated, info = env.step(action)
        if render_gif:
            pygame.image.save(env.renderer.window, "temp{}.png".format(i))
        if done:
            last_state = env.render()
            break

    env.close()
    # check that the end of the loop contains water
    assert np.array_equal(get_cell_center_col(env, 6,5, last_state), [9, 195, 255])
    assert np.array_equal(get_cell_center_col(env, 7,5, last_state), [9, 195, 255])
    assert np.array_equal(get_cell_center_col(env, 8,5, last_state), [9, 195, 255])
    assert np.array_equal(get_cell_center_col(env, 8,4, last_state), [9, 195, 255])
    assert np.array_equal(get_cell_center_col(env, 7,4, last_state), [9, 195, 255])
    assert np.array_equal(get_cell_center_col(env, 7,6, last_state), [9, 195, 255])

def get_cell_center_col(env, x, y, last_state):
    queue_width = env.renderer.queue_width
    tile_size = env.renderer.tile_size
    centering_vert = (5-env.board.height)/2 if env.board.height < 5 else 0
    #cell = np.array([x*tile_size + queue_width, y * tile_size]) + env.renderer.board_border // 2
    cell = np.array([x*tile_size + queue_width, (y + centering_vert) * tile_size]) + env.renderer.board_border
    center = np.array([int(cell[0] + tile_size // 2), int(cell[1] + tile_size // 2)])
    #print("center = ", center)
    return last_state[center[1]][center[0]]
    #return last_state[center[0]][center[1]]

def diff_board_size(steps=100, render_gif=False, width=10, height=7, **kwargs):
    env = gym.make("PipeDream-v0", width=width, height=height, **kwargs)
    env.reset(seed=0)
    env.render()
    for i in range(steps):
        action = env.action_space.sample()
        state, reward, done, truncated, info = env.step(action)
        env.render()
        if render_gif:
            pygame.image.save(env.renderer.window, "temp{}.png".format(i))
        if done:
            break
    env.close()

def test_5x5_board(render_gif=False, width=5, height=5):
    diff_board_size(render_gif=render_gif, width=width, height=height)

def test_3x3_board(render_gif=False, width=3, height=3, **kwargs):
    diff_board_size(render_gif=render_gif, width=width, height=height, **kwargs)

def test_20x20_board(render_gif=False, width=20, height=20, **kwargs):
    diff_board_size(render_gif=render_gif, width=width, height=height, **kwargs)

def test_3x10_board(render_gif=False, width=3, height=10):
    diff_board_size(render_gif=render_gif, width=width, height=height)

def test_10x3_board(render_gif=False, width=10, height=3):
    diff_board_size(render_gif=render_gif, width=width, height=height)

def test_pipe_capacity_10(render_gif=False, **kwargs):
    test_working_loop(pipe_capacity=10, render_gif=render_gif, **kwargs)

def test_pipe_capacity_2(render_gif=False):
    test_working_loop(pipe_capacity=2, render_gif=render_gif)

def test_pipe_capacity_1(render_gif=False):
    test_working_loop(pipe_capacity=1, render_gif=render_gif)

def get_gif(func, gif_name):
    directory = os.path.dirname(os.path.realpath(__file__))
    num_frames = 200
    filename_list = [os.path.join(directory, "temp" + str(n) + ".png") for n in range(num_frames)]

    func(render_gif=True)

    anim_seconds = 5
    # glob the files with the specified regex sorted by time created
    files = sorted(glob.glob("temp?*.png"), key=os.path.getmtime)
    files = [os.path.join(directory, file) for file in files]
    seconds_per_frame = anim_seconds / num_frames
    frame_delay = str(int(seconds_per_frame * 500))
    #frame_delay = 2
    frame_delay = "120"
    command_list = ["convert", "-delay", frame_delay, "-loop", "0"] + files + [gif_name]
    subprocess.call(command_list, cwd=directory)
    for filename in files:
        os.remove(filename)
    
    command_list2 = ["mv", gif_name, "../images/"]
    subprocess.call(command_list2, cwd=directory)

def test_rgb_array():
    test_working_loop(render_mode="rgb_array")


if __name__=="__main__":
    #test_rgb_array()
    #get_gif(test_working_loop, "test_working_loop.gif")
    #get_gif(test_20x20_board, "test_20x20_board.gif")
    #get_gif(test_minimum_3x3_board, "test_min_3x3_board.gif")

    #test_3x3_board()
    #diff_board_size(width=4, height=4)
    #diff_board_size(width=2, height=2)
    #test_5x5_board()
    #test_20x20_board(window_size=1200)
    #test_10x3_board()
    #test_3x10_board()

    #test_3x3_board()
    #test_3x3_board(window_size=1200)
    #test_3x3_board(window_size=400)

    #test_pipe_capacity_10()
    test_working_loop(render_fps=1)

    #test_working_loop(render_fps=4)
    #test_working_loop(render_fps=8)
    #print("Starting capacity 4 test")
    #test_pipe_capacity_4()
    #print("Starting capacity 3 test")
    #test_pipe_capacity_3()
    #print("Starting capacity 2 test")
    #test_pipe_capacity_2()
    #print("Starting capacity 1 test")
    #test_pipe_capacity_1()
