"""Minimax con poda alfa-beta para tres en raya."""


LINEAS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def ganador(tablero):
    for a, b, c in LINEAS:
        if tablero[a] != " " and tablero[a] == tablero[b] == tablero[c]:
            return tablero[a]
    return None


def minimax_alfa_beta(tablero, jugador, alfa, beta, profundidad=0):
    resultado = ganador(tablero)
    if resultado == "X":
        return 10 - profundidad, None
    if resultado == "O":
        return profundidad - 10, None

    jugadas = [i for i, casilla in enumerate(tablero) if casilla == " "]
    if not jugadas:
        return 0, None

    mejor_jugada = None
    siguiente = "O" if jugador == "X" else "X"
    if jugador == "X":
        mejor_valor = float("-inf")
        for jugada in jugadas:
            nuevo_tablero = list(tablero)
            nuevo_tablero[jugada] = jugador
            valor, _ = minimax_alfa_beta(
                nuevo_tablero, siguiente, alfa, beta, profundidad + 1
            )
            if valor > mejor_valor:
                mejor_valor, mejor_jugada = valor, jugada
            alfa = max(alfa, mejor_valor)
            if alfa >= beta:
                break
    else:
        mejor_valor = float("inf")
        for jugada in jugadas:
            nuevo_tablero = list(tablero)
            nuevo_tablero[jugada] = jugador
            valor, _ = minimax_alfa_beta(
                nuevo_tablero, siguiente, alfa, beta, profundidad + 1
            )
            if valor < mejor_valor:
                mejor_valor, mejor_jugada = valor, jugada
            beta = min(beta, mejor_valor)
            if alfa >= beta:
                break

    return mejor_valor, mejor_jugada


if __name__ == "__main__":
    tablero = [" "] * 9
    valor, jugada = minimax_alfa_beta(
        tablero, "X", float("-inf"), float("inf")
    )
    print(f"Mejor jugada para X: casilla {jugada}")
    print(f"Valor minimax: {valor}")
