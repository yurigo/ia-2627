# Búsqueda en espacios de estados

Esta lección presenta cuatro algoritmos para encontrar caminos en un espacio de
estados. En los ejemplos, cada estado es una casilla `(fila, columna)` de una
cuadrícula; los movimientos permitidos son arriba, abajo, izquierda y derecha.
`S` representa el inicio, `G` la meta, `#` una pared, `.` una casilla normal y
`M` una casilla de terreno especial. Un camino es la secuencia de casillas que
conecta el inicio con la meta.

Los algoritmos mantienen una **frontera** de estados descubiertos que todavía
no han explorado y un conjunto de **visitados** para evitar recorrer un estado
varias veces. Su diferencia principal es el orden en que eligen el siguiente
estado de la frontera.

## Búsqueda en anchura (BFS)

BFS (*breadth-first search*) explora primero todos los estados a una distancia
de un movimiento, luego los que están a dos movimientos, y así sucesivamente.
Para mantener este orden usa una cola FIFO: el primer estado que entra es el
primero que sale. En `examples/bfs.py`, `deque` implementa la cola y cada
elemento guarda tanto la posición como el camino recorrido hasta ella.

Cuando todos los movimientos tienen el mismo coste, BFS encuentra un camino
con el menor número de movimientos. La variante
[`bfs-con-paredes.py`](examples/bfs-con-paredes.py) descarta las casillas
marcadas como paredes. La versión
[`bfs-declarativo.py`](examples/bfs-declarativo.py) lee un laberinto escrito
como texto y además muestra el camino y las casillas exploradas.

**Cuándo usarlo:** cuando los pasos cuestan lo mismo y se necesita el camino
más corto. Puede consumir mucha memoria porque conserva muchos estados
pendientes.

## Búsqueda en profundidad (DFS)

DFS (*depth-first search*) sigue un camino tan lejos como pueda antes de
retroceder y probar otra alternativa. Para ello usa una pila LIFO: el último
estado añadido es el primero que sale. En `examples/dfs.py`, una lista cumple
esa función mediante `append` y `pop`; el conjunto de visitados evita ciclos.

DFS puede encontrar una solución sin explorar primero todas las alternativas
cercanas, pero el camino encontrado **no tiene por qué ser el más corto**. La
variante [`dfs-con-paredes.py`](examples/dfs-con-paredes.py) evita paredes y
[`dfs-declarativo.py`](examples/dfs-declarativo.py) permite visualizar tanto
el camino como la traza de exploración.

**Cuándo usarlo:** cuando basta con encontrar una solución y se quiere explorar
con poca memoria. El resultado depende del orden de los movimientos; en un
espacio infinito o sin control de visitados, puede no terminar.

## Búsqueda voraz (Greedy best-first)

La búsqueda voraz (*greedy best-first search*) elige el estado que parece más
cercano a la meta según una heurística `h(n)`. En
[`greedy-declarativo.py`](examples/greedy-declarativo.py), la heurística es la
distancia Manhattan:

`h(n) = |fila(n) - fila(meta)| + |columna(n) - columna(meta)|`

Esta distancia estima cuántos movimientos arriba/abajo y derecha/izquierda
faltan, ignorando paredes. Una cola de prioridad (`heapq`) hace que se explore
primero el estado con menor heurística. La heurística es una guía, no el coste
real del camino: como el algoritmo no considera cuánto ha costado llegar hasta
un estado, puede elegir una ruta larga o incluso no hallar el camino de menor
coste.

**Cuándo usarlo:** cuando se busca una solución rápidamente y una buena
estimación de la dirección hacia la meta resulta útil, aceptando que no se
garantiza una solución óptima.

## Búsqueda A* (A-star)

A* combina el coste real del recorrido con una estimación del coste restante.
Para cada estado `n` calcula:

- `g(n)`: coste acumulado desde el inicio.
- `h(n)`: coste estimado hasta la meta.
- `f(n) = g(n) + h(n)`: prioridad usada para elegir el siguiente estado.

En [`astar-declarativo.py`](examples/astar-declarativo.py), cada movimiento
cuesta 1 al entrar en una casilla normal y 5 al entrar en `M`; las paredes no
son transitables. La misma distancia Manhattan sirve como `h(n)`. La
implementación guarda el mejor coste conocido en `costes` y los predecesores en
`padres`, con los que reconstruye el camino al llegar a `G`. Así puede preferir
un camino con más pasos si evita suficientes casillas de coste alto.

Con costes no negativos y una heurística admisible (que nunca sobreestima el
coste restante), A* encuentra una solución de coste mínimo. Manhattan es
admisible aquí porque cada movimiento cuesta al menos 1 y solo se permiten
movimientos ortogonales. Una heurística que sobrestime puede hacer que se pierda
esa garantía.

**Cuándo usarlo:** cuando importa minimizar el coste total y se dispone de una
heurística útil. En general, una mejor heurística admisible puede reducir la
exploración sin sacrificar la optimalidad.

## Comparación rápida

| Algoritmo | Cómo ordena la frontera | ¿Garantiza camino óptimo? |
| --- | --- | --- |
| BFS | Primero el descubierto hace más tiempo (cola FIFO) | Sí, si todos los pasos cuestan lo mismo |
| DFS | Primero el descubierto más recientemente (pila LIFO) | No |
| Voraz | Menor `h(n)` (estimación hasta la meta) | No |
| A* | Menor `g(n) + h(n)` | Sí, bajo las condiciones descritas arriba |

## Ejecutar los ejemplos

Desde la raíz del repositorio, ejecuta un ejemplo con Python 3, por ejemplo:

```bash
python3 01-search/examples/bfs-declarativo.py
python3 01-search/examples/greedy-declarativo.py
python3 01-search/examples/astar-declarativo.py
```

Compara el camino devuelto y la traza de estados explorados. En particular,
observa que BFS busca pocos movimientos, mientras que A* tiene en cuenta el
coste de atravesar las casillas `M`.
