import time

class State:
    MAX_DEPTH = None

    def __init__(self, board, player, depth, parent=None, score=None):
        self.board = board
        self.player = player

        self.depth = depth
        self.score = score

        self.possible_moves = []

        self.choice = None

    def enemy(self):
        if (self.player == 'red'):
            return 'blue'
        else:
            return 'red'

    def moves(self):
        possibleMoves = self.board.getMoves('b' if self.player == 'blue' else 'r')

        states = []

        for move in possibleMoves:
            states.append( State(move, 'blue' if move.blue_moves else 'red', self.depth - 1, parent=self) )

        return states

def min_max(state):
    if (state.depth == 0 or state.board.checkWin()):
        state.score = state.board.calculateScore(state.depth)
        return state

    state.possible_moves = state.moves()

    scores = [min_max(move) for move in state.possible_moves]

    if state.player == 'blue':
        state.choice = max(scores, key=lambda x: x.score)
    else:
        state.choice = min(scores, key=lambda x: x.score)

    state.score = state.choice.score
    return state

def ab_pruning(alpha, beta, state):
    if (state.depth == 0 or state.board.checkWin()):
        state.score = state.board.calculateScore(state.depth)
        return state

    if alpha >= beta:
        return state

    state.possible_moves = state.moves()

    if state.player == 'blue':
        current_score = float('-inf')

        for move in state.possible_moves:
            new_state = ab_pruning(alpha, beta, move)

            if current_score < new_state.score:
                state.choice = new_state
                current_score = new_state.score

            if alpha < new_state.score:
                alpha = new_state.score
                if alpha >= beta:
                    break
    else:
        current_score = float('inf')

        for move in state.possible_moves:
            new_state = ab_pruning(alpha, beta, move)

            if current_score > new_state.score:
                state.choice = new_state
                current_score = new_state.score

            if beta > new_state.score:
                beta = new_state.score
                if alpha >= beta:
                    break

    state.score = state.choice.score

    return state
