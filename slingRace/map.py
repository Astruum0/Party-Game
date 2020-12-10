import pygame
from math import sqrt

def dist(p1, p2):
    return sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))

class Map:
    def __init__(self):
        self.rotatePoints = [(300, 150), (800, 400)]
    
    def show(self, win):
        for rp in self.rotatePoints:
            pygame.draw.circle(win, (0, 0, 0), rp, 5)
        
    def chooseClosestPoint(self, coords):
        closestpt = self.rotatePoints[0]
        distMin = dist(coords, closestpt)
        for pt in self.rotatePoints:
            actualDist = dist(coords, pt)
            if actualDist < distMin:
                distMin = actualDist
                closestpt = pt
        return closestpt, distMin
                