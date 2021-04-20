import run
import argparse

cmd = argparse.ArgumentParser()
cmd.add_argument("-1", "--player-one", required=False, default="console", help="first player (filename or \"console\", \"edax\", default: \"console\")")
cmd.add_argument("-2", "--player-two", required=False, default="console", help="second player (filename or \"console\", \"edax\", default: \"console\")")
cmd.add_argument("-t", "--time", "--time-limit", required=False, default=2, help="time limit (seconds, default=2)", type=int)
cmd.add_argument("-d", "--edax-difficulty", required=False, default=100, help="AI difficulty (0-100, default=100, only applies if using \"edax\")", type=int)
cmd.add_argument("-e", "--edax", "--edax-path", required=False, default=".", help="path to folder/directory containing edax binary (only necessary if NOT in current directory) - please name the binary \"edax\" with no filename extension and make sure data/eval.dat is in the same directory as the binary")
cmd.add_argument("-m", "--num-games", "--multiple-games", required=False, default=None, type=int, help="enable multi-game mode (prints win/loss statistics after playing multiple games)")
cmd.add_argument("-r", "--machine-readable", help="machine-readable output", action="store_true", default=False, required=False)

args = cmd.parse_args()

print(args)