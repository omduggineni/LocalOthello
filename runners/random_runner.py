import random

class Strategy:
    logging = True
    def best_strategy(self, board, player, best_move, still_running, othello_resource=None):
        best_move.value = random.choice(othello_resource.possible_moves(board, player))