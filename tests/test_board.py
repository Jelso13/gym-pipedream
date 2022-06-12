import gym_pipedream
from gym_pipedream.grid_elements import *
from gym_pipedream.envs.pipedream_env import PipeDreamEnv
import logging

import pytest

tap_data = [
    ["top left", [0,0], ["right", "down"]],
    ["top right", [9,0], ["down", "left"]],
    ["bottom right", [9,6], ["up", "left"]],
    ["bottom left", [0,6], ["up", "right"]],
    ["outside top", [3, -3], []],
    ["outside right", [15, 3], []],
    ["outside bottom", [3, 15], []],
    ["outside left", [-4,2], []],
    ["inside", [3,3], ["up", "right", "down", "left"]]
]

@pytest.mark.parametrize("coords, expected_output", [[i[1], i[2]] for i in tap_data], ids=[i[0] for i in tap_data])
def test_tap_init(coords, expected_output):
    env = PipeDreamEnv()
    output = env.board.get_valid_tap_direction(coords, True)[1]
    assert output == expected_output



if __name__=="__main__":
    print(tap_data)
    #pytest.main(["-v"])
    pytest.main(["-v", "--tb=no", "--no-header", "--no-summary", "--show-capture=no"])