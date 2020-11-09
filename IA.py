from random import choice, randint
import numpy as np
import matplotlib.pyplot as plt

class IA():
    def __init__(self, Player):
        self.Player = Player
        self.depth = 5000

    def seach_best_move(self):
        self.dico = {}
        list_boat = []
        for boat in self.Player.destroyed:
            if not self.Player.CheckDestroyed(boat[0] - 1):
                list_boat.append(self.Player.boat[boat[0] - 1])
        for i in range(self.depth):
            for boat in list_boat:
                self.hunt(boat[1])
        self.destroy()
        #print(self.Player.attack_board.board)
        #print(self.heatmap())
        coo = list(self.dico.keys())[list(self.dico.values()).index(max(self.dico.values()))]
        if coo[0] < 0 or coo[1] < 0:
            del self.dico[coo]
        return(list(self.dico.keys())[list(self.dico.values()).index(max(self.dico.values()))])


    def hunt(self, boat):
        placed = False
        board = self.Player.attack_board.get_board(copy = True)
        tries = 0
        while placed == False:
            if tries == self.depth/10:
                placed = True
            vertical = randint(0,1)
            if vertical:
                x, y = randint(0,9 - boat + 1), randint(0,9)
                valid = True
                for i in range(x, x + boat):
                    if board[i][y] == 6:
                        valid = False
                if valid == True:
                    for i in range(x, x + boat):
                        if (i % 2 == 0 and y % 2 == 1) or (i % 2 == 1 and y % 2 == 0):
                            if (i, y) in self.dico:
                                self.dico[(i,y)] += 1
                            else:
                                if board[i][y] == 0:
                                    self.dico[(i,y)] = 1
                        placed = True
            else:
                x, y = randint(0,9), randint(0,9 - boat + 1)
                valid = True
                for i in range(y, y + boat):
                    if board[x][i] == 11:
                        valid = False
                if valid == True:
                    for i in range(y, y + boat):
                        if (i % 2 == 0 and x % 2 == 1) or (i % 2 == 1 and x % 2 == 0):
                            if (x, i) in self.dico:
                                self.dico[(x,i)] += 1
                            else:
                                if board[x][i] == 0:
                                    self.dico[(x,i)] = 1
                        placed = True
            tries += 1

    def destroy(self):
        board = self.Player.attack_board.board
        for i in range(10):
            for j in range(10):
                neighbours = []
                if int(board[i][j]) != 0 and int(board[i][j]) != 6 and int(board[i][j]) != 7:
                    for adj_x, adj_y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        try:
                            if board[adj_x][adj_y] == board[i][j]:
                                neighbours.append((adj_x, adj_y))
                        except:
                            pass
                    if len(neighbours) == 0:
                        for adj_x, adj_y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                            try:
                                if int(board[adj_x][adj_y]) == 0:
                                    if (adj_x, adj_y) in self.dico:
                                        self.dico[(adj_x, adj_y)] += 10000
                                    else:
                                        self.dico[(adj_x, adj_y)] = 10000
                            except:
                                pass
                    else:
                        for x, y in neighbours:
                            xaxys = x - i
                            yaxys = y - j
                            if xaxys != 0:
                                try:
                                    if int(board[i-xaxys][j]) == 0:
                                        if (i-xaxys, j) in self.dico:
                                            self.dico[(i-xaxys, j)] += 10000
                                        else:
                                            self.dico[(i-xaxys, j)] = 10000
                                except:
                                    pass
                            elif yaxys != 0:
                                try:
                                    if int(board[i][j-yaxys]) == 0:
                                        if (i, j-yaxys) in self.dico:
                                            self.dico[(i, j-yaxys)] += 10000
                                        else:
                                            self.dico[(i, j-yaxys)] = 10000
                                except:
                                    pass


    def heatmap(self):
        heatmap = np.zeros((10, 10))
        for i in range(10):
            for j in range(10):
                try:
                    heatmap[i][j] = self.dico[(i,j)] / 1000
                except:
                    heatmap[i][j] = 0
        return(heatmap)

