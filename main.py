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

def display_board(board, machine_readable=False):
    if machine_readable:
        print(board)
    else:
        for i in range(0, 64, 8):
            print(" ".join(board[i:i+8]))

if __name__ == "__main__":
    import random
    import multiprocessing as mp
    import run
    import sys
    import argparse
    mp.freeze_support()

    cmd = argparse.ArgumentParser()
    cmd.add_argument("-o", "--othello-resource", required=True, help="path to othelloresource.py (you don't have to name it that)")
    cmd.add_argument("-1", "--player-one", required=False, default="console", help="first player (filename or \"console\", \"random\", default: \"console\")")
    cmd.add_argument("-2", "--player-two", required=False, default="console", help="second player (filename or \"console\", \"random\", default: \"console\")")
    cmd.add_argument("-t", "--time", "--time-limit", required=False, default=2, help="time limit (seconds, default=2)", type=int)
    cmd.add_argument("-r", "--machine-readable", help="machine-readable output", action="store_true", default=False, required=False)

    args = cmd.parse_args()

    othello_resource_path = args.othello_resource
    othello_resource = load_othelloresource(othello_resource_path)

    time_limit = int(args.time)

    machine_readable = args.machine_readable

    swap_xo = {"x": "o", "o": "x", ".": "."}
    player_dict = {"x": args.player_one, "o": args.player_two}
    current_board = "...........................xo......ox..........................."
    current_player = "x"
    display_board(current_board, machine_readable=machine_readable)
    while True:
        if len(othello_resource.possible_moves(current_board, current_player)) == 0:
            if len(othello_resource.possible_moves(current_board, swap_xo[current_player])) > 0:
                current_player = swap_xo[current_player]
                continue
            else:
                break

        next_move = run.run_program(current_board, current_player, player_dict[current_player], time_limit, othello_resource_path)
        
        current_board = othello_resource.make_move(current_board, current_player, next_move)
        if machine_readable:
            print(current_player, next_move, current_board.count('x'), current_board.count('o'))
        else:
            print(current_player, "at square", next_move, "->", f"x = {current_board.count('x')} discs, o = {current_board.count('o')} discs")
        display_board(current_board, machine_readable=machine_readable)
        print()
        current_player = swap_xo[current_player]
    
    x_score = current_board.count('x')
    o_score = current_board.count('o')
    if x_score > o_score:
        print(f"X wins by +{x_score-o_score}")
    elif o_score > x_score:
        print(f"O wins by +{o_score-x_score}")
    else:
        print("Tie")