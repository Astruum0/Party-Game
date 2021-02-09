from Class import Board, Player
from random import randint
import pygame
import sys
import imageio
from start import place_boat

# Get arguments for difficulty
try:
    difficulty = sys.argv[1]
    if difficulty not in (["easy", "medium", "hard"]):
        raise TypeError
except:
    print(
        "Argument non valide, difficulté mise a normal, lancez Battleship.py [easy, medium, hard] pour choisir votre difficulté"
    )
    difficulty = "medium"
# Launch first screen to place the boat
board = list(place_boat())

# Define colors and dimensions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WIDTH = 30
HEIGHT = 30
MARGIN = 7

pygame.init()
win = pygame.display.set_mode((800, 380))
pygame.display.set_caption("Bataille navale")
clock = pygame.time.Clock()

# Create instance for the player and the AI
player = Player(None, board)
bot = Player(difficulty, None)

finished = False
running = True
bot_turn = randint(0, 1)
coup = 0
# Game Loop
while running:
    clock.tick(60)
    pygame.display.update()

    # Player and AI turn
    if bot_turn:
        coo = bot.search_best_move()
        output = bot.SendHit(coo[0], coo[1], player)
        if output[2]:
            running = False
            winner = "bot"
        if output[0] and not (output[1]):
            bot_turn = False
        coup += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN) - 11
            row = pos[1] // (HEIGHT + MARGIN)
            if not (bot_turn):
                output = player.SendHit(row, column, bot)
                if output[2]:
                    running = False
                    winner = "Player"
                if output[0] and not (output[1]):
                    bot_turn = True
    # Draw game
    win.fill(WHITE)
    for index, board in enumerate(
        [player.attack_board.board, player.defense_board.board]
    ):
        for row, i in enumerate(board):
            for column, case in enumerate(i):
                offset = 0
                if index == 0:
                    offset = 400
                if case == 0:
                    color = BLUE
                elif case == 6:
                    color = BLACK
                elif case == 12:
                    color = RED
                else:
                    color = GREEN
                pygame.draw.rect(
                    win,
                    color,
                    [
                        (MARGIN + WIDTH) * column + MARGIN + offset,
                        (MARGIN + HEIGHT) * row + MARGIN,
                        WIDTH,
                        HEIGHT,
                    ],
                )
    pygame.display.flip()
print(f"{winner} a gagné en {coup} coups")
imageio.mimsave("heatmap/heatmap.gif", bot.images, fps=2)
pygame.quit()
