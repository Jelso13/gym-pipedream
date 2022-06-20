import gym
import gym_pipedream
from gym_pipedream.grid_elements import *
from gym_pipedream.envs.pipedream_env import PipeDreamEnv
import random

def test_random_agent(steps=100):
    env = gym.make("PipeDream-v0", render_mode="ascii")
    env.reset()
    env.render()
    for e in range(steps):
        action = env.action_space.sample()
        print("action = ", action)
        state, reward, done, info = env.step(action)
        env.render()
        print(reward)
        if done:
            break

def core_test_with_water_loop(actions = [[7,6], [7,5], [7,4],[8,4],[8,5],[6,5]], pipe_capacity=5):
    random.seed(0)
    env = PipeDreamEnv(render_mode="ascii", pipe_capacity=pipe_capacity)
    state = env.reset()
    env.render()

    env.next_tiles = [LeftUpPipe(), CrossPipe(), RightDownPipe(), LeftDownPipe(), LeftUpPipe(), HorizontalPipe()]
    env.current_tile = env.next_tiles[0]

    w,h = [env.board.width, env.board.height]
    for i in range(100):
        if i == 3:
            random.seed(1)
        if i in range(len(actions)):
            action = actions[i]
        else:
            #action = env.action_space.sample()
            action = [random.randint(0,w-1), random.randint(0,h-1)]
        
        state, reward, done, info = env.step(action)
        env.render()
        if done:
            print("Game Over!")
            break
    return env

def test_cross_pipe_water():
    env = core_test_with_water_loop()
    final_pipe =  env.board.tiles[5*10 + 6]
    cross_pipe =  env.board.tiles[5*10 + 7]
    print(final_pipe.type)
    assert final_pipe.type == "horizontal"
    assert final_pipe.state == 0
    assert cross_pipe.state2 == 0
    assert cross_pipe.state == 0

def test_water_pipe_nonreplaceable():
    actions = [[7,6], [7,5], [7,4],[8,4],[8,5],[6,5]] + [[7,6]] * 20
    env = core_test_with_water_loop(actions=actions)
    assert env.board.tiles[6*10+7].state == 0


def test_tap_nonreplaceable():
    actions = [[6,6]] * 50
    env = core_test_with_water_loop(actions=actions)
    assert env.board.tiles[6*10 + 6].type[:5] == "start"

def test_replaceable_empty_pipe():
    random.seed(0)
    env = PipeDreamEnv(render_mode="ascii")
    state = env.reset()
    env.render()
    for i in range(100):
        action = [3,3]
        held_tile = env.current_tile
        state, reward, done, info = env.step(action)
        env.render()
        if done:
            print("Game Over!")
            break
        assert env.board.tiles[33].type == held_tile.type

def test_partially_filled_pipes_nonreplaceable():
    random.seed(0)
    env = PipeDreamEnv(render_mode="ascii")
    state = env.reset()
    env.render()
    env.board.set_tile([7,6], LeftUpPipe())
    #env.board.tiles[33] = LeftUpPipe()
    #env.board.tiles[33].state = 1 # set state to partially filled
    env.render()
    env.next_tiles = [VerticalPipe() for j in range(8)] + [HorizontalPipe() for i in range(92)]
    for i in range(100):
        if i >= 6:
            action = [7,6]
        else:
            action = [3,3]
        held_tile = env.current_tile
        state, reward, done, info = env.step(action)
        env.render()
        if done:
            print("Game Over!")
            break
    assert env.board.tiles[6*env.board.width + 7].type == "leftup"

def test_longer_fill_time():
    random.seed(0)
    pipe_capacity = 8
    env = PipeDreamEnv(render_mode="ascii", pipe_capacity=pipe_capacity)
    state = env.reset()
    env.render()

    env.next_tiles = [LeftUpPipe(state=pipe_capacity), CrossPipe(state=pipe_capacity), RightDownPipe(state=pipe_capacity), LeftDownPipe(state=pipe_capacity), LeftUpPipe(state=pipe_capacity), HorizontalPipe(state=pipe_capacity)]
    env.current_tile = env.next_tiles[0]

    w,h = [env.board.width, env.board.height]
    #env.render()
    for i in range(100):
        if i == 0:
            action = [7,6]
        elif i == 1:
            action = [7,5]
        elif i == 2:
            action = [7,4]
        elif i == 3:
            # if action ==3 then if the pipe is flowing at the slower rate then
            # [7, 5] should have a state of 7
            assert env.board.tiles[5*10+7].state == pipe_capacity
            action = [8,4]
            random.seed(0)
        elif i == 4:
            action = [8,5]
        elif i == 5:
            action = [6,5]
        else:
            #action = env.action_space.sample()
            action = [random.randint(0,w-1), random.randint(0,h-1)]
        
        print("action = ", action)
        print("next tiles = ", [t.type for t in env.next_tiles])
        print("start state = ", env.board.tiles[42].state)
        state, reward, done, info = env.step(action)
        env.render()
        if done:
            print("Game Over!")
            break

    final_pipe =  env.board.tiles[5*10 + 6]
    cross_pipe =  env.board.tiles[5*10 + 7]

def test_pipe_capacity_5():
    core_test_with_water_loop(pipe_capacity=5)

def test_pipe_capacity_4():
    core_test_with_water_loop(pipe_capacity=4)

def test_pipe_capacity_3():
    core_test_with_water_loop(pipe_capacity=3)

def test_pipe_capacity_2():
    core_test_with_water_loop(pipe_capacity=2)

def test_pipe_capacity_1():
    core_test_with_water_loop(pipe_capacity=1)

#def test_cross_half_filled_replace():
#
#    raise NotImplementedError

if __name__=="__main__":
    #test_random_agent()
    #test_cross_pipe_water()
    #test_water_pipe_nonreplaceable()
    #test_tap_nonreplaceable()
    #test_replaceable_empty_pipe()
    test_partially_filled_pipes_nonreplaceable()
    #test_longer_fill_time()
    #test_pipe_capacity_3()