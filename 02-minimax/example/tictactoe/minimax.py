
import random

HUMAN = "X"
AI = "O"

WINNING_COMBINATIONS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
]

MOVE_ORDER = [4, 0, 2, 6, 8, 1, 3, 5, 7]


def get_winner(board):
    """Devuelve X, O o None."""

    for a, b, c in WINNING_COMBINATIONS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    return None


def get_available_moves(board):
    """Devuelve las casillas libres."""

    return [
        index
        for index in MOVE_ORDER
        if board[index] == ""
    ]


def is_draw(board):
    """Comprueba si el tablero está lleno y no hay ganador."""

    return get_winner(board) is None and "" not in board


def minimax(
    board,
    depth,
    maximizing,
    ai=AI,
    human=HUMAN,
    alpha=float("-inf"),
    beta=float("inf")
):
    """Algoritmo Minimax con poda alfa-beta."""

    winner = get_winner(board)

    if winner == ai:
        return 10 - depth

    if winner == human:
        return depth - 10

    moves = get_available_moves(board)

    if not moves:
        return 0

    if maximizing:
        best_score = float("-inf")

        for move in moves:
            board[move] = ai

            score = minimax(
                board,
                depth + 1,
                False,
                ai,
                human,
                alpha,
                beta
            )

            board[move] = ""

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                break

        return best_score

    else:
        best_score = float("inf")

        for move in moves:
            board[move] = human

            score = minimax(
                board,
                depth + 1,
                True,
                ai,
                human,
                alpha,
                beta
            )

            board[move] = ""

            best_score = min(best_score, score)
            beta = min(beta, best_score)

            if beta <= alpha:
                break

        return best_score


def get_best_move(board, ai=AI, human=HUMAN):
    """Devuelve el mejor movimiento disponible."""

    if get_winner(board):
        return None

    moves = get_available_moves(board)

    if not moves:
        return None

    best_score = float("-inf")
    best_moves = []

    for move in moves:
        board[move] = ai

        score = minimax(
            board,
            depth=1,
            maximizing=False,
            ai=ai,
            human=human
        )

        board[move] = ""

        if score > best_score:
            best_score = score
            best_moves = [move]

        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)
