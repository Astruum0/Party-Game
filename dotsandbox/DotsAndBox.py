import numpy as np
import pygame
import math
import time
from dotsandbox.ai import get_best_move

class Game:
    def __init__(self, taille):
        self.taille = taille
        self.board = np.zeros((self.taille, taille))
        self.lines = {}
        self.square_won = {}
        self.score = [0, 0]
        self.current_player = 0
        self.running = True
        self.player1 = 1
        self.player2 = 2

    def draw_line(self, start, end, player):
        if (start, end) not in self.lines:
            self.lines[(start, end)] = player
            self.check_square()

    def check_square(self):
        next = False
        for x in range(0, self.taille - 1):
            for y in range(0, self.taille - 1):
                to_check = [(x * self.taille + y, x * self.taille + y + 1),
                            ((x + 1) * self.taille + y, (x + 1) * self.taille + y + 1),
                            (x * self.taille + y, (x + 1) * self.taille + y),
                            (x * self.taille + y + 1, (x + 1) * self.taille + y + 1)]
                valid = True
                for check in to_check:
                    if check not in self.lines:
                        valid = False
                if valid == True:
                    if (x, y) not in self.square_won:
                        self.square_won[(x,y)] = self.current_player
                        self.score[self.current_player] += 1
                        self.current_player = not(self.current_player)
                        self.check_win()    
        self.current_player = not(self.current_player)                    

    def check_win(self):
        if len(self.square_won) == (self.taille - 1) * (self.taille - 1):
            self.running = False


def trace_lines(game, win, player, click = False):
    taille, offset, ecart, width, color = 5, 40, 80, 5, [(255, 0, 0), (0, 0,255)]
    temp = []
    pos = pygame.mouse.get_pos()

    x, y = math.floor((pos[0] - offset) / ecart), math.floor((pos[1] - offset) / ecart)
    if 0 <= x < taille - 1 and 0 <= y < taille - 1:
        center = ((x+1) * ecart, (y+1) * ecart)
        off_x, off_y = pos[0] - center[0], pos[1] - center[1]

        for i, number in enumerate([off_x,off_y]):
            if abs(number) > 10:
                temp.append((i, number))

        if temp:
            maxi = 0
            index = 0
            for i, number in temp:
                if abs(number) > maxi:
                    maxi = number
                    index = i
            if index == 0:
                if number > 0:
                    pygame.draw.line(win, color[player], ((x + 1) * ecart + offset, y * ecart + offset), ((x + 1) * ecart + offset, (y + 1) * ecart + offset), width)
                    if click == True:
                        game.draw_line((y * taille) + x + 1, (y + 1) * taille + x + 1, player)
                else:
                    pygame.draw.line(win, color[player], (x * ecart + offset, y * ecart + offset), (x * ecart + offset, (y + 1) * ecart + offset), width)
                    if click == True:
                        game.draw_line((y * taille) + x, (y + 1) * taille + x, player)
            else:
                if number > 0:
                    pygame.draw.line(win, color[player], (x * ecart + offset, (y + 1) * ecart + offset), ((x + 1) * ecart + offset, (y + 1) * ecart + offset), width)
                    if click == True:
                        game.draw_line((y + 1) * taille + x, (y + 1) * taille + x + 1, player)
                else:
                    pygame.draw.line(win, color[player], (x * ecart + offset, y * ecart + offset), ((x + 1) * ecart + offset, y * ecart + offset), width)
                    if click == True:
                        game.draw_line(y * taille + x, y * taille + x + 1, player)

def draw_board(game, win):
    taille, offset, ecart, width, color = 5, 40, 80, 5, [(255, 0, 0), (0, 0,255)]
    pygame.font.init()
    myfont = pygame.font.SysFont('Arial Bold', 40)
    for i, line in enumerate(game.board):
        for j, case in enumerate(line):
            coo = (ecart * j + offset, ecart * i + offset)
            pygame.draw.circle(win, (0, 0, 0), coo, width)
            index = (taille * i) + j   
            if (index, index+1) in game.lines.keys():
                pygame.draw.line(win, color[game.lines[(index, index+1)]], coo, (coo[0] + ecart, coo[1]), width)
            if (index, index+taille) in game.lines.keys():
                pygame.draw.line(win, color[game.lines[(index, index+taille)]], coo, (coo[0], coo[1] + ecart), width)
    for square, player in game.square_won.items():
        x, y = square
        if player == 0:
            textsurface = myfont.render('R', False, color[0])
        else:
            textsurface = myfont.render('B', False, color[1])
        win.blit(textsurface,(y * ecart + offset + (ecart / 3), x * ecart + offset + (ecart / 3) ))

def play(difficulty):
    taille, offset, ecart, width, color = 5, 40, 80, 5, [(255, 0, 0), (0, 0,255)]
    pygame.font.init()
    font = pygame.font.SysFont('Arial Bold', 40)
    dimension = offset * 2 + (taille - 1) * ecart
    win = pygame.display.set_mode((dimension, dimension))
    pygame.display.set_caption("Dots and Boxes")
    clock = pygame.time.Clock()
    game = Game(taille)

    while game.running: 
        win.fill((255, 255, 255))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and game.current_player == 0:
                trace_lines(game, win, game.current_player, True)
            
        if game.current_player == 1:
            best_move = get_best_move(game, taille, difficulty)
            game.draw_line(best_move[0], best_move[1], game.current_player)

        trace_lines(game, win, game.current_player, None)
        draw_board(game, win)

        pygame.display.update()

    run = True
    while run:
        win.fill((255, 255, 255))
        winner = game.score.index(max(game.score))
        if winner == 0:
            text = font.render("You win!", True, (0,0,0))
        else:
            text = font.render("You lose!", True, (0,0,0))
        text_rect = text.get_rect(center=(dimension/2, dimension/2))
        win.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

if __name__ == "__main__":
    play("hard")