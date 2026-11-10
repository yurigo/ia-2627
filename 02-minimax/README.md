# Minimax

Maximizo la ia.
Minimizo el jugador.

```pseudocodigo

funcion minimax (tablero, profundidad, isMaximizing)

    # estado final
    si juego se gana
        retorno 1000
    si juego se pierde
        retorno -1000
    si juego se empata
        retorno 0

    si (isMaximizing) entonces
        bestScore = -infinito

        para cada estado del tablero
            
            hago el movimiento
            nuevoTablero = (algo nuevo)

            score = minimax(nuevoTablero , depth + 1, false)

            deshacer el movimiento
            el tablero sigue intacto.

            bestScore = max ( score ,bestScore )


        fin para

        return bestScore

    sino
        # estoy minimizando
        bestScore = +infinito

        por cada estado del tablero
            hacer el movimiento

            nuevoTablero = (algo nuevo)

            score = minimax ( nuevoTablero, depth + 1 , true )

            deshago el movivmiento
            tablero está intacto

            bestScore = min ( bestScore, score )

        fin por

        retorna bestScore

    fin si

finfuncion

```


# Minimax alfa beta prunning

(TBD)