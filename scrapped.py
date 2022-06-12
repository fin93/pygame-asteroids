import pygame, math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pos = [0, 0]
angle = 90


class Ship:
    def __init__(self):
        self.ship = pygame.image.load('./things/better_first_ship.svg').convert()
        self.ship = pygame.transform.scale(self.ship, (self.ship.get_width() / 10, self.ship.get_height() / 10))
        self.origional = self.ship
        self.rect = self.ship.get_rect()
        self.vel = [0, 0]
        self.pos = [0, 0]
        self.angle = 0
        self.angle_change = 0

    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.rect.center = [self.pos[0] + self.rect.width / 2, self.pos[1] + self.rect.height / 2]

    def rotate(self):
        self.angle = self.angle_change
        self.ship = pygame.transform.rotate(self.origional, self.angle)
        self.rect = self.ship.get_rect()
        self.rect.center = [self.pos[0] + self.rect.width / 2, self.pos[1] + self.rect.height / 2]
    
    def move(self, keys):
        # self.vel[0] = self.vel[0] * 0.99
        # self.vel[1] = self.vel[1] * 0.99
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vel[0] += 0.1 * math.cos(math.radians(self.angle))
            self.vel[1] += 0.1 * math.sin(math.radians(self.angle))
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vel[0] -= 0.1 * math.cos(math.radians(self.angle))
            self.vel[1] -= 0.1 * math.sin(math.radians(self.angle))
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angle_change += 1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle_change += -1
        else:
            self.angle_change = 0

        self.update()
        self.rotate()
        self.draw()

    def draw(self):
        screen.blit(self.ship, self.rect)
        


# yep = pygame.image.load('./things/better_first_ship.svg')
# yep = pygame.transform.scale(yep, (yep.get_width() / 10, yep.get_height() / 10))
# yep = pygame.transform.rotate(yep, angle)


ship = Ship()

def main():
    ship.draw()
    pygame.display.flip()
    count = 0
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        clock.tick(60)
        count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        

        ship.move(pygame.key.get_pressed())
        
        pygame.display.update()

main()