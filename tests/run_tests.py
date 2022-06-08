import gym_pipedream
from gym_pipedream.grid_elements import *
from gym_pipedream.envs.pipedream_env import PipeDreamEnv
import random

VERBOSE = True

# Test to ensure that the encodings are correct *move to separate file*
def all_subclasses(cls):
    return list(set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]))

def print_sep(txt=""):
    print("\n{:-^80s}\n".format(" "+txt+" "))

def print_test(desc, outcome):
    print("    {:<30s}{}".format(desc, outcome))

def test_encodings():
    subcls = [cl for cl in all_subclasses(Tile) if cl.__name__ != "Pipe"]

    print_sep("TEST: Encodings")

    for cl in subcls:
        x = cl()
        print("type {:<20s} encoding {:<10s}".format(str(x.type), str(x.get_encoding())))

def test_board(env):
    print_sep("TEST: Board Initialisation")
    if VERBOSE: env.print_board()

def test_init_pipe(env):
    print_sep("TEST: Tap Position Initialisation")
    env.init_tap()
    if VERBOSE: env.print_board()

def test_init_tap(env):
    # test every direction at every location
    print_sep("TEST: Valid Tap Positions")
    dirs = ["top", "right", "bottom", "left"]
    tests = {
        "top" : [(i, 0) for i in [0, 1, 4, BOARD_WIDTH-1]],
        "right" : [(BOARD_WIDTH-1, i) for i in [0, 1, 4, BOARD_HEIGHT-1]],
        "bottom" : [(i, BOARD_HEIGHT-1) for i in [0, 1, 4, BOARD_WIDTH-1]],
        "left": [(0, i) for i in [0, 1, 4, BOARD_HEIGHT-1]]
    }

    print(env.get_valid_tap_direction((1,1), True))


import unittest
from unittest.runner import TextTestResult
import logging

TextTestResult.getDescription = lambda _, test: "{:<50s}".format(test.shortDescription()) if test.shortDescription() else "Test"

class TestBoard(unittest.TestCase):

    #def __init__(self, testName, arg1):
    #    super(TestBoard, self).__init__(testName)
    #    self.arg1 = arg1

    def test_0_init_tap(self):
        """Test thing"""
        env = PipeDreamEnv()
        self.assertEqual(env.get_valid_tap_direction((0,0), True)[1], ["right", "down"])

    def test_1_a(self):
        """assertion of false things test"""
        for i in range(1,11):
            with self.subTest(i=i):
                self.assertGreaterEqual(10, i)
        #self.assertEqual(3,4)
        #self.assertEqual(3,3)
        #self.assertEqual("hello","hello")
    
if __name__=="__main__":
    #env = PipeDreamEnv()
    #test_encodings()
    #test_board(env)
    #test_init_pipe(env)
    #test_init_tap(env)

    board_test = unittest.TestLoader().loadTestsFromTestCase(TestBoard)

    all_tests = unittest.TestSuite([board_test])
    unittest.TextTestRunner(verbosity=2).run(all_tests)
