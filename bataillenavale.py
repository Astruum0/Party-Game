from Class import Board, Player
from random import randint
import pygame
import sys

try:
    difficulty = sys.argv[1]
    if difficulty not in(["easy","medium","hard","impossible"]): 
        raise TypeError
except:
    print("Argument non valide, difficulté mise a normal")
    difficulty = "medium"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WIDTH = 60
HEIGHT = 60
MARGIN = 15

pygame.init()
win = pygame.display.set_mode((1600, 765))
pygame.display.set_caption("Bataille navale")
clock = pygame.time.Clock()

player = Player(None)
bot = Player(difficulty)
finished = False
running = True
bot_turn = False
while running:
    clock.tick(60)
    pygame.display.update()
    
    if bot_turn:
        coo = bot.seach_best_move()
        output = bot.SendHit(coo[0], coo[1], player)
        if output[2]:
            running = False
            winner = "bot"
        if not(output[0]) and not(output[1]):
            bot_turn = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN) - 11
            row = pos[1] // (HEIGHT + MARGIN)
            if not(bot_turn):
                output = player.SendHit(row, column, bot)
                if output[2]:
                    running = False
                    winner = "Player"
                if not(output[0]) and not(output[1]):
                    bot_turn = True
    win.fill(WHITE)
    for index, board in enumerate([player.attack_board.board, player.defense_board.board]):
        for row, i in enumerate(board):
            for column, case in enumerate(i):
                offset = 0
                if index == 0:
                    offset = 835
                if case == 0:
                    color = BLUE
                elif case == 6:
                    color = BLACK
                elif case == 7:
                    color = RED
                else:
                    color = GREEN
                pygame.draw.rect(win,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN + offset,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])


    pygame.display.flip()
print(f"{winner} a gagné")
pygame.quit()
