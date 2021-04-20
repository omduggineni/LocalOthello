from types import SimpleNamespace
import edax_runner

INVALID_FILENAME = -1

program_cache = dict()
program_cache["edax"] = edax_runner

def run_program(name, board_state, player):
    best_move = SimpleNamespace()
    best_move.value = None
    still_running = SimpleNamespace()
    still_running.value = 1
