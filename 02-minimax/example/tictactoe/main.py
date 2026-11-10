
import pygame
import sys

from game import TicTacToe
from ui import GameUI


def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (GameUI.WIDTH, GameUI.HEIGHT)
    )

    pygame.display.set_caption("3 en Raya — Arcadia")

    clock = pygame.time.Clock()

    game = TicTacToe()
    ui = GameUI(screen)

    running = True
    ai_time = None

    while running:

        clock.tick(60)

        # ==========================
        # EVENTOS
        # ==========================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button != 1:
                    continue

                mouse_x, mouse_y = event.pos

                # Nueva partida
                if ui.reset_rect.collidepoint(event.pos):

                    game.reset_game()
                    ai_time = None
                    continue

                # Movimiento del jugador
                if (
                    game.active
                    and game.current_player == "X"
                    and ai_time is None
                ):

                    col = (
                        mouse_x - ui.BOARD_X
                    ) // ui.CELL_SIZE

                    row = (
                        mouse_y - ui.BOARD_Y
                    ) // ui.CELL_SIZE

                    if 0 <= row < 3 and 0 <= col < 3:

                        index = row * 3 + col

                        moved = game.make_move(index)

                        if (
                            moved
                            and game.active
                            and game.current_player == "O"
                        ):

                            ai_time = pygame.time.get_ticks() + 400

        # ==========================
        # TURNO DE LA IA
        # ==========================

        if (
            ai_time is not None
            and pygame.time.get_ticks() >= ai_time
        ):

            ai_time = None

            if game.active and game.current_player == "O":
                game.ai_move()

        # ==========================
        # DIBUJAR INTERFAZ
        # ==========================

        ui.draw(game)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
