from reversi import Reversi
import reversi
from game import (
    TwoPlayerGameState,
)
from tournament import (
    StudentHeuristic,
)
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


class MySolution1(StudentHeuristic):
    def get_name(self) -> str:
        return "2301_04_sol1"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return complex_evaluation_function(state)


class MySolution2(StudentHeuristic):
    def get_name(self) -> str:
        return "2301_04_sol2"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        if not isinstance(state.game, Reversi):
            return 0
        if isinstance(state.board, dict):
            board = state.board
        else:
            board = reversi.from_array_to_dictionary_board(state.board)
        if state.end_of_game:
            scores = state.scores
            result = scores[0] - scores[1]
        else:
            game = state.game
            corners = [board.get((1, 1)), board.get((1, game.height)), board.get((game.width, 1)), board.get((game.width, game.height))]
            x_squares = [board.get((2,2)), board.get((2, game.height-1)), board.get((game.width-1, 2)), board.get((game.width-1, game.height-1))]
            corner_diff = 0
            for i in range(4):
                if corners[i] == game.player1.label:
                    corner_diff += 4
                elif corners[i] == game.player2.label:
                    corner_diff -= 4
                else:
                    if x_squares[i] == game.player1.label:
                        corner_diff -= 1
                    elif x_squares[i] == game.player2.label:
                        corner_diff += 1

            mobility = len(game.generate_successors(state))

            result = 4*corner_diff - mobility

        if state.is_player_max(state.player1):
            return result
        elif state.is_player_max(state.player2):
            return - result
        else:
            raise ValueError('Player MAX not defined')


class MySolution3(StudentHeuristic):
    def get_name(self) -> str:
        return "2301_04_sol3"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return general_evaluation_function(state, self.evaluate)

    def evaluate(self, state: TwoPlayerGameState) -> float:
        successors = state.game.generate_successors(state)
        total = len(successors)
        exes = 0.
        for suc in successors:
            for pos in suc.board.keys():
                if is_x_position(pos) and pos not in state.board:
                    exes += 1

        score = exes / total
        if state.is_player_max(state.player1):
            return - score
        if state.is_player_max(state.player2):
            return score
        else:
            raise ValueError('Player MAX not defined')
