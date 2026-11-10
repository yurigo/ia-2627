
import pygame


class GameUI:

    WIDTH = 900
    HEIGHT = 920

    BOARD_SIZE = 390
    CELL_SIZE = BOARD_SIZE // 3

    BOARD_X = (WIDTH - BOARD_SIZE) // 2
    BOARD_Y = 330

    BG = (16, 17, 22)
    CARD = (25, 27, 35)
    CELL_BG = (34, 37, 47)
    CELL_HOVER = (45, 49, 62)
    BORDER = (55, 59, 72)

    WHITE = (240, 242, 250)
    MUTED = (145, 150, 165)

    PURPLE = (155, 115, 255)
    CYAN = (70, 205, 225)
    GREEN = (75, 220, 155)

    def __init__(self, screen):

        self.screen = screen

        self.font_title = pygame.font.SysFont("arial", 52, bold=True)
        self.font_subtitle = pygame.font.SysFont("arial", 20)
        self.font_normal = pygame.font.SysFont("arial", 21)
        self.font_small = pygame.font.SysFont("arial", 16)
        self.font_symbol = pygame.font.SysFont("arial", 76, bold=True)
        self.font_score = pygame.font.SysFont("arial", 35, bold=True)

        self.reset_rect = pygame.Rect(
            self.WIDTH // 2 - 110,
            790,
            220,
            48
        )

    def draw_text(self, text, font, color, x, y):

        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))

        self.screen.blit(surface, rect)

    def draw_background(self):

        self.screen.fill(self.BG)

        pygame.draw.rect(
            self.screen,
            self.CARD,
            (0, 0, self.WIDTH, 85)
        )

        pygame.draw.line(
            self.screen,
            self.BORDER,
            (0, 85),
            (self.WIDTH, 85)
        )

        pygame.draw.rect(
            self.screen,
            self.PURPLE,
            (35, 22, 40, 40),
            border_radius=10
        )

        self.draw_text(
            "A",
            self.font_normal,
            self.WHITE,
            55,
            42
        )

        self.draw_text(
            "arcadia",
            self.font_normal,
            self.WHITE,
            130,
            42
        )

        self.draw_text(
            "JUEGOS",
            self.font_small,
            self.MUTED,
            450,
            42
        )

        self.draw_text(
            "Jugador",
            self.font_small,
            self.WHITE,
            830,
            42
        )

    def draw_header(self):

        self.draw_text(
            "● JUEGO DESTACADO",
            self.font_small,
            self.GREEN,
            450,
            125
        )

        self.draw_text(
            "3 EN RAYA",
            self.font_title,
            self.WHITE,
            450,
            175
        )

        self.draw_text(
            "El clásico juego de estrategia",
            self.font_subtitle,
            self.MUTED,
            450,
            220
        )

    def draw_scoreboard(self, game):

        card_width = 200
        card_height = 75

        x1 = 238
        x2 = 462
        y = 245

        for player, x, color in [
            ("X", x1, self.PURPLE),
            ("O", x2, self.CYAN)
        ]:

            active = (
                game.current_player == player
                and game.active
            )

            pygame.draw.rect(
                self.screen,
                self.CARD,
                (x, y, card_width, card_height),
                border_radius=12
            )

            pygame.draw.rect(
                self.screen,
                color if active else self.BORDER,
                (x, y, card_width, card_height),
                width=2,
                border_radius=12
            )

            self.draw_text(
                player,
                self.font_score,
                color,
                x + 30,
                y + 38
            )

            self.draw_text(
                "Jugador" if player == "X" else "IA",
                self.font_small,
                self.MUTED,
                x + 90,
                y + 26
            )

            self.draw_text(
                str(game.victories[player]),
                self.font_score,
                self.WHITE,
                x + 160,
                y + 43
            )

    def draw_board(self, game):

        mouse_pos = pygame.mouse.get_pos()

        for index, value in enumerate(game.board):

            row, col = divmod(index, 3)

            x = self.BOARD_X + col * self.CELL_SIZE
            y = self.BOARD_Y + row * self.CELL_SIZE

            rect = pygame.Rect(
                x + 5,
                y + 5,
                self.CELL_SIZE - 10,
                self.CELL_SIZE - 10
            )

            is_winner = (
                game.winning_combination is not None
                and index in game.winning_combination
            )

            if is_winner:
                color = (55, 65, 75)

            elif (
                rect.collidepoint(mouse_pos)
                and value == ""
                and game.active
                and game.current_player == "X"
            ):
                color = self.CELL_HOVER

            else:
                color = self.CELL_BG

            pygame.draw.rect(
                self.screen,
                color,
                rect,
                border_radius=15
            )

            if value == "X":

                self.draw_text(
                    "X",
                    self.font_symbol,
                    self.PURPLE,
                    rect.centerx,
                    rect.centery
                )

            elif value == "O":

                self.draw_text(
                    "O",
                    self.font_symbol,
                    self.CYAN,
                    rect.centerx,
                    rect.centery
                )

        self.draw_winning_line(game)

    def draw_winning_line(self, game):

        combination = game.winning_combination

        if combination is None:
            return

        def center(index):

            row, col = divmod(index, 3)

            return (
                self.BOARD_X + col * self.CELL_SIZE + self.CELL_SIZE // 2,
                self.BOARD_Y + row * self.CELL_SIZE + self.CELL_SIZE // 2
            )

        start = center(combination[0])
        end = center(combination[2])

        color = self.PURPLE if game.winner == "X" else self.CYAN

        pygame.draw.line(
            self.screen,
            color,
            start,
            end,
            6
        )

    def draw_status(self, game):

        if game.winner == "X":
            color = self.PURPLE

        elif game.winner == "O":
            color = self.CYAN

        elif not game.active:
            color = self.GREEN

        else:
            color = self.WHITE

        self.draw_text(
            game.status,
            self.font_normal,
            color,
            self.WIDTH // 2,
            755
        )

    def draw_reset_button(self):

        mouse_pos = pygame.mouse.get_pos()

        color = (
            self.CELL_HOVER
            if self.reset_rect.collidepoint(mouse_pos)
            else self.CARD
        )

        pygame.draw.rect(
            self.screen,
            color,
            self.reset_rect,
            border_radius=12
        )

        pygame.draw.rect(
            self.screen,
            self.BORDER,
            self.reset_rect,
            width=1,
            border_radius=12
        )

        self.draw_text(
            "↻  Nueva partida",
            self.font_normal,
            self.WHITE,
            self.reset_rect.centerx,
            self.reset_rect.centery
        )

    def draw_footer(self):

        pygame.draw.line(
            self.screen,
            self.BORDER,
            (0, 875),
            (self.WIDTH, 875)
        )

        self.draw_text(
            "arcadia",
            self.font_small,
            self.MUTED,
            70,
            897
        )

        self.draw_text(
            "Un espacio para jugar.",
            self.font_small,
            self.MUTED,
            820,
            897
        )

    def draw(self, game):

        self.draw_background()
        self.draw_header()
        self.draw_scoreboard(game)
        self.draw_board(game)
        self.draw_status(game)
        self.draw_reset_button()
        self.draw_footer()
