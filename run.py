import multiprocessing as mp
import sys
import time

def load_program_from_file(filename):
    from importlib import machinery as importlib_machinery
    import types
    loader = importlib_machinery.SourceFileLoader("othello_resource", filename)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    return module

def load_program(name):
    if name == "edax":
        from runners import edax_runner
        return edax_runner, True
    if name == "console":
        from runners import console_runner
        return console_runner, True
    if name == "random":
        from runners import random_runner
        return random_runner, True
    else:
        return load_program_from_file(name), False

def default_possible_moves(board, token):
    print("error - you don't define a possible_moves method")
    sys.exit(1)
    return []
def default_make_move(board, token, index):
    print("error - you don't define a make_move method")
    sys.exit(1)
    return ""
def load_othelloresource(path):
    from importlib import machinery as importlib_machinery
    import types
    loader = importlib_machinery.SourceFileLoader("othello_resource", path)
    module = types.ModuleType(loader.name)
    module.possible_moves = default_possible_moves
    module.make_move = default_make_move
    loader.exec_module(module)
    return module

def program_caller(player_name, board_state, player_xo, best_move, still_running, othello_resource_path, ready):
    player, provide_othello_resource = load_program(player_name)
    strat = player.Strategy()
    if provide_othello_resource:
        othello_resource = load_othelloresource(othello_resource_path)
        ready.value = 1
        strat.best_strategy(board_state, player_xo, best_move, othello_resource=othello_resource)
    else:
        ready.value = 1
        strat.best_strategy(board_state, player_xo, best_move)

def run_program(board_state, player_xo, player_name, time_limit, othello_resource_path):
    best_move = mp.Value("i")
    best_move.value = 0
    still_running = mp.Value("i")
    still_running.value = 1
    ready = mp.Value("i")
    ready.value = 0

    process = mp.Process(target=program_caller, args=(player_name, board_state, player_xo, best_move, still_running, othello_resource_path, ready))
    process.start()
    start_time_limit = time.perf_counter()
    while ready.value == 0:
        if time.perf_counter() > start_time_limit+1:
            process.kill()
            print("ERROR: Code that runs on import must finish within 1s")
            print("Any code outside a function or if __name__ == \"__main__\" block, including imports, must terminate within 1 second.")
            sys.exit(1)
    process.join(2)
    process.kill()
    return best_move.value

if __name__ == "__main__":
    mp.freeze_support()