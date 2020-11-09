import numpy as np
from random import randint

class Board:
    def __init__(self):
        self.board = np.zeros((10, 10))

    def get_board(self, copy=False):
        if copy:
            return self.board.copy()
        else:
            return self.board

class Player:
    def __init__(self):
        self.boat = [(1,5), (2,4), (3,3), (4,3), (5,2)]
        self.destroyed = [[i, 0] for i in range(1,6)]
        self.defense_board = Board()
        self.attack_board = Board()
        self.random_placement(self.boat)
        self.destroyed_boats = 0

    def random_placement(self, boats):
        for boat_value, boat_length in boats:
            placed = False
            while placed == False:
                vertical = randint(0,1)
                if vertical:
                    x, y = randint(0,9 - boat_length + 1), randint(0,9)
                    valid = True
                    for i in range(x, x + boat_length):
                        if self.defense_board.board[i][y] != 0:
                            valid = False
                    if valid == True:
                        for i in range(x, x + boat_length):
                            self.defense_board.board[i][y] = boat_value
                            placed = True
                else:
                    x, y = randint(0,9), randint(0,9 - boat_length + 1)
                    valid = True
                    for i in range(y, y + boat_length):
                        if self.defense_board.board[x][i] != 0:
                            valid = False
                    if valid == True:
                        for i in range(y, y + boat_length):
                            self.defense_board.board[x][i] = boat_value
                            placed = True

    def SendHit(self, x, y, Player):
        if self.validHit(x, y):
            try:
                id_boat = int(Player.defense_board.board[x][y])
            except:
                id_boat = int(Player.Player.defense_board.board[x][y])
            if id_boat == 0:
                self.attack_board.board[x][y] = 6
                print(f"Plouf en {x+1},{y+1}")
            else:
                print(f"Touché en {x+1},{y+1}")
                self.attack_board.board[x][y] = id_boat
                self.destroyed[id_boat-1][1] += 1
                if self.CheckDestroyed(id_boat-1):
                    self.Destroy(id_boat)
                    self.destroyed_boats += 1
                    if self.destroyed_boats == 5:
                        return True
            return False
        else:
            return False

    def validHit(self, x, y):
        if 0 <= x <= 9 and 0 <= y <= 9:
            if self.attack_board.board[x][y] == 0:
                return True
        return False

    def CheckDestroyed(self, id_boat):
        if list(self.boat[id_boat]) == self.destroyed[id_boat]:
            return True
        return False

    def Destroy(self, boat):
        for i in range(10):
            for j in range(10):
                if int(self.attack_board.board[i][j]) == boat:
                    self.attack_board.board[i][j] = 7
                

        
