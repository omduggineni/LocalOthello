from types import SimpleNamespace
from runners import console_runner, edax_runner, random_runner
import importlib.machinery
import types
import multiprocessing as mp

INVALID_FILENAME = -1

def load_program_from_file(filename):
    loader = importlib.machinery.SourceFileLoader("othello_resource", filename)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    return module

def load_program(name):
    if name == "edax":
        return edax_runner, True
    if name == "console":
        return console_runner, True
    if name == "random":
        return random_runner, True
    else:
        return load_program_from_file(name), False

def program_caller(player_name, board_state, player_xo, best_move, still_running, othello_resource_path):
    player, provide_othello_resource = load_program(player_name)
    strat = player.Strategy()
    if provide_othello_resource:
        strat.best_strategy(board_state, player_xo, best_move, still_running, othello_resource_path=othello_resource_path)
    else:
        strat.best_strategy(board_state, player_xo, best_move, still_running)

def run_program(board_state, player_xo, player_name, time_limit, othello_resource_path):
    best_move = mp.Value("i")
    best_move.value = 0
    still_running = mp.Value("i")
    still_running.value = 1

    process = mp.Process(target=program_caller, args=(player_name, board_state, player_xo, best_move, still_running, othello_resource_path))
    process.start()
    process.join(2)
    process.kill()
    return best_move.value