import run
import argparse
import importlib

cmd = argparse.ArgumentParser()
cmd.add_argument("-o", "--othello-resource", required=True, help="path to othelloresource.py (no .py extension!)")
cmd.add_argument("-1", "--player-one", required=False, default="console", help="first player (filename or \"console\", \"edax\", default: \"console\")")
cmd.add_argument("-2", "--player-two", required=False, default="console", help="second player (filename or \"console\", \"edax\", default: \"console\")")
cmd.add_argument("-t", "--time", "--time-limit", required=False, default=2, help="time limit (seconds, default=2)", type=int)
cmd.add_argument("-d", "--edax-difficulty", required=False, default=100, help="AI difficulty (0-100, default=100, only applies if using \"edax\")", type=int)
cmd.add_argument("-e", "--edax", "--edax-path", required=False, default=".", help="path to folder/directory containing edax binary (only necessary if NOT in current directory) - please name the binary \"edax\" with no filename extension and make sure data/eval.dat is in the same directory as the binary")
cmd.add_argument("-m", "--num-games", "--multiple-games", required=False, default=1, type=int, help="enable multi-game mode (prints win/loss statistics after playing multiple games)")
cmd.add_argument("-r", "--machine-readable", help="machine-readable output", action="store_true", default=False, required=False)

args = cmd.parse_args()
othello_resource = importlib.__import__(args.othello_resource)
print(othello_resource.possible_moves("........"*3+"...xo..."+"...ox..."+"........"*3, "x"))

print(args)