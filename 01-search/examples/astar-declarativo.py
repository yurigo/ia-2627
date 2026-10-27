
import heapq


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

    for fila, columna in explorados:
        if mapa[fila][columna] in (".", "M"):
            mapa[fila][columna] = "*"

    for fila in mapa:
        print(" ".join(fila))


# g(n): coste de entrar en una casilla
def coste_casilla(mapa, posicion):
    fila, columna = posicion

    if mapa[fila][columna] == "M":
        return 5

    return 1


# h(n): heurística Manhattan hasta la meta
def h(posicion, objetivo):
    return (
        abs(posicion[0] - objetivo[0]) +
        abs(posicion[1] - objetivo[1])
    )


# A*
def a_star(laberinto):
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

    # Frontera: (f(n), g(n), posición)
    frontera = []
    heapq.heappush(
        frontera,
        (h(inicio, objetivo), 0, inicio)
    )

    # Coste real mínimo conocido desde S
    costes = {inicio: 0}

    # Reconstrucción del camino
    padres = {}

    explorados = []

    movimientos = [
        (-1, 0),  # arriba
        (1, 0),   # abajo
        (0, -1),  # izquierda
        (0, 1)    # derecha
    ]

    while frontera:
        f_actual, g_actual, actual = heapq.heappop(frontera)

        # Ignorar entradas antiguas de la cola
        if g_actual != costes.get(actual):
            continue

        explorados.append(actual)

        if actual == objetivo:
            # Reconstruir el camino desde G hasta S
            camino = []
            nodo = objetivo

            while nodo != inicio:
                camino.append(nodo)
                nodo = padres[nodo]

            camino.append(inicio)
            camino.reverse()

            return camino, explorados, g_actual

        fila, columna = actual

        for df, dc in movimientos:
            nf = fila + df
            nc = columna + dc
            vecino = (nf, nc)

            if not (
                0 <= nf < filas and
                0 <= nc < columnas
            ):
                continue

            if mapa[nf][nc] == "#":
                continue

            # Calcular el nuevo coste acumulado g(n)
            nuevo_g = (
                g_actual +
                coste_casilla(mapa, vecino)
            )

            # Solo actualizar si encontramos un coste mejor
            if nuevo_g < costes.get(vecino, float("inf")):
                costes[vecino] = nuevo_g
                padres[vecino] = actual

                # Calcular h(n) y f(n)
                heuristica = h(vecino, objetivo)
                f_vecino = nuevo_g + heuristica

                heapq.heappush(
                    frontera,
                    (f_vecino, nuevo_g, vecino)
                )

    return None, explorados, float("inf")

laberinto = """
S . . M # . . . . . . # . . . . . . . # . . . . .
# # . M # . # # # # . # . # # # # # . # . # # # .
. . . M . . . . . # . . . # . . . # . . . . . # .
. # # # # # # # . # # # . # . # . # # # # . # . .
. . . . . . . # . . . . . . . # . . . . . . # . .
# # # # . . . # # # # # # . # # # # # . # # # . #
. . . # . # . . . . . # . . . M . # . . . . . . .
. # . # . # # # # # . # # # # M . # . # # # # # .
. # . . . . . . . # . . . . # M . M . . . . M # .
. # # # # # # # . # # # . . # # # # # # # . M # .
. . . . . . . # . . . # . . . . . . . # . . M . .
# # # # # . . # # # . # # # # # # # . . # # # . .
. . . . # . . . . . . . . . . . . # . . . . . . .
. # # . # # # # # # # # # # # . # . # # # # # # .
. . . . . . . . . . . . . . # . . . . . . . . . G
"""

camino, explorados, coste_total = a_star(laberinto)

print("Camino:", camino)
print("Coste total:", coste_total)
print("Explorados:", explorados)

if camino is not None:
    imprimir_laberinto(laberinto, camino)
    print()
    imprimir_traza(laberinto, explorados)
else:
    print("No existe un camino hasta la meta.")
