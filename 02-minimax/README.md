# Minimax y poda alfa-beta

Minimax es un algoritmo de búsqueda para juegos de dos participantes, por turnos,
deterministas y de información perfecta. Supone que ambos jugadores eligen
siempre la jugada que más les conviene: el jugador **MAX** intenta maximizar la
puntuación y **MIN** intenta minimizarla. La puntuación se define desde el punto
de vista de MAX; por ejemplo, una victoria de MAX vale `+1`, una derrota `-1` y
un empate `0`.

## Minimax

El árbol de juego representa las posiciones posibles: cada nodo es un estado del
tablero y cada arista es una jugada legal. Las hojas son estados terminales (o
estados de profundidad limitada) cuyo valor se puede evaluar. El valor de un
nodo se calcula de abajo hacia arriba:

```text
V(s) = utilidad(s)                         si s es terminal
V(s) = max(V(hijo))                        si juega MAX
V(s) = min(V(hijo))                        si juega MIN
```

El siguiente pseudocódigo muestra la búsqueda recursiva. `copiarYJugar` crea un
nuevo estado, por lo que el tablero de la llamada actual permanece intacto.

```text
función minimax(estado, jugador, profundidad):
    si X ha ganado en estado: devolver (10 - profundidad, ninguna)
    si O ha ganado en estado: devolver (profundidad - 10, ninguna)
    si no quedan jugadas legales: devolver (0, ninguna)

    si jugador = X:
        mejorValor = -infinito
    si no:
        mejorValor = +infinito
    mejorJugada = ninguna

    para cada jugada legal en estado:
        siguienteEstado = copiarYJugar(estado, jugada)
        siguienteJugador = O si jugador = X; si no, X
        (valor, _) = minimax(siguienteEstado, siguienteJugador,
                             profundidad + 1)

        si jugador = X y valor > mejorValor:
            mejorValor = valor
            mejorJugada = jugada
        si jugador = O y valor < mejorValor:
            mejorValor = valor
            mejorJugada = jugada

    devolver (mejorValor, mejorJugada)
```

Así, una jugada de MAX se valora suponiendo que MIN responderá con la mejor
contrajugada posible, y viceversa. La elección de MAX es la jugada legal cuyo
hijo tiene el valor más alto. Este razonamiento es óptimo para los supuestos del
modelo, pero el número de nodos crece exponencialmente: con un factor de
ramificación `b` y profundidad `d`, el coste es `O(b^d)` y la memoria de una
búsqueda recursiva en profundidad es `O(d)` (sin contar el estado del juego).

En [`examples/minimax.py`](examples/minimax.py) se aplica el algoritmo al
tres en raya. Una victoria de X recibe `10 - profundidad`, una victoria de O
`profundidad - 10` y el empate `0`; así se prefieren las victorias rápidas y se
retrasan las derrotas. El parámetro `jugador` alterna entre MAX (X) y MIN (O).
El ejemplo explora el árbol completo, algo práctico para este juego pequeño.

## Poda alfa-beta

La poda alfa-beta devuelve la misma jugada que minimax, pero evita explorar
ramas que ya no pueden cambiar la decisión. Mantiene dos cotas durante el
recorrido:

- `alfa`: el mejor valor que MAX puede garantizar en el camino actual.
- `beta`: el mejor (menor) valor que MIN puede garantizar en el camino actual.

Cuando `alfa >= beta`, el resto de los hijos del nodo no puede mejorar el
resultado para quien lo visita y se puede descartar. La poda es correcta porque
solo omite alternativas que no podrían ser elegidas frente a una respuesta
mejor ya encontrada. Su eficacia depende del orden de exploración: en el mejor
caso puede reducir el trabajo a `O(b^(d/2))`, mientras que en el peor caso sigue
siendo `O(b^d)`. El espacio de búsqueda en profundidad continúa siendo `O(d)`.

El pseudocódigo es igual a minimax salvo por las cotas, que se actualizan después
de cada hijo, y el corte cuando ya no es posible mejorar la decisión:

```text
función minimaxAlfaBeta(estado, jugador, profundidad, alfa, beta):
    si X ha ganado en estado: devolver (10 - profundidad, ninguna)
    si O ha ganado en estado: devolver (profundidad - 10, ninguna)
    si no quedan jugadas legales: devolver (0, ninguna)

    mejorJugada = ninguna
    si jugador = X:
        mejorValor = -infinito
        para cada jugada legal en estado:
            siguienteEstado = copiarYJugar(estado, jugada)
            (valor, _) = minimaxAlfaBeta(siguienteEstado, O,
                                         profundidad + 1, alfa, beta)
            si valor > mejorValor:
                mejorValor = valor
                mejorJugada = jugada
            alfa = max(alfa, mejorValor)
            si alfa >= beta: salir del bucle
    si no:
        mejorValor = +infinito
        para cada jugada legal en estado:
            siguienteEstado = copiarYJugar(estado, jugada)
            (valor, _) = minimaxAlfaBeta(siguienteEstado, X,
                                         profundidad + 1, alfa, beta)
            si valor < mejorValor:
                mejorValor = valor
                mejorJugada = jugada
            beta = min(beta, mejorValor)
            si alfa >= beta: salir del bucle

    devolver (mejorValor, mejorJugada)
```

[`examples/minimax_alpha_beta.py`](examples/minimax_alpha_beta.py) resuelve el
mismo estado inicial de tres en raya con estas cotas.

En juegos mayores, como cuatro en línea, normalmente no es viable explorar hasta
el final. Se limita la profundidad y se usa una función heurística para estimar
los estados no terminales; la poda alfa-beta sigue siendo aplicable.

## Prueba los juegos

- [Jugar al tres en raya](https://super-web-lovat.vercel.app)
- [Jugar a cuatro en línea](https://super-web-lovat.vercel.app)

## Ejecutar los ejemplos

Desde la raíz del repositorio, con Python 3:

```bash
python3 02-minimax/examples/minimax.py
python3 02-minimax/examples/minimax_alpha_beta.py
```

Ambos programas imprimen la mejor jugada calculada para X y su valor minimax.
