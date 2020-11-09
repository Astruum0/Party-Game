import math
import random
from copy import deepcopy


def bestMove(board, player, difficulty):
    difficulties = {"easy": 1, "medium": 2, "hard": 3, "impossible": 5}
    return (
        _minmaxAlgorithm(board, difficulties[difficulty], -math.inf, math.inf, True)[0]
        + 1
    )


def _minmaxAlgorithm(board, depth, alpha, beta, playerTurn):
    # opponent = 1 if player == 2 else 2
    validSpots = _findSpots(board)
    if depth == 0:
        return (None, _boardScore(board, 2))
    if _isWinner(board, 2):
        return (None, 100000000000000 * depth)
    if _isWinner(board, 1):
        return (None, -100000000000000 * depth)
    if len(validSpots) == 0:
        return (None, 0)

    if playerTurn:
        value = -math.inf
        bestMove, _ = random.choice(validSpots)
        for col, row in validSpots:
            copyBoard = deepcopy(board)
            copyBoard[col][row] = 2
            _, new_score = _minmaxAlgorithm(copyBoard, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                bestMove = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (bestMove, value)
    else:
        value = math.inf
        bestMove, _ = random.choice(validSpots)
        for col, row in validSpots:
            copyBoard = deepcopy(board)
            copyBoard[col][row] = 1
            _, new_score = _minmaxAlgorithm(copyBoard, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                bestMove = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (bestMove, value)


def _isWinner(board, player):
    board_w = len(board)
    board_h = len(board[0])

    # Horizontal check
    for j in range(board_h):
        for i in range(board_w - 3):
            if (
                board[i][j] == player
                and board[i + 1][j] == player
                and board[i + 2][j] == player
                and board[i + 3][j] == player
            ):
                return player

    # Vertical check
    for j in range(board_h - 3):
        for i in range(board_w):
            if (
                board[i][j] == player
                and board[i][j + 1] == player
                and board[i][j + 2] == player
                and board[i][j + 3] == player
            ):
                return player

    # Up Left – Bottom Right Diagonal check
    for j in range(board_h - 3):
        for i in range(board_w - 3):
            if (
                board[i][j] == player
                and board[i + 1][j + 1] == player
                and board[i + 2][j + 2] == player
                and board[i + 3][j + 3] == player
            ):
                return player

    # Bottom left – Up Right Diagonal check
    for j in range(3, board_h):
        for i in range(board_w - 3):
            if (
                board[i][j] == player
                and board[i + 1][j - 1] == player
                and board[i + 2][j - 2] == player
                and board[i + 3][j - 3] == player
            ):
                return player


def _findSpots(board):
    spots = []
    for col in range(len(board)):
        if board[col][0] == None:
            for row in range(len(board[col])):
                if board[col][row] != None:
                    spots.append((col, row - 1))
                    break
                if row == len(board[col]) - 1:
                    spots.append((col, row))
                    break
    return spots


def _boardScore(board, player):
    board_w = len(board)
    board_h = len(board[0])

    score = 0

    # Center column
    centerColumn = [board[len(board) // 2][i] for i in range(board_h)]
    score += centerColumn.count(player) * 3

    # Vertical
    for col in range(board_w):
        fullColumn = [board[col][i] for i in range(board_h)]
        for row in range(board_h - 3):
            group4pieces = fullColumn[row : row + 4]
            score += _scoreFrom4Pieces(group4pieces, player)

    # Horizontal
    for row in range(board_h):
        fullRow = [board[i][row] for i in range(board_w)]
        for col in range(board_w - 3):
            group4pieces = fullRow[col : col + 4]
            score += _scoreFrom4Pieces(group4pieces, player)

    # Up Left – Bottom Right Diagonal check
    for col in range(board_w - 3):
        for row in range(board_h - 3):
            group4pieces = [board[col + i][row + i] for i in range(4)]
            score += _scoreFrom4Pieces(group4pieces, player)

    # Bottom left – Up Right Diagonal check
    for col in range(board_w - 3):
        for row in range(board_h - 3):
            group4pieces = [board[col + 3 - i][row + i] for i in range(4)]
            score += _scoreFrom4Pieces(group4pieces, player)

    return score


def _scoreFrom4Pieces(group, player):
    score = 0
    opponent = 2 if player == 1 else 1

    if group.count(player) == 4:
        score += 100
    elif group.count(player) == 3 and group.count(None) == 1:
        score += 5
    elif group.count(player) == 2 and group.count(None) == 2:
        score += 2

    if group.count(opponent) == 3 and group.count(None) == 1:
        score -= 4

    return score


def _copyOfBoard(board):
    copyB = [[None for _ in range(len(board[0]))] for _ in range(len(board))]
    for c in range(len(board)):
        for r in range(len(board[c])):
            copyB[c][r] = board[c][r]
    return copyB

