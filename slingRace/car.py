import pygame
from math import cos, sin, pi, sinh
from map import dist

class Car:
    def __init__(self, player=1):
        self.pos = [0, 300]
        self.rotation = 0
        self.vel = 5
        self.sprites = [pygame.image.load(f"slingRace/assets/spaceship{player}-{i}.png") for i in range(1, 5)]
        self.spriteIndex = 0
        
        self.topleft = [self.pos[0] - self.sprites[self.spriteIndex].get_width()//2, self.pos[1] - self.sprites[self.spriteIndex].get_height()//2]
        
        self.connectedPt = None
        self.stringLength = None
        self.pointSide = None
        self.angleRotation = None
    
    def update(self):
        
        if self.angleRotation:
            self.rotation += self.angleRotation
        
        xvel = self.vel * cos(-self.rotation)
        yvel = self.vel * sin(-self.rotation)
        
        if self.connectedPt and not self.angleRotation:
            if dist(self.connectedPt, (self.pos[0] + xvel, self.pos[1] + yvel)) > self.stringLength:
                self.angleRotation = 2 * sinh(self.vel/(2*self.stringLength))
                print(self.angleRotation)
                if self.pointSide == "right":
                    self.angleRotation *= -1
                
                self.rotation += self.angleRotation
                xvel = self.vel * cos(-self.rotation)
                yvel = self.vel * sin(-self.rotation)
            
        self.pos[0] += xvel
        self.pos[1] += yvel
        self.topleft[0] += xvel
        self.topleft[1] += yvel
    
    def show(self, win):
        
        rotated_image = pygame.transform.rotate(self.sprites[self.spriteIndex], self.rotation*(180/pi))
        new_rect = rotated_image.get_rect(center = self.sprites[self.spriteIndex].get_rect(topleft = self.topleft).center)

        win.blit(rotated_image, new_rect.topleft)
        
        if self.connectedPt:
            pygame.draw.line(win, (0, 0, 0), self.pos, self.connectedPt, 3)
        
        self.spriteIndex = (self.spriteIndex + 1) % 4
    
    def connect(self, pt, dist):
        self.connectedPt = pt
        self.stringLength = dist
        
        xvel = self.vel * cos(-self.rotation)
        yvel = self.vel * sin(-self.rotation)
        x = self.connectedPt[0]
        y = self.connectedPt[1]
        x1 = self.pos[0]
        y1 = self.pos[1]
        x2 = self.pos[0] + xvel
        y2 = self.pos[1] + yvel
        
        
        self.pointSide = "right" if (x - x1) * (y2-y1) - (y-y1) * (x2-x1) < 0 else "left"
    
    def unlink(self):
        self.connectedPt = None
        self.stringLength = None
        self.pointSide = None
        self.angleRotation = None