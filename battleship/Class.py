import numpy as np
from random import randint
from time import sleep


class Board:
    def __init__(self):
        self.board = np.zeros((10, 10))

    def get_board(self, copy=False):
        if copy:
            return self.board.copy()
        else:
            return self.board


class Player:

    #  _____ _                        _    __                  _   _
    # /  ___| |                      | |  / _|                | | (_)
    # \ `--.| |__   __ _ _ __ ___  __| | | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
    #  `--. \ '_ \ / _` | '__/ _ \/ _` | |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
    # /\__/ / | | | (_| | | |  __/ (_| | | | | |_| | | | | (__| |_| | (_) | | | \__ \
    # \____/|_| |_|\__,_|_|  \___|\__,_| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

    def __init__(self, difficulty, player_board):
        self.boat = [(1, 5), (2, 4), (3, 3), (4, 3), (5, 2)]
        self.destroyed = [[i, 0] for i in range(1, 6)]
        self.defense_board = Board()
        self.attack_board = Board()
        self.destroyed_boats = 0

        # Set searching depth for monte-carlo simulation
        if difficulty:
            self.random_placement(self.boat)
            diff = {"easy": 0.1, "medium": 1, "hard": 5}
            self.difficulty = difficulty
            self.depth = int(diff[difficulty] * 10000)
            self.images = []
        else:
            self.player_placement(player_board)

    def player_placement(self, board):
        for i, line in enumerate(board):
            for j, column in enumerate(line):
                self.defense_board.board[i][j] = column

    # Send a shot to the opponent defense board
    def SendHit(self, x, y, Player):
        if self.validHit(x, y):
            id_boat = int(Player.defense_board.board[x][y])
            if id_boat == 0:
                self.attack_board.board[x][y] = 6
                Player.defense_board.board[x][y] = 6
                return (True, False, False)
            else:
                Player.defense_board.board[x][y] = 12
                self.attack_board.board[x][y] = id_boat
                self.destroyed[id_boat - 1][1] += 1
                if self.CheckDestroyed(id_boat - 1):
                    self.Destroy(id_boat)
                    self.destroyed_boats += 1
                    if self.destroyed_boats == 5:
                        return (True, True, True)
                return (True, True, False)
        else:
            return (False, False, False)

    # Check if the shot can be launched
    def validHit(self, x, y):
        if 0 <= x <= 9 and 0 <= y <= 9:
            if self.attack_board.board[x][y] == 0:
                return True
        return False

    # Check if a boat was destroyed
    def CheckDestroyed(self, id_boat):
        if list(self.boat[id_boat]) == self.destroyed[id_boat]:
            return True
        return False

    # Modify the attack board when a board is destroyed
    def Destroy(self, boat):
        for i in range(10):
            for j in range(10):
                if int(self.attack_board.board[i][j]) == boat:
                    self.attack_board.board[i][j] = 12

    #   ___  _____    __                  _   _
    #  / _ \|_   _|  / _|                | | (_)
    # / /_\ \ | |   | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
    # |  _  | | |   |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
    # | | | |_| |_  | | | |_| | | | | (__| |_| | (_) | | | \__ \
    # \_| |_/\___/  |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

    # Place boat randomly on the defense board
    def random_placement(self, boats):
        for boat_value, boat_length in boats:
            placed = False
            while placed == False:
                vertical = randint(0, 1)
                if vertical:
                    x, y = randint(0, 9 - boat_length + 1), randint(0, 9)
                    valid = True
                    for i in range(x, x + boat_length):
                        if self.defense_board.board[i][y] != 0:
                            valid = False
                        for adj_x, adj_y in [
                            (i - 1, y),
                            (i + 1, y),
                            (i, y - 1),
                            (i, y + 1),
                        ]:
                            try:
                                if self.defense_board.board[adj_x][adj_y] != 0:
                                    valid = False
                            except:
                                pass
                    if valid == True:
                        for i in range(x, x + boat_length):
                            self.defense_board.board[i][y] = boat_value
                            placed = True
                else:
                    x, y = randint(0, 9), randint(0, 9 - boat_length + 1)
                    valid = True
                    for i in range(y, y + boat_length):
                        if self.defense_board.board[x][i] != 0:
                            valid = False
                        for adj_x, adj_y in [
                            (x - 1, i),
                            (x + 1, i),
                            (x, i - 1),
                            (x, i + 1),
                        ]:
                            try:
                                if self.defense_board.board[adj_x][adj_y] != 0:
                                    valid = False
                            except:
                                pass
                    if valid == True:
                        for i in range(y, y + boat_length):
                            self.defense_board.board[x][i] = boat_value
                            placed = True

    # Main AI method
    def search_best_move(self):
        self.dico = {}
        list_boat = []
        if self.difficulty != "easy":
            # Add all the remaining boat of the opponent defense board to a list
            for boat in self.destroyed:
                if not self.CheckDestroyed(boat[0] - 1):
                    list_boat.append(self.boat[boat[0] - 1])
            # Launch the monte-carlo simulation depth times
            for _ in range(self.depth):
                for boat in list_boat:
                    self.monte_carlo(boat[1])
        else:
            self.random_move()
        # Let the hunt begin
        self.hunt()
        # Get the best move with the heatmap
        coo = list(self.dico.keys())[
            list(self.dico.values()).index(max(self.dico.values()))
        ]
        if coo[0] < 0 or coo[1] < 0:
            del self.dico[coo]
        return list(self.dico.keys())[
            list(self.dico.values()).index(max(self.dico.values()))
        ]

    def random_move(self):
        valid = False
        while not(valid):
            x, y = randint(0,9), randint(0,9)
            if self.validHit(x, y):
                valid = True
                self.dico[(x, y)] = 1
                sleep(1)

    # Main searching tool, place boat randomly and affect a probability to each tile. Output an only statistic determined heatmap
    def monte_carlo(self, boat):
        placed = False
        board = self.attack_board.get_board(copy=True)
        tries = 0
        while placed == False:
            if tries == 100:
                placed = True
            vertical = randint(0, 1)
            if vertical:
                x, y = randint(0, 9 - boat + 1), randint(0, 9)
                valid = True
                for i in range(x, x + boat):
                    if board[i][y] != 0:
                        valid = False
                if valid == True:
                    for i in range(x, x + boat):
                        if (
                            (i % 2 == 0 and y % 2 == 1)
                            or (i % 2 == 1 and y % 2 == 0)
                            or self.difficulty in ["easy", "medium"]
                        ):
                            if (i, y) in self.dico:
                                self.dico[(i, y)] += 1
                            else:
                                if board[i][y] == 0:
                                    self.dico[(i, y)] = 1
                        placed = True
            else:
                x, y = randint(0, 9), randint(0, 9 - boat + 1)
                valid = True
                for i in range(y, y + boat):
                    if board[x][i] != 0:
                        valid = False
                if valid == True:
                    for i in range(y, y + boat):
                        if (
                            (i % 2 == 0 and x % 2 == 1)
                            or (i % 2 == 1 and x % 2 == 0)
                            or self.difficulty in ["easy", "medium"]
                        ):
                            if (x, i) in self.dico:
                                self.dico[(x, i)] += 1
                            else:
                                if board[x][i] == 0:
                                    self.dico[(x, i)] = 1
                        placed = True
            tries += 1

    # Specialized searching tool, change the heatmap probability if a boat is partially sunk
    def hunt(self):
        board = self.attack_board.board
        for i in range(10):
            for j in range(10):
                neighbours = []
                if int(board[i][j]) not in [0, 6, 12]:
                    for adj_x, adj_y in [
                        (i - 1, j),
                        (i + 1, j),
                        (i, j - 1),
                        (i, j + 1),
                    ]:
                        try:
                            if board[adj_x][adj_y] == board[i][j]:
                                neighbours.append((adj_x, adj_y))
                        except:
                            pass
                    if len(neighbours) == 0:
                        for adj_x, adj_y in [
                            (i - 1, j),
                            (i + 1, j),
                            (i, j - 1),
                            (i, j + 1),
                        ]:
                            try:
                                if int(board[adj_x][adj_y]) == 0:
                                    if (adj_x, adj_y) in self.dico:
                                        self.dico[(adj_x, adj_y)] += self.depth
                                    else:
                                        self.dico[(adj_x, adj_y)] = self.depth
                            except:
                                pass
                    else:
                        for x, y in neighbours:
                            xaxys = x - i
                            yaxys = y - j
                            if xaxys != 0:
                                try:
                                    if int(board[i - xaxys][j]) == 0:
                                        if (i - xaxys, j) in self.dico:
                                            self.dico[(i - xaxys, j)] += self.depth
                                        else:
                                            self.dico[(i - xaxys, j)] = self.depth
                                except:
                                    pass
                            elif yaxys != 0:
                                try:
                                    if int(board[i][j - yaxys]) == 0:
                                        if (i, j - yaxys) in self.dico:
                                            self.dico[(i, j - yaxys)] += self.depth
                                        else:
                                            self.dico[(i, j - yaxys)] = self.depth
                                except:
                                    pass