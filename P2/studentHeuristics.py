from game import TwoPlayerGameState
from heuristic import complex_evaluation_function
from reversi import from_array_to_dictionary_board
from tournament import StudentHeuristic
from typing import Callable


def general_evaluation_function(state: TwoPlayerGameState, func: Callable[[TwoPlayerGameState], float]) -> float:
    if state.end_of_game:
        scores = state.scores
        score_difference = scores[0] - scores[1]
        if state.is_player_max(state.player1):
            return score_difference
        if state.is_player_max(state.player2):
            return - score_difference
        else:
            raise ValueError('Player MAX not defined')

    return func(state)


def is_x_position(pos) -> bool:
    return pos in [(2, 2), (2, 7), (7, 2), (7, 7)]


def is_c_position(pos) -> bool:
    return pos in [(1, 2), (2, 1), (1, 7), (2, 8), (7, 1), (8, 2), (7, 8), (8, 7)]


class MySolution1(StudentHeuristic):
    def get_name(self) -> str:
        return "2301_04_sol1"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return complex_evaluation_function(state)


class MySolution3(StudentHeuristic):
    def get_name(self) -> str:
        return "2301_04_sol3"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return general_evaluation_function(state, self.evaluate)

    def evaluate(self, state: TwoPlayerGameState) -> float:
        score = 0
        for pos in state.board:
            if pos not in state.parent.board:       # i. e. the move played
                if is_x_position(pos):
                    score = -1
                if is_c_position(pos):
                    score = -.5

        score *= state.game.max_score
        if state.is_player_max(state.player1):
            return score
        if state.is_player_max(state.player2):
            return - score
        else:
            raise ValueError('Player MAX not defined')
