import pygame
import numpy as np
import copy


def place_boat():
    # Color init
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    WIDTH = 30
    HEIGHT = 30
    MARGIN = 7

    # Pygame init
    pygame.init()
    win = pygame.display.set_mode((800, 380))
    pygame.display.set_caption("Bataille navale")
    retry = pygame.image.load("assets/battleship/retry.png")
    ok = pygame.image.load("assets/battleship/ok.png")
    FPS = 60

    # Variable init
    boats = [(0, 5), (1, 4), (2, 3), (3, 3), (4, 2)]
    boat = []
    space = 37
    offset_boat = 550
    rectangle_draging = False
    clock = pygame.time.Clock()
    running = True
    board = np.zeros((10, 10))
    is_horizontal = [True, True, True, True, True]
    placed = [False, False, False, False, False]

    for id, length in boats:
        rectangle = []
        for i in range(length):
            rectangle.append(
                pygame.rect.Rect((space * i) + offset_boat, (40 * id) + 80, 30, 30)
            )
        boat.append(rectangle)
    # Rotate boat horizontally
    def rotate_hor(boats, carre):
        is_horizontal[boats] = not (is_horizontal[boats])
        new_abciss = copy_boat[boats][carre].x
        new_ord = copy_boat[boats][carre].y
        for i, treated in enumerate(copy_boat[boats]):
            if i < carre:
                treated.x, treated.y = new_abciss, new_ord + (
                    (space * (carre - i)) * -1
                )
            elif i > carre:
                treated.x, treated.y = new_abciss, new_ord + (space * (i - carre))

    # Rotate boat verticaly
    def rotate_ver(boats, carre):
        is_horizontal[boats] = not (is_horizontal[boats])
        new_abciss = copy_boat[boats][carre].x
        new_ord = copy_boat[boats][carre].y
        for i, treated in enumerate(copy_boat[boats]):
            if i < carre:
                treated.x, treated.y = (
                    new_abciss + ((space * (carre - i)) * -1),
                    new_ord,
                )
            elif i > carre:
                treated.x, treated.y = new_abciss + (space * (i - carre)), new_ord

    # Place boat if the position is valid
    def place(treated, coo):
        id, case = treated
        if placed[id] == False:
            row = coo[1] // (HEIGHT + MARGIN)
            column = coo[0] // (WIDTH + MARGIN)
            length = boats[id][1]
            before, after = case, (length - 1) - case
            if is_horizontal[id]:
                if column - before >= 0 and column + after <= 9:
                    valid = True
                    for i in range(column - before, column + after + 1):
                        if board[row][i] == 0:
                            board[row][i] = id + 1
                        else:
                            valid = False
                            break
                    if valid:
                        placed[id] = True
            else:
                if row - before >= 0 and row + after <= 9:
                    valid = True
                    for i in range(row - before, row + after + 1):
                        if board[i][column] == 0:
                            board[i][column] = id + 1
                        else:
                            valid = False
                            break
                    if valid:
                        placed[id] = True

    copy_boat = copy.deepcopy(boat)

    # Main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    for i, instance in enumerate(copy_boat):
                        for j, rect in enumerate(instance):
                            if rect.collidepoint(event.pos):
                                moved = (i, j)
                                rectangle_draging = True
                                mouse_x, mouse_y = event.pos
                                offset_x = rect.x - mouse_x
                                offset_y = rect.y - mouse_y
                    x, y = event.pos
                    if 720 < x < 780 and 300 < y < 360:
                        board = np.zeros((10, 10))
                        is_horizontal = [True, True, True, True, True]
                        placed = [False, False, False, False, False]
                        copy_boat = copy.deepcopy(boat)
                    if 640 < x < 700 and 300 < y < 360 and not False in placed:
                        running = False
                if event.button == 3:
                    for i, instance in enumerate(copy_boat):
                        for j, rect in enumerate(instance):
                            if rect.collidepoint(event.pos):
                                rotated = (i, j)
                                if is_horizontal[i]:
                                    rotate_hor(i, j)
                                else:
                                    rotate_ver(i, j)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    rectangle_draging = False
                    try:
                        place(moved, event.pos)
                    except:
                        pass
            elif event.type == pygame.MOUSEMOTION:
                if rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    for i, rect in enumerate(copy_boat[moved[0]]):
                        rect.x = (
                            mouse_x + offset_x + (moved[1] - i) * space * -1
                            if is_horizontal[moved[0]]
                            else mouse_x + offset_x
                        )
                        rect.y = (
                            mouse_y + offset_y + (moved[1] - i) * space * -1
                            if not (is_horizontal[moved[0]])
                            else mouse_y + offset_y
                        )
        win.fill(WHITE)
        for row, i in enumerate(board):
            for column, case in enumerate(i):
                color = BLUE if case == 0 else RED
                pygame.draw.rect(
                    win,
                    color,
                    [
                        (MARGIN + WIDTH) * column + MARGIN,
                        (MARGIN + HEIGHT) * row + MARGIN,
                        WIDTH,
                        HEIGHT,
                    ],
                )
        for i, instance in enumerate(copy_boat):
            if placed[i] == False:
                for rect in instance:
                    pygame.draw.rect(win, RED, rect)
        win.blit(retry, (720, 300))
        if not (False in placed):
            win.blit(ok, (640, 300))
        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    if False in placed:
        return None
    return board
