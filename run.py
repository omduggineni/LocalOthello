import multiprocessing as mp
import sys
import time
import random

def load_program_from_file(filename):
    from importlib import machinery as importlib_machinery
    import types
    loader = importlib_machinery.SourceFileLoader("your_othello_strategy", filename)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    return module

# Returns a tuple. 
# The first element contains the program's module, 
# the second contains a boolean which specifies whether or not to also load othelloresource.py and send it to the program 
# (necessary for any Othello programs bundled with this application)
def load_program(name):
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
    strat = player.Strategy() #your IDE may complain about this but it's fine
    if provide_othello_resource:
        othello_resource = load_othelloresource(othello_resource_path)
        ready.value = 1
        strat.best_strategy(board_state, player_xo, best_move, still_running, othello_resource=othello_resource)
    else:
        ready.value = 1
        strat.best_strategy(board_state, player_xo, best_move, still_running)

def run_program(board_state, player_xo, player_name, time_limit, othello_resource_path):
    if player_name == "console":
        othello_resource = load_othelloresource(othello_resource_path)
        possible_moves = othello_resource.possible_moves(board_state, player_xo)
        print(f"Possible moves: {possible_moves}")
        possible_moves = set(possible_moves)
        while True:
            try:
                move = int(input("Choose your move: "))
                assert move in possible_moves
                return move
            except AssertionError:
                print("ERROR: Not a valid move")
            except ValueError:
                print("ERROR: Not a valid move")
            except EOFError:
                print("ERROR: Not a valid move")
    elif player_name == "random":
        othello_resource = load_othelloresource(othello_resource_path)
        possible_moves = othello_resource.possible_moves(board_state, player_xo)
        return random.sample(possible_moves, 1)[0]

    best_move = mp.Value("i")
    best_move.value = -1
    still_running = mp.Value("i")
    still_running.value = 1
    ready = mp.Value("i")
    ready.value = 0

    process = mp.Process(target=program_caller, args=(player_name, board_state, player_xo, best_move, still_running, othello_resource_path, ready))
    process.start()
    start_time_limit = time.perf_counter()
    while ready.value == 0:
        if not process.is_alive():
            print("ERROR: your code crashed while loading :(")
            sys.exit(1)
        if time.perf_counter() > start_time_limit+1:
            process.kill()
            print("ERROR: Code that runs on import must finish within 1s")
            print("Any code outside a function or if __name__ == \"__main__\" block, including imports, must terminate within 1 second.")
            sys.exit(1)
    process.join(time_limit-0.05)
    if process.is_alive():
        still_running.value = 0
        process.join(0.05)
    process.kill()
    return best_move.value

if __name__ == "__main__":
    mp.freeze_support()
