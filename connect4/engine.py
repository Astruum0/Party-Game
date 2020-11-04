class Engine:
    def __init__(self):

        self.board_size = 7
        self.board = [[None for _ in range(7)] for _ in range(7)]
        self.round = "X"

    def printBoard(self):
        print("┌" + "─" * self.board_size + "┐")
        for j in range(len(self.board)):
            print("│", end="")
            for i in range(len(self.board[j])):
                if self.board[i][j] == None:
                    print(" ", end="")
                elif self.board[i][j] == "X":
                    print("X", end="")
                elif self.board[i][j] == "O":
                    print("O", end="")
            print("│\n", end="")

        print("└" + "─" * self.board_size + "┘")
        print(" " + "".join(str(i) for i in range(1, self.board_size + 1)) + " ")

    def isBoardFull(self):
        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                if self.board[i][j] == None:
                    return False
        return True

    def play(self, col):
        try:
            col = int(col)
        except:
            return False
        if col < 1 or col > 7:
            return False
        row = 0
        for i in range(1, self.board_size):
            if self.board[col - 1][i] != None:
                break
            row += 1
        if row > 7:
            return False
        self.board[col - 1][row] = self.round
        self.round = "X" if self.round == "O" else "O"
        return True

    def isWinner(self):

        for player in ["X", "O"]:
            # Horizontal check
            for j in range(len(self.board)):
                for i in range(len(self.board[j]) - 3):
                    if (
                        self.board[i][j] == player
                        and self.board[i + 1][j] == player
                        and self.board[i + 2][j] == player
                        and self.board[i + 3][j] == player
                    ):
                        return player

            # Vertical check
            for j in range(len(self.board) - 3):
                for i in range(len(self.board[j])):
                    if (
                        self.board[i][j] == player
                        and self.board[i][j + 1] == player
                        and self.board[i][j + 2] == player
                        and self.board[i][j + 3] == player
                    ):
                        return player

            # Up Left – Bottom Right Diagonal check
            for j in range(len(self.board) - 3):
                for i in range(len(self.board[j]) - 3):
                    if (
                        self.board[i][j] == player
                        and self.board[i + 1][j + 1] == player
                        and self.board[i + 2][j + 2] == player
                        and self.board[i + 3][j + 3] == player
                    ):
                        return player

            # Bottom left – Up Right Diagonal check
            for j in range(3, len(self.board)):
                for i in range(len(self.board[j]) - 3):
                    if (
                        self.board[i][j] == player
                        and self.board[i + 1][j - 1] == player
                        and self.board[i + 2][j - 2] == player
                        and self.board[i + 3][j - 3] == player
                    ):
                        return player

        return None


if __name__ == "__main__":
    engine = Engine()
    while not engine.isBoardFull():
        engine.printBoard()
        playerinput = False
        while not playerinput:
            print("TURN: Player 1" if engine.round == "X" else "TURN: Player 2")
            playerinput = engine.play(input("Choose column to play (1 to 7) : "))

        w = engine.isWinner()
        if w:
            engine.printBoard()
            print("Player 1 wins !" if w == "X" else "Player 2 wins !")
            break

    if not w:
        engine.printBoard()
        print("Tie")

