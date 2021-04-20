import numpy as np
import pygame
import math
from ai import get_best_move

difficulty = "hard"
taille = 5
offset = 40
ecart = 80
current_player = 0
width = 5
color = ["red", "blue"]
score = [0, 0]
pygame.init()
dimension = offset * 2 + (taille - 1) * ecart
win = pygame.display.set_mode((dimension, dimension))
pygame.display.set_caption("Dots and Boxes")
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont('Arial Bold', 40)

class Game:
    def __init__(self):
        self.board = np.zeros((taille, taille))
        self.lines = {}
        self.square_won = {}
        self.player1 = 1
        self.player2 = 2

    def draw_line(self, start, end, player):
        if (start, end) not in self.lines:
            self.lines[(start, end)] = player
            self.check_square()

    def check_square(self):
        global current_player
        next = False
        for x in range(0, taille - 1):
            for y in range(0, taille - 1):
                to_check = [(x * taille + y, x * taille + y + 1),
                            ((x + 1) * taille + y, (x + 1) * taille + y + 1),
                            (x * taille + y, (x + 1) * taille + y),
                            (x * taille + y + 1, (x + 1) * taille + y + 1)]
                valid = True
                for check in to_check:
                    if check not in self.lines:
                        valid = False
                if valid == True:
                    if (x, y) not in self.square_won:
                        self.square_won[(x,y)] = current_player
                        score[current_player] += 1
                        current_player = not(current_player)
                        self.check_win()    
        current_player = not(current_player)                    

    def check_win(self):
        global running
        if len(self.square_won) == (taille - 1) * (taille - 1):
            running = False



def trace_lines(game, player, click = False):
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
                    pygame.draw.line(win, color[current_player], ((x + 1) * ecart + offset, y * ecart + offset), ((x + 1) * ecart + offset, (y + 1) * ecart + offset), width)
                    if click == True:
                        game.draw_line((y * taille) + x + 1, (y + 1) * taille + x + 1, player)
                else:
                    pygame.draw.line(win, color[current_player], (x * ecart + offset, y * ecart + offset), (x * ecart + offset, (y + 1) * ecart + offset), width)
                    if click == True:
                        game.draw_line((y * taille) + x, (y + 1) * taille + x, player)
            else:
                if number > 0:
                    pygame.draw.line(win, color[current_player], (x * ecart + offset, (y + 1) * ecart + offset), ((x + 1) * ecart + offset, (y + 1) * ecart + offset), width)
                    if click == True:
                        game.draw_line((y + 1) * taille + x, (y + 1) * taille + x + 1, player)
                else:
                    pygame.draw.line(win, color[current_player], (x * ecart + offset, y * ecart + offset), ((x + 1) * ecart + offset, y * ecart + offset), width)
                    if click == True:
                        game.draw_line(y * taille + x, y * taille + x + 1, player)

def draw_board():
    for i, line in enumerate(game.board):
        for j, case in enumerate(line):
            coo = (ecart * j + offset, ecart * i + offset)
            pygame.draw.circle(win, "black", coo, width)
            index = (taille * i) + j   
            if (index, index+1) in game.lines.keys():
                pygame.draw.line(win, color[game.lines[(index, index+1)]], coo, (coo[0] + ecart, coo[1]), width)
            if (index, index+taille) in game.lines.keys():
                pygame.draw.line(win, color[game.lines[(index, index+taille)]], coo, (coo[0], coo[1] + ecart), width)
    for square, player in game.square_won.items():
        x, y = square
        if player == 0:
            textsurface = myfont.render('R', False, "red")
        else:
            textsurface = myfont.render('B', False, "blue")
        win.blit(textsurface,(y * ecart + offset + (ecart / 3), x * ecart + offset + (ecart / 3) ))


running = True
game = Game()

while running: 
    win.fill("white")
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and current_player == 0:
            trace_lines(game, current_player, True)
        
    if current_player == 1:
        best_move = get_best_move(game, taille, difficulty)
        game.draw_line(best_move[0], best_move[1], current_player)

    trace_lines(None, None)
    draw_board()

    pygame.display.flip()

print(f"Le gagnant est joueur {score.index(max(score)) + 1} ( {max(score)} points )") 
pygame.quit()

