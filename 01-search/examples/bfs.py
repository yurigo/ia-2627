from collections import deque

def bfs(filas, columnas, inicio, objetivo):

    cola = deque()
    cola.append((inicio, [inicio]))

    visitados = set()
    visitados.add(inicio)

    movimientos = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while cola:
        # elemento = cola.popleft()
        # actual = elemento[0]
        # camino = elemento[1]

        actual, camino = cola.popleft()

        if (actual == objetivo):
            return camino

        fila, columna = actual

        for df, dc in movimientos:
            nueva_fila = fila + df
            nueva_columna = columna + dc

            vecino = (nueva_fila, nueva_columna)

            #¿estoy dentro de la matriz?
            if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:

                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo_camino = camino + [vecino]
                    cola.append((vecino, nuevo_camino))

    return None


print("el camino es: " , bfs(10, 10, (0,0) , (2,2)) )



