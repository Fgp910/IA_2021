from reversi import Reversi
import reversi
from game import (
    TwoPlayerGameState,
)
from tournament import (
    StudentHeuristic,
)


class MySolution1(StudentHeuristic):
    def get_name(self) -> str:
        return "2301_04_sol1"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        if state.end_of_game:
            scores = state.scores
            # Evaluation of the state from the point of view of MAX
            score_difference = scores[0] - scores[1]
        else:
            successors = state.game.generate_successors(state)
            # Minimize the number of your opponent moves (for MAX).
            score_difference = - len(successors)

        if state.is_player_max(state.player1):
            return score_difference
        elif state.is_player_max(state.player2):
            return - score_difference
        else:
            raise ValueError('Player MAX not defined')

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

            movility = len(game.generate_successors(state))

            result = 4*corner_diff - movility

        if state.is_player_max(state.player1):
            return result
        elif state.is_player_max(state.player2):
            return - result
        else:
            raise ValueError('Player MAX not defined')

# Private functions
#def isStable(game: reversi.Reversi, state: TwoPlayerGameState) -> bool:
