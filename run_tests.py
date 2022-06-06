import gym_pipedream
from gym_pipedream.grid_elements import *
from gym_pipedream.envs.pipedream_env import PipeDreamEnv

VERBOSE = False

# Test to ensure that the encodings are correct *move to separate file*
def all_subclasses(cls):
    return list(set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]))

def print_sep(txt=""):
    print("\n{:-^80s}\n".format(" "+txt+" "))

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
    for i in range(500):
        env.init_tap()
    if VERBOSE: env.print_board()

if __name__=="__main__":
    env = PipeDreamEnv()
    test_encodings()
    test_board(env)
    test_init_pipe(env)