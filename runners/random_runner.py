import random
import time
from importlib import machinery as importlib_machinery
import types
import sys

def default_possible_moves(board, token):
    print("error - you don't define a possible_moves method")
    sys.exit(1)
    return []
def default_make_move(board, token, index):
    print("error - you don't define a make_move method")
    sys.exit(1)
    return ""
def load_othelloresource(path):
    loader = importlib_machinery.SourceFileLoader("othello_resource", path)
    module = types.ModuleType(loader.name)
    module.possible_moves = default_possible_moves
    module.make_move = default_make_move
    loader.exec_module(module)
    return module

class Strategy:
    logging = True
    def best_strategy(self, board, player, best_move, running, othello_resource_path="./othelloresource.py"):
        best_move.value = random.choice(load_othelloresource(othello_resource_path).possible_moves(board, player))