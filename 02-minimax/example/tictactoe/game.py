
from minimax import (
    HUMAN,
    AI,
    get_winner,
    get_best_move,
    is_draw
)


class TicTacToe:

    def __init__(self):
        self.victories = {
            HUMAN: 0,
            AI: 0
        }

        self.reset_game()

    def reset_game(self):
        """Reinicia la partida sin perder el marcador."""

        self.board = [""] * 9
        self.current_player = HUMAN

        self.active = True
        self.winner = None
        self.winning_combination = None

        self.status = "Turno del jugador X"

    def make_move(self, index):
        """Realiza un movimiento."""

        if not self.active:
            return False

        if self.current_player != HUMAN:
            return False

        if not 0 <= index < 9:
            return False

        if self.board[index] != "":
            return False

        self._place_move(index)
        return True

    def ai_move(self):
        """Calcula y ejecuta el movimiento de la IA."""

        if not self.active or self.current_player != AI:
            return

        move = get_best_move(self.board)

        if move is not None:
            self._place_move(move)

    def _place_move(self, index):
        """Coloca una ficha y comprueba el resultado."""

        player = self.current_player
        self.board[index] = player

        winner = get_winner(self.board)

        if winner:
            self.winner = winner
            self.active = False

            self.victories[winner] += 1

            self.winning_combination = self._get_winning_combination()

            self.status = f"¡Jugador {winner} ha ganado!"

            return

        if is_draw(self.board):
            self.active = False
            self.status = "¡Empate!"
            return

        self.current_player = AI if player == HUMAN else HUMAN

        self.status = f"Turno del jugador {self.current_player}"

    def _get_winning_combination(self):
        """Devuelve las tres casillas ganadoras."""

        from minimax import WINNING_COMBINATIONS

        for combination in WINNING_COMBINATIONS:
            a, b, c = combination

            if (
                self.board[a]
                and self.board[a] == self.board[b] == self.board[c]
            ):
                return combination

        return None
