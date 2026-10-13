from collections import deque

def bfs(filas, columnas, inicio, objetivo, paredes):

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
            print("cola:" , cola)
            print("visitados:" , visitados)
            return camino

        fila, columna = actual

        for df, dc in movimientos:
            nueva_fila = fila + df
            nueva_columna = columna + dc

            vecino = (nueva_fila, nueva_columna)

            #¿estoy dentro de la matriz?
            if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
                if vecino not in paredes:
                    if vecino not in visitados:
                        visitados.add(vecino)
                        nuevo_camino = camino + [vecino]
                        cola.append((vecino, nuevo_camino))

    return None


# print("el camino es: " , bfs(5, 5, (0,0), (4,4), [(1,0),(1,1),(2,2),(2,3),(3,2)]) )
print("el camino es: " , bfs(5, 5, (0,0), (4,4), [(1,0),(1,1),(1,3),(0,4),(2,3),(3,2)]) )



