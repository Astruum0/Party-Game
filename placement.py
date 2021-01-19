import pygame
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WIDTH = 30
HEIGHT = 30
MARGIN = 7

pygame.init()
win = pygame.display.set_mode((800, 380))
pygame.display.set_caption("Bataille navale")

FPS = 144

pygame.display.set_caption("Tracking System")

boats = [(0, 5), (1, 4), (2, 3), (3, 3), (4,2)]
boat = []
space = 37
offset_boat = 550

for id, length in boats:
    rectangle = []
    for i in range(length):
        rectangle.append(pygame.rect.Rect((space * i) + offset_boat,
                                          (40 * id) + 80
                                          , 30, 30))
    boat.append(rectangle)

rectangle_draging = False

clock = pygame.time.Clock()

running = True

board = np.zeros((10, 10))

is_horizontal = [True, True, True, True, True]

def rotate_hor(boats, carre):
    global boat, is_horizontal, space
    is_horizontal[boats] = not(is_horizontal[boats])
    new_abciss = boat[boats][carre].x
    new_ord = boat[boats][carre].y
    for i, treated in enumerate(boat[boats]):
        if i < carre:
            treated.x, treated.y = new_abciss, new_ord + ((space * (carre - i)) * -1)
        elif i > carre:
            treated.x, treated.y = new_abciss, new_ord + (space * (i - carre))

def rotate_ver(boats, carre):
    global boat, is_horizontal, space
    is_horizontal[boats] = not(is_horizontal[boats])
    new_abciss = boat[boats][carre].x
    new_ord = boat[boats][carre].y
    for i, treated in enumerate(boat[boats]):
        if i < carre:
            treated.x, treated.y = new_abciss + ((space * (carre - i)) * -1), new_ord
        elif i > carre:
            treated.x, treated.y = new_abciss + (space * (i - carre)), new_ord
            
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                for i, instance in enumerate(boat):
                    for j, rect in enumerate(instance):   
                        if rect.collidepoint(event.pos):
                            moved = (i, j)
                            rectangle_draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = rect.x - mouse_x
                            offset_y = rect.y - mouse_y

            if event.button == 3:
                for i, instance in enumerate(boat):
                    for j, rect in enumerate(instance):   
                        if rect.collidepoint(event.pos):
                            rotated = (i, j)
                            if is_horizontal[i]:
                                print(boat[i])
                                rotate_hor(i, j)
                                print(boat[i])
                            else:
                                print(boat[i])
                                rotate_ver(i, j)
                                print(boat[i])

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                for i, rect in enumerate(boat[moved[0]]):
                    rect.x = mouse_x + offset_x + (moved[1] - i) * space * -1 if is_horizontal[moved[0]] else mouse_x + offset_x
                    rect.y = mouse_y + offset_y + (moved[1] - i) * space * -1 if not(is_horizontal[moved[0]]) else mouse_y + offset_y

    win.fill(WHITE)
    for row, i in enumerate(board):
        for column, case in enumerate(i):
            pygame.draw.rect(win,
                                BLUE,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])


    for instance in boat:
        for rect in instance:
            pygame.draw.rect(win, RED, rect)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()