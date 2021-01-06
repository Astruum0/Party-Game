import pygame
import neat
import os
from bird import Bird
from ground import Ground
from pipe import Pipe
from score import Score

class game:
    def __init__(self):
        pygame.init()
        self.w = 576
        self.h = 1024
        self.clock = pygame.time.Clock() 
        self.win = pygame.display.set_mode((self.w, self.h))
        
        self.gameOverBoucle = False
        pygame.display.set_caption("Flappy Bird")
        self.bg = pygame.image.load("assets/flappybird/bg1.png").convert_alpha()
        self.startingimage = pygame.image.load("assets/flappybird/startingscreen.png").convert_alpha()
        self.launch = False
        self.list_pipes = []
        self.bird = Bird(self.w//6, 400 - 25)
        self.ground = Ground()
        self.score = Score()
        
        

    def runSolo(self):
        self.timeClock = 0
        self.game = True
        self.all_sprites_list = pygame.sprite.RenderUpdates()
        self.all_sprites_list.add(self.bird)
        self.all_sprites_list.add(self.ground)
        self.win.blit(self.bg, (0, 0))
        pygame.display.update()

        while self.game: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game = False
                    return

            self.updateScore()
            self.ground.update()
            self.bird.updateImgs()
            self.all_sprites_list.remove(self.bird)
            self.all_sprites_list.add(self.bird)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not self.launch and self.timeClock > 5:
                self.bird.jump()
                self.launch = True
                self.win.blit(self.bg, (0, 0))
                self.list_pipes.append(Pipe())
                self.all_sprites_list.add(self.list_pipes[-1])

            if keys[pygame.K_SPACE] and self.launch:
                self.bird.jump()

            if self.launch:
                self.bird.affectGravity()
                if self.list_pipes[-1].rect.x <= (2*self.w)//5:    
                    self.list_pipes.append(Pipe())
                    self.all_sprites_list.add(self.list_pipes[-1])
                if self.list_pipes[0].rect.x <= -self.list_pipes[0].w:
                    self.all_sprites_list.remove(self.list_pipes[0])
                    self.list_pipes.pop(0)
                for pipe in self.list_pipes:
                    pipe.update()
                    if self.bird.collide(pipe):
                        self.launch = False
                        self.game = False
                        self.gameOverScreen()
                        return
            else:
                self.win.blit(self.startingimage, (117, 150))

            self.all_sprites_list.remove(self.ground)
            self.all_sprites_list.add(self.ground)

            
            if self.game:                
                self.all_sprites_list.update()
                self.all_sprites_list.clear(self.win, self.bg)
                spriteslist = self.all_sprites_list.draw(self.win)
                pygame.display.update(spriteslist)
                self.score.draw(self.win)
                self.timeClock += 1
            self.clock.tick(30)
    
    def runBot(self, genomes, config):
        nets = []
        ge = []
        birds = []
        
        for i, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            birds.append(Bird(self.w//6, 400 - 25))
            g.fitness = 0
            ge.append(g)
        
        self.timeClock = 0
        self.game = True
        # self.all_sprites_list = pygame.sprite.RenderUpdates()
        # self.all_sprites_list.add(self.bird)
        # self.all_sprites_list.add(self.ground)
        
        # pygame.display.update()
        
        self.list_pipes.append(Pipe())
        # self.all_sprites_list.add(self.list_pipes[-1])

        while self.game: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game = False
                    pygame.quit()
                
            pipe_ind = 0
            if len(birds) > 0:
                if len(self.list_pipes) > 1 and birds[0].rect.x > self.list_pipes[0].rect.x + self.list_pipes[0].rect.w:
                    pipe_ind = 1
            else:
                self.game = False
                self.reset()
                break
                    
            for x, bird in enumerate(birds):
                bird.updateImgs()
                bird.affectGravity()
                
                ge[x].fitness += 0.01
                output = nets[x].activate((bird.rect.y, abs(bird.rect.y - (self.list_pipes[pipe_ind].y + 100)), abs(bird.rect.y - (self.list_pipes[pipe_ind].y - 100))))
                
                if output[0] > 0.5:
                    bird.jump()
                            

            self.ground.update()
            
            
            
                
            if self.list_pipes[-1].rect.x <= (2*self.w)//5:    
                self.list_pipes.append(Pipe())
                # self.all_sprites_list.add(self.list_pipes[-1])
            if self.list_pipes[0].rect.x <= -self.list_pipes[0].w:
                # self.all_sprites_list.remove(self.list_pipes[0])
                self.list_pipes.pop(0)
            for pipe in self.list_pipes:
                pipe.update()
                for i, bird in enumerate(birds):
                    if bird.collide(pipe):
                        ge[i].fitness -= 1
                        birds.pop(i)
                        nets.pop(i)
                        ge.pop(i)
                        
                    if pipe.rect.x <= bird.rect.x and pipe.rect.x >= bird.rect.x + self.ground.xspeed:
                        for g in ge:
                            g.fitness += 5


            # self.all_sprites_list.remove(self.ground)
            # self.all_sprites_list.add(self.ground)

            
            if self.game:        
                self.win.blit(self.bg, (0, 0))
                for pipe in self.list_pipes:
                    pipe.draw(self.win)
                self.ground.draw(self.win)
                
                for bird in birds:
                    bird.draw(self.win)
                        
                # self.all_sprites_list.update()
                # self.all_sprites_list.clear(self.win, self.bg)
                # spriteslist = self.all_sprites_list.draw(self.win)
                # pygame.display.update(spriteslist)
                # self.score.draw(self.win)
                
                
                pygame.display.update()
                self.timeClock += 1
            self.clock.tick(30)

    def reset(self):
        self.score.reset()
        self.bird.reset()
        # for pipe in self.list_pipes:
        #     self.all_sprites_list.remove(pipe)
        self.list_pipes = []
        self.ground.reset()
        self.win.blit(self.bg, (0, 0))

    def updateScore(self):
        for pipe in self.list_pipes:
            if pipe.rect.x <= self.bird.rect.x and pipe.rect.x >= self.bird.rect.x + self.ground.xspeed:
                self.score.addscore()
                self.win.blit(self.bg, (0, 0))

    def gameOverScreen(self):
        self.gameOverBoucle = True
        self.timeClock = 0
        while self.gameOverBoucle:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.gameOverBoucle = False
                    return
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.timeClock >= 20:
                self.gameOverBoucle = False
                for pipe in self.list_pipes:
                    self.all_sprites_list.remove(pipe)    
                self.reset()
                self.runSolo()
                return
            self.score.updateNewHighscore(self.win)
            self.all_sprites_list.clear(self.win, self.bg)
            self.bird.draw(self.win)
            for pipe in self.list_pipes:
                pipe.draw(self.win)
            self.ground.draw(self.win)
            self.score.draw(self.win)
            self.score.draw_panel(self.win)
            pygame.display.update()

            self.timeClock += 1
        pygame.quit()

def run():
    jeu = game()
    
    
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    print(config_path)
    
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    
    winner = p.run(jeu.runBot, 50)

run()

# jeu = game()
# jeu.runSolo()
