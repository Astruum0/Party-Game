from connect4.engine import Engine
from connect4.solver import bestMove
from connect4.animation import DropTokenAnimation
import pygame


class connect4GUI:
    def __init__(self, difficulty):
        self.w = 700
        self.h = 700
        self.token_size = self.w // 7
        self.engine = Engine()

        self.difficulty = difficulty

        self.win = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Connect 4")

        self.imgs = {
            "grid": pygame.image.load("assets/connect4/grid.png"),
            "tokenP1": pygame.image.load("assets/connect4/tokenP1.png"),
            "tokenP2": pygame.image.load("assets/connect4/tokenP2.png"),
        }

        self.winner = None, None

        self.dropdown = None

        self.clock = pygame.time.Clock()
        self.play()

        # bestCol = bestMove(self.engine.board, 2, "impossible")
        # row = self.engine.getRow(bestCol)

        # self.dropdown = DropTokenAnimation(
        #     self.engine.round,
        #     (
        #         (bestCol - 1) * self.token_size,
        #         self.token_size + row * self.token_size,
        #     ),
        # )
        # self.animationLoop()

        # self.engine.play(bestCol)

    def play(self):

        run = True
        while run:
            self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    run = False

                if e.type == pygame.MOUSEBUTTONDOWN:
                    col = (e.pos[0] // 100) + 1

                    # col = bestMove(self.engine.board, 2, "impossible")

                    row = self.engine.getRow(col)

                    if type(row) == int:
                        self.dropdown = DropTokenAnimation(
                            self.engine.round,
                            (
                                (col - 1) * self.token_size,
                                self.token_size + row * self.token_size,
                            ),
                        )
                        self.animationLoop()

                        self.engine.play(col)

                        self.show()

                        self.winner = self.engine.gameIsEnded()
                        if self.winner[0]:
                            self.endScreen()
                            break

                        bestCol = bestMove(self.engine.board, 2, self.difficulty)
                        row = self.engine.getRow(bestCol)

                        self.dropdown = DropTokenAnimation(
                            self.engine.round,
                            (
                                (bestCol - 1) * self.token_size,
                                self.token_size + row * self.token_size,
                            ),
                        )
                        self.animationLoop()

                        self.engine.play(bestCol)

                        self.winner = self.engine.gameIsEnded()
                        if self.winner[0]:
                            self.endScreen()
                            break

            self.show()

    def endScreen(self):
        count = 0
        while count < 120:
            self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    break

            self.show()

            count += 1

        self.reset()

    def reset(self):
        self.winner = None, None
        self.engine.reset()

    def show(self):
        self.win.fill((220, 220, 220))

        mouseX, _ = pygame.mouse.get_pos()
        if not self.winner[0] and not self.dropdown:
            self.win.blit(
                self.imgs[f"tokenP{self.engine.round}"],
                (
                    mouseX - self.imgs[f"tokenP{self.engine.round}"].get_size()[0] // 2,
                    0,
                ),
            )

        for col in range(self.engine.board_w):
            for row in range(self.engine.board_h):
                if self.engine.board[col][row] in [1, 2]:
                    self.win.blit(
                        self.imgs[f"tokenP{self.engine.board[col][row]}"],
                        (self.token_size * col, self.token_size * (row + 1)),
                    )

        if self.dropdown:
            self.win.blit(
                self.imgs[f"tokenP{self.dropdown.player}"],
                (self.dropdown.pos[0], self.dropdown.pos[1]),
            )

        self.win.blit(self.imgs["grid"], (0, self.h - self.imgs["grid"].get_size()[1]))

        if self.winner[0] in [1, 2]:
            pygame.draw.line(
                self.win,
                (0, 0, 0),
                (
                    self.winner[1][0][0] * self.token_size + self.token_size // 2,
                    self.winner[1][0][1] * self.token_size + self.token_size * 1.5,
                ),
                (
                    self.winner[1][1][0] * self.token_size + self.token_size // 2,
                    self.winner[1][1][1] * self.token_size + self.token_size * 1.5,
                ),
                5,
            )

        pygame.display.update()

    def animationLoop(self):

        while self.dropdown:
            self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.dropdown = None
                    break

            self.dropdown.update()
            self.show()

            if self.dropdown.ended:
                self.dropdown = None
                break

        self.show()


if __name__ == "__main__":
    gui = connect4GUI("impossible")
    gui.play()
