from colorama import init, Fore, Style
from solver import bestMove
import sys


class Engine:
    def __init__(self):

        self.board_w = 7
        self.board_h = 6
        self.board_size = 7
        self.board = [[None for _ in range(6)] for _ in range(7)]
        self.round = 1

    def printBoard(self):
        print("┌" + "─" * self.board_w * 2 + "─┐")
        for j in range(self.board_h):
            print("│", end="")
            for i in range(self.board_w):
                if self.board[i][j] == None:
                    print("  ", end="")
                elif self.board[i][j] == 1:
                    print(Fore.RED + " ●" + Style.RESET_ALL, end="")
                elif self.board[i][j] == 2:
                    print(Fore.YELLOW + " ●" + Style.RESET_ALL, end="")
            print(" │\n", end="")

        print("└" + "─" * self.board_w * 2 + "─┘")
        print("  " + " ".join(str(i) for i in range(1, self.board_w + 1)) + "  ")

    def isBoardFull(self):
        for j in range(self.board_h):
            for i in range(self.board_w):
                if self.board[i][j] == None:
                    return False
        return True

    def getRow(self, col):
        try:
            col = int(col)
        except:
            return False
        if col < 1 or col > 7:
            return False
        row = -1
        for j in range(self.board_h):
            if self.board[col - 1][j] != None:
                break
            row += 1
        if row == -1:
            return False
        return row

    def play(self, col):
        try:
            col = int(col)
        except:
            return False
        if col < 1 or col > 7:
            return False
        row = -1
        for j in range(self.board_h):
            if self.board[col - 1][j] != None:
                break
            row += 1
        if row == -1:
            return False
        self.board[col - 1][row] = self.round
        self.round = 1 if self.round == 2 else 2
        return True

    def gameIsEnded(self):
        if self.isBoardFull():
            return 3, None
        else:
            return self.isWinner()

    def reset(self):
        self.board = [[None for _ in range(6)] for _ in range(7)]
        self.round = 1

    def isWinner(self):

        for player in [1, 2]:
            # Horizontal check
            for j in range(self.board_h):
                for i in range(self.board_w - 3):
                    if (
                        self.board[i][j] == player
                        and self.board[i + 1][j] == player
                        and self.board[i + 2][j] == player
                        and self.board[i + 3][j] == player
                    ):
                        return player, ((i, j), (i + 3, j))

            # Vertical check
            for j in range(self.board_h - 3):
                for i in range(self.board_w):
                    if (
                        self.board[i][j] == player
                        and self.board[i][j + 1] == player
                        and self.board[i][j + 2] == player
                        and self.board[i][j + 3] == player
                    ):
                        return player, ((i, j), (i, j + 3))

            # Up Left – Bottom Right Diagonal check
            for j in range(self.board_h - 3):
                for i in range(self.board_w - 3):
                    if (
                        self.board[i][j] == player
                        and self.board[i + 1][j + 1] == player
                        and self.board[i + 2][j + 2] == player
                        and self.board[i + 3][j + 3] == player
                    ):
                        return player, ((i, j), (i + 3, j + 3))

            # Bottom left – Up Right Diagonal check
            for j in range(3, self.board_h):
                for i in range(self.board_w - 3):
                    if (
                        self.board[i][j] == player
                        and self.board[i + 1][j - 1] == player
                        and self.board[i + 2][j - 2] == player
                        and self.board[i + 3][j - 3] == player
                    ):
                        return player, ((i, j), (i + 3, j - 3))

        return None, None


if __name__ == "__main__":
    init()
    engine = Engine()

    try:
        mode = sys.argv[1]
    except:
        mode = "2P"

    while not engine.isBoardFull():
        engine.printBoard()

        if engine.round == 1 or mode == "2P":
            playerinput = False
            while not playerinput:
                print("TURN: Player 1" if engine.round == 1 else "TURN: Player 2")
                playerinput = engine.play(input("Choose column to play (1 to 7) : "))
        else:
            difficulty = "medium"
            if mode.lower() in ["easy", "medium", "hard", "impossible"]:
                difficulty = mode
            bestCol = bestMove(engine.board, 2, mode)
            engine.play(bestCol)

        w = engine.isWinner()[0]
        if w:
            engine.printBoard()
            print("Player 1 wins !" if w == 1 else "Player 2 wins !")
            break

    if not w:
        engine.printBoard()
        print("Tie")
