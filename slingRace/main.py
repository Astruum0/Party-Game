import pygame
from map import Map
from car import Car
 
def dist(x1, y1, x2, y2):
    return abs((x1**2 + y1**2) - (x2**2 + y2**2))


class Main:
    def __init__(self):
        self.W = 1000
        self.H = 700
        
        self.win = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Sling Race")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.map = Map()
        self.car = Car()
        
        self.run()
    
    
    def run(self):
        while self.running:
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                closestPoint, distanceToPoint = self.map.chooseClosestPoint(self.car.pos)
                if distanceToPoint <= 200:
                    if not self.car.connectedPt:
                        self.car.connect(closestPoint, distanceToPoint)
                else:
                    self.car.unlink()
            else:
                self.car.unlink()
            
            self.clock.tick(60)
            self.win.fill((120, 120, 120))
            
            self.car.update()
            
            self.map.show(self.win)
            self.car.show(self.win)
            
            pygame.display.update()
            
if __name__ == "__main__":
    Main()
            
            
    
    