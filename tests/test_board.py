import gym_pipedream
from gym_pipedream.grid_elements import *
from gym_pipedream.envs.pipedream_env import PipeDreamEnv
import logging

LOGGER = logging.getLogger(__name__)

import pytest


def gen_tap_data(min_x, max_x, min_y, max_y, expected_directions, section_label):
    data = []
    ids = []
    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            #assert env.get_valid_tap_direction((i,j), True)[1] == expected_directions
            data.append([(i,j), expected_directions])
            #ids.append(" {:<20} | position: ({},{}) | expected directions: {:<40} ".format(section_label, str(i),str(j), str(expected_directions)))
            tmp_str =  " {:<20} | position: ({},{}) | expected directions: {:<40} ".format(section_label, str(i),str(j), str(expected_directions))
            ids.append("{:<100}".format(tmp_str))

    return data, ids

tap_data = []
tap_ids = []
a, b = gen_tap_data(1, BOARD_WIDTH-1, 0,1, ["right", "down", "left"], "Top middle test")
tap_data += a
tap_ids += b
a, b = gen_tap_data(BOARD_WIDTH-1, BOARD_WIDTH, 1,BOARD_HEIGHT-1, ["up", "down", "left"], "Right middle test")
tap_data += a
tap_ids += b
a, b = gen_tap_data(1, BOARD_WIDTH-1, BOARD_HEIGHT-1,BOARD_HEIGHT, ["up", "right", "left"], "Bottom middle test")
tap_data += a
tap_ids += b
a, b = gen_tap_data(0, 1, 1, BOARD_HEIGHT-1, ["up", "right", "down"], "Left middle test")
tap_data += a
tap_ids += b

a, b = gen_tap_data(0,1, 0, 1, ["right", "down"], "Top Left Test")
tap_data += a
tap_ids += b
a, b = gen_tap_data(BOARD_WIDTH-1,BOARD_WIDTH, 0, 1, ["down", "left"], "Top right Test")
tap_data += a
tap_ids += b
a, b = gen_tap_data(BOARD_WIDTH-1, BOARD_WIDTH, BOARD_HEIGHT-1, BOARD_HEIGHT, ["up", "left"], "Bottom right test")
tap_data += a
tap_ids += b
a, b = gen_tap_data(0,1, BOARD_HEIGHT-1, BOARD_HEIGHT, ["up", "right"], "Bottom left test")
tap_data += a
tap_ids += b

@pytest.mark.parametrize("coords, expected_output", tap_data, ids=tap_ids)
def test_tap_init(coords, expected_output):
    env = PipeDreamEnv()
    output = env.board.get_valid_tap_direction(coords, True)[1]
    assert output == expected_output




if __name__=="__main__":
    #pytest.main(["-v"])
    pytest.main(["-v", "--tb=no", "--no-header", "--no-summary", "--show-capture=no"])