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

