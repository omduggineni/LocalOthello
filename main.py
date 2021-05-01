from importlib import machinery as importlib_machinery
import types
import sys
from statistics import mean

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
        print("  A B C D E F G H  ")
        for i in range(0, 64, 8):
            print(f"{i//8+1} " + " ".join(board[i:i+8]) + f" {i//8+1}")
        print("  A B C D E F G H  ")

move_letters = "ABCDEFGH"
def move_to_letters(move_num):
    return move_letters[move_num%8]+str(move_num//8+1)

def main():
    import random
    import run
    import argparse

    cmd = argparse.ArgumentParser()
    cmd.add_argument("-v", "--version", action="version",
        version="v1.2.0")
    cmd.add_argument("-o", "--othello-resource", required=True, help="path to othelloresource.py (you don't have to name it that)")
    cmd.add_argument("-1", "--player-one", required=False, default="console", help="first player (filename or \"console\", \"random\", default: \"console\")")
    cmd.add_argument("-2", "--player-two", required=False, default=None, help="second player (filename or \"console\", \"random\", default: same as first player)")
    cmd.add_argument("-m", "--multiple-trials", required=False, default=1, help="number of repeated games", type=int)
    cmd.add_argument("-t", "--time", "--time-limit", required=False, default=2, help="time limit (seconds, default=2)", type=int)
    cmd.add_argument("-r", "--machine-readable", help="machine-readable output", action="store_true", default=False, required=False)
    cmd.add_argument("-j", "--just-statistics", help="only print statistics - requires multiple-trials (-m) > 1", action="store_true", default=False, required=False)

    args = cmd.parse_args()

    if args.player_two is None:
        args.player_two = args.player_one

    othello_resource_path = args.othello_resource
    othello_resource = load_othelloresource(othello_resource_path)

    time_limit = int(args.time)

    machine_readable = args.machine_readable

    num_trials = args.multiple_trials
    multiple_trials = num_trials != 1

    just_statistics = args.just_statistics

    if just_statistics and (args.player_one == "console" or args.player_two == "console"):
        print("WARNING: just_statistics was requested but is incompatible with console input (the default). Ignoring --just-statistics. (-j)")
        print()
        just_statistics = False

    swap_xo = {"x": "o", "o": "x", ".": "."}
    player_dict = {"x": args.player_one, "o": args.player_two}

    logs = []
    for i in range(num_trials):
        gameboards = []
        current_board = "...........................xo......ox..........................."
        gameboards.append(current_board)
        current_player = "x"
        if multiple_trials:
            if not just_statistics: print(f"GAME {i+1}:")
        if not just_statistics: display_board(current_board, machine_readable=machine_readable)
        
        while True:
            if len(othello_resource.possible_moves(current_board, current_player)) == 0:
                if len(othello_resource.possible_moves(current_board, swap_xo[current_player])) > 0:
                    current_player = swap_xo[current_player]
                    continue
                else:
                    break

            next_move = run.run_program(current_board, current_player, player_dict[current_player], time_limit, othello_resource_path)
            
            current_board = othello_resource.make_move(current_board, current_player, next_move)
            gameboards.append(current_board)
            if not just_statistics: 
                if machine_readable:
                    print(current_player, next_move, current_board.count('x'), current_board.count('o'))
                else:
                    print(current_player, "at square", f"{move_to_letters(next_move)} (index {next_move})", "->", f"x = {current_board.count('x')} discs, o = {current_board.count('o')} discs")
                display_board(current_board, machine_readable=machine_readable)
                print()
            current_player = swap_xo[current_player]

        x_score = current_board.count('x')
        o_score = current_board.count('o')
        if x_score > o_score:
            if not just_statistics: print(f"X wins by +{x_score-o_score}")
        elif o_score > x_score:
            if not just_statistics: print(f"O wins by +{o_score-x_score}")
        else:
            if not just_statistics: print("Tie")
        if not just_statistics: print('\n')
        
        log_obj = {}
        log_obj['x_score'] = x_score
        log_obj['o_score'] = o_score
        log_obj['win_player'] = "x" if x_score > o_score else ("o" if o_score > x_score else None)
        log_obj['boards'] = gameboards
        logs.append(log_obj)
    
    if not just_statistics: print("===========")
    if not just_statistics: print("Statistics:")
    avg_x_score = mean([log["x_score"] for log in logs])
    print(f"Average score for x: {avg_x_score}")
    avg_o_score = mean([log["o_score"] for log in logs])
    print(f"Average score for o: {avg_o_score}")
    avg_endgame_board_fullness = avg_x_score+avg_o_score
    #print(f"Average endgame board fullness (average number of discs in the board when the game ended): {avg_endgame_board_fullness}")
    num_discs_win = abs(avg_x_score-avg_o_score)
    percent_filled_board = (max(avg_x_score, avg_o_score)/avg_endgame_board_fullness)*100
    print(f"Overall Winner: {'player 1' if avg_x_score > avg_o_score else ('player 2' if avg_o_score > avg_x_score else 'none (tie)')} (won by {round(num_discs_win, 2)} discs on average, with {round(percent_filled_board, 2)}% of the filled board)")

if __name__ == "__main__":
    import multiprocessing as mp
    mp.freeze_support()
    main()
