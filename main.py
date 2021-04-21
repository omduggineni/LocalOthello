from importlib import machinery as importlib_machinery
import types

def load_othelloresource(path):
    loader = importlib_machinery.SourceFileLoader("othello_resource", path)
    module = types.ModuleType(loader.name)
    def default_possible_moves(board, token):
        print("error - you don't define a possible_moves method")
        sys.exit(1)
        return []
    def default_make_move(board, token, index):
        print("error - you don't define a make_move method")
        sys.exit(1)
        return ""
    module.possible_moves = default_possible_moves
    module.make_move = default_make_move
    loader.exec_module(module)
    return module

if __name__ == "__main__":
    import random
    import multiprocessing as mp
    import run
    import sys
    import argparse
    mp.freeze_support()

    cmd = argparse.ArgumentParser()
    cmd.add_argument("-o", "--othello-resource", required=True, help="path to othelloresource.py (you don't have to name it that)")
    cmd.add_argument("-1", "--player-one", required=False, default="console", help="first player (filename or \"console\", \"edax\", default: \"console\")")
    cmd.add_argument("-2", "--player-two", required=False, default="console", help="second player (filename or \"console\", \"edax\", default: \"console\")")
    cmd.add_argument("-t", "--time", "--time-limit", required=False, default=2, help="time limit (seconds, default=2)", type=int)
    cmd.add_argument("-d", "--edax-difficulty", required=False, default=100, help="AI difficulty (0-100, default=100, only applies if using \"edax\")", type=int)
    cmd.add_argument("-e", "--edax", "--edax-path", required=False, default=".", help="path to folder/directory containing edax binary (only necessary if NOT in current directory) - please name the binary \"edax\" with no filename extension and make sure data/eval.dat is in the same directory as the binary")
    cmd.add_argument("-m", "--num-games", "--multiple-games", required=False, default=1, type=int, help="enable multi-game mode (prints win/loss statistics after playing multiple games)")
    cmd.add_argument("-r", "--machine-readable", help="machine-readable output", action="store_true", default=False, required=False)

    args = cmd.parse_args()

    othello_resource_path = args.othello_resource
    othello_resource = load_othelloresource(othello_resource_path)

    time_limit = int(args.time)

    swap_xo = {"x": "o", "o": "x", ".": "."}
    player_dict = {"x": args.player_one, "o": args.player_two}
    current_board = "...........................xo......ox..........................."
    current_player = "x"
    print(current_board)
    while True:
        if len(othello_resource.possible_moves(current_board, current_player)) == 0:
            if len(othello_resource.possible_moves(current_board, swap_xo[current_player])) > 0:
                current_player = swap_xo[current_player]
                continue
            else:
                break

        next_move = run.run_program(current_board, current_player, player_dict[current_player], time_limit, othello_resource_path)
        print(current_player, next_move)
        
        current_board = othello_resource.make_move(current_board, current_player, next_move)
        print(current_board)
        current_player = swap_xo[current_player]