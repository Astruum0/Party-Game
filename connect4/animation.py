class DropTokenAnimation:
    def __init__(self, player, destination):

        self.player = player

        self.pos = [destination[0], 0]
        self.velY = 0
        self.accY = 9
        self.destinationY = destination[1]

        self.bounces = 0
        self.bounceLosss = 0.5

        self.ended = False

    def update(self):
        self.velY += self.accY
        self.pos[1] += self.velY

        if self.pos[1] >= self.destinationY:
            self.pos[1] = self.destinationY
            self.velY *= -self.bounceLosss
            self.bounces += 1

        if self.bounces == 3:
            self.pos[1] = self.destinationY
            self.ended = True
