from connect4.gui import connect4GUI
from battleship.BattleShip import playBattleship
from flappybird.game import Game
import pygame

class gameButton:
    subBtns = [pygame.image.load(f"assets/launcher/btn-{diff}.png") for diff in ["easy", "medium", "hard"]]
    hoverImg = pygame.image.load(f"assets/launcher/btn-hovering.png")
    difficulties = ["easy", "medium", "hard"]
    def __init__(self, name, index):
        self.game = name
        self.image = pygame.image.load(f"assets/launcher/btn-{name}.png")
        self.x = 75
        self.y = 200 + 70*index
        self.width = 450
        self.height = 60
        
        self.hovered = False
        self.difficultyIndex = None
        
    def show(self, win):
        if self.hovered:
            for i, img in enumerate(gameButton.subBtns):
                win.blit(img, (self.x + 155*i, self.y))
            win.blit(gameButton.hoverImg, (self.x + 155*self.difficultyIndex, self.y))
            
        else:
            win.blit(self.image, (self.x, self.y))
    
    def mouseOver(self, mouseCoords):
        if mouseCoords[0] >= self.x and mouseCoords[0] < self.x + self.width and mouseCoords[1] >= self.y and mouseCoords[1] < self.y + self.height:
            self.hovered = True
            self.difficultyIndex = (mouseCoords[0] - 75) // 150
            
            
        else:
            self.hovered = False
            self.difficultyIndex = None
    
    def click(self):
        if self.hovered:
            difficulty = gameButton.difficulties[self.difficultyIndex]
            
            if self.game == "connect4":
                connect4GUI(difficulty)
            elif self.game == "battleship":
                playBattleship(difficulty=difficulty)
            elif self.game == "flappybird":
                game = Game()
                game.playVsBot(self.difficultyIndex + 1)
        else:
            return
            
        

WIDTH = 600
HEIGHT = 600

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Face The AI")

bg = pygame.image.load("assets/launcher/background.png")

clock = pygame.time.Clock()
running = True

buttons = [gameButton(name, i) for i, name in enumerate(["connect4", "battleship", "flappybird"])]

while running:
    clock.tick(60)
    win.blit(bg, (0, 0))
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            for btn in buttons:
                btn.click()
                
            win = pygame.display.set_mode((WIDTH, HEIGHT))
            
    mouseCoords = pygame.mouse.get_pos()
            
    for btn in buttons:
        btn.mouseOver(mouseCoords)
        btn.show(win)
            
    pygame.display.update()
    
    
