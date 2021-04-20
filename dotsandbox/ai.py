from random import choice
banned = []

def get_best_move(game_state, width, difficulty):
    if difficulty == "easy":
        return random_move(game_state.lines, width, difficulty)
    if difficulty == "medium":
        return find_complete(game_state.lines, width, difficulty)
    if difficulty == "hard":
        return find_complete(game_state.lines, width, difficulty)


def random_move(game_state, width, difficulty):
    legal_move = list(
    [(i, i + 1) for i in range(width * width - 1) if (i + 1) % width != 0]
    + [(i, i + width) for i in range(width * (width - 1))]
    - game_state.keys()
    )
    if difficulty == "hard":
        legal_move_hard = (list(list(set(legal_move)-set(banned)) + list(set(banned)-set(legal_move))))
        try:
            return(choice(legal_move_hard))
        except:
            pass
    return(choice(legal_move))

def find_complete(game_state, width, difficulty):
    global banned
    banned = []
    for x in range(0, width - 1):
        for y in range(0, width - 1):
            to_check = [(x * width + y, x * width + y + 1),
                        ((x + 1) * width + y, (x + 1) * width + y + 1),
                        (x * width + y, (x + 1) * width + y),
                        (x * width + y + 1, (x + 1) * width + y + 1)]
            valid = 0
            not_drawn = []
            for line in to_check:
                if line in game_state:
                    valid += 1
                else:
                    not_drawn.append(line)
            if valid == 3:
                return not_drawn[0]
            if valid == 2 and difficulty == "hard":
                banned.append(not_drawn[0])
                banned.append(not_drawn[1])
    return random_move(game_state, width, difficulty)
            