def imprimir_laberinto(laberinto, camino):
    mapa = [
        linea.split()
        for linea in laberinto.strip().splitlines()
    ]

    for fila, columna in camino:
        casilla = mapa[fila][columna]

        if casilla == ".":
            mapa[fila][columna] = "█"
        elif casilla == "M":
            mapa[fila][columna] = "▓"

    for fila in mapa:
        print(" ".join(fila))

def imprimir_traza(laberinto, explorados):
    mapa = [
        linea.split()
        for linea in laberinto.strip().splitlines()
    ]

    # Primero, marcar todas las casillas exploradas
    for fila, columna in explorados:
        if mapa[fila][columna] == ".":
            mapa[fila][columna] = "*"
        elif mapa[fila][columna] == "M":
            mapa[fila][columna] = "*"

    # Imprimir el resultado
    for fila in mapa:
        print(" ".join(fila))


def dfs(laberinto):
    # Convertimos el texto en una matriz
    mapa = [
        linea.split()
        for linea in laberinto.strip().splitlines()
    ]

    filas = len(mapa)
    columnas = len(mapa[0])

    # Encontrar inicio y objetivo
    inicio = objetivo = None

    for f in range(filas):
        for c in range(columnas):
            if mapa[f][c] == "S":
                inicio = (f, c)
            elif mapa[f][c] == "G":
                objetivo = (f, c)

    if inicio is None or objetivo is None:
        raise ValueError("El laberinto debe tener S y G")

    pila = [(inicio, [inicio])]
    visitados = {inicio}
    explorados = []

    movimientos = [
        (-1, 0),  # arriba
        (1, 0),   # abajo
        (0, -1),  # izquierda
        (0, 1)    # derecha
    ]

    while pila:
        actual, camino = pila.pop()
        explorados.append(actual)

        if actual == objetivo:
            return camino, explorados

        fila, columna = actual

        for df, dc in movimientos:
            nf = fila + df
            nc = columna + dc

            vecino = (nf, nc)

            # Dentro del mapa y no es una pared
            if (0 <= nf < filas and
                0 <= nc < columnas and
                mapa[nf][nc] != "#" and
                vecino not in visitados):

                visitados.add(vecino)
                pila.append((vecino, camino + [vecino]))

    return None


# laberinto = """
# S . . . . . . . . G
# . # # # # # # # # .
# . . . . . . . . . .
# """

laberinto = """
S . M . # . . . . . . # . . . . . . . # . . . . .
# # M . # . # # # # . # . # # # # # . # . # # # .
. . M . . . . . . # . . . # . . . # . . . . . # .
. # # # # # # # . # # # . # . # . # # # # . # . .
. . . . . . . # . . . . . . . # . . . . . . # . .
# # # # . . . # # # # # # . # # # # # . # # # . #
. . . # . # . . . . . # . . . M . # . . . . . . .
. # . # . # # # # # . # # # # M . # . # # # # # .
. # . . . . . . . # . . . . # M . . . . . . . # .
. # # # # # # # . # # # . . # # # # # # # . . # .
. . . . . . . # . . . # . . . M M M M . # . . . .
# # # # # . . # # # . # # # # # # # M . # # # . .
. . . . # . . . . . . . . . . . . # M . . . . . .
. # # . # # # # # # # # # # # . # . # # # # # # .
. . . . . . . . . . . . . . # . . . . . . . . . G
"""

camino, explorados = dfs(laberinto)
print("Camino:", camino , explorados)

imprimir_laberinto(laberinto, camino)
imprimir_traza(laberinto, explorados)