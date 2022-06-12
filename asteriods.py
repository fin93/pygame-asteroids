import pygame, math, random, gc

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
SIZE =  10
RATIO = [2.7 * SIZE, 1 * SIZE]
OFFPUT = 17
SPEED = 5

class Menu:
    def __init__(self, screen, main):
        self.screen = screen
        self.main = main
        self.font = pygame.font.SysFont("sans-serif", 30)
        self.text = self.font.render("Press Space to Start", 1, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.score = self.read_score()[0]
        self.actual_score = self.read_score()[1]
        self.score_rect = self.score.get_rect()
        self.score_rect.center = (WIDTH // 2, HEIGHT // 3)

    def read_score(self):
        try:
            f = open('score.txt', 'r')
            data = f.read()
            return [self.font.render(f'Highscore  {data}', 1, (255, 255, 255)), data]
        except:
            ok = open('score.txt', 'w')
            ok.close()
            self.actual_score = 0
            self.write_score()
            del self
            Main()

    def write_score(self):
        f = open('score.txt', 'w')
        f.write(str(self.actual_score)) 

    def run(self):
        clock = pygame.time.Clock()
        count = 0
        while True:
            clock.tick(60)
            screen.fill((0, 0, 0))
            count += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.main.main()

            self.text_rect.center = (WIDTH // 2, HEIGHT // 2 + math.sin(count / 30) * 20)
            self.screen.blit(self.text, self.text_rect)
            self.score_rect.center = (WIDTH // 2, HEIGHT // 3 + math.sin(count / 30) * 20)
            self.screen.blit(self.score, self.score_rect)
            pygame.display.update()
    
    def game_over(self, score):
        self.text = self.font.render("Game Over", 1, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.screen.blit(self.text, self.text_rect)

        if score >= int(self.actual_score): 
            self.actual_score = score
            yes = self.font.render("New Highscore!", 1, (255, 255, 255))
            yes_rect = yes.get_rect()
            yes_rect.center = (WIDTH // 2, HEIGHT // 3)
            self.screen.blit(yes, yes_rect)
            self.write_score()

        self.text = self.font.render("Press Space For Menu", 1, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (WIDTH // 2, HEIGHT // 1.5)
        self.screen.blit(self.text, self.text_rect)

        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_SPACE:
                        mainn = Main()

class Ship:
    def __init__(self, yes):
        self.pos_initial = [yes[0], yes[1]]
        self.pos_u = [self.pos_initial[0], self.pos_initial[1] - RATIO[0]]    
        self.pos_l = [self.pos_initial[0] - RATIO[1], self.pos_initial[1]]    
        self.pos_r = [self.pos_initial[0] + RATIO[1], self.pos_initial[1]]    
        self.angle = 0
        self.vel = [0, 0]
        self.move_angle = 0
        self.cancel = 0
        self.fired = []

    def calculate_positions(self):
        self.pos_u = [self.pos_initial[0] - math.sin(self.angle) * RATIO[0], self.pos_initial[1] - math.cos(self.angle) * RATIO[0]]
        self.pos_l = [self.pos_initial[0] - math.cos(self.angle) * RATIO[1], self.pos_initial[1] + math.sin(self.angle) * RATIO[1]]
        self.pos_r = [self.pos_initial[0] + math.cos(self.angle) * RATIO[1], self.pos_initial[1] - math.sin(self.angle) * RATIO[1]]

    def draw(self): 
        pygame.draw.polygon(screen, (120, 120, 120), (self.pos_l, self.pos_r, self.pos_u), 2)

    def get_keys(self, keys):
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_angle -= math.pi / 1800
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_angle += math.pi / 1800
        elif self.move_angle > 0:  
            self.move_angle -= 0.01
        elif self.move_angle < 0: 
            self.move_angle += 0.01
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vel[0] += (self.pos_u[0] - self.pos_initial[0]) / 500
            self.vel[1] += (self.pos_u[1] - self.pos_initial[1]) / 500
        else:
            self.vel[0] *= 0.98
            self.vel[1] *= 0.98

    def wall(self):
        if self.pos_l[0] > WIDTH or self.pos_r[0] > WIDTH or self.pos_u[0] > WIDTH and not self.cancel:
            if self.pos_u[0] - self.pos_initial[0] < 0: self.pos_initial[0] =  RATIO[0]
            else:   self.pos_initial[0] =  RATIO[1]
            self.cancel = 1
        elif self.pos_l[0] < 0 or self.pos_r[0] < 0 or self.pos_u[0] < 0 and not self.cancel:
            if self.pos_u[0] - self.pos_initial[0] > 0: self.pos_initial[0] = WIDTH - RATIO[0]   
            else:   self.pos_initial[0] = WIDTH - RATIO[1]
            self.cancel = 1
        else: self.cancel = 0
        if self.pos_l[1] > HEIGHT or self.pos_r[1] > HEIGHT or self.pos_u[1] > HEIGHT and not self.cancel:
            if self.pos_u[1] - self.pos_initial[1] < 0: self.pos_initial[1] = RATIO[0]
            else:   self.pos_initial[1] = RATIO[1]
            self.cancel = 1
        elif self.pos_l[1] < 0 or self.pos_r[1] < 0 or self.pos_u[1] < 0 and not self.cancel:
            if self.pos_u[0] - self.pos_initial[0] > 0: self.pos_initial[1] = HEIGHT - RATIO[0]
            else:   self.pos_initial[1] = HEIGHT - RATIO[1]
            self.cancel = 1
        else: self.cancel = 0
        
    def update_fired(self):
        if self.fired != []:
            yup = 0
            for i in range(len(self.fired)):
                self.fired[i][0] += self.fired[i][2]
                self.fired[i][1] += self.fired[i][3]
                if self.fired[i][0] < 0 or self.fired[i][1] < 0 or self.fired[i][0] > WIDTH or self.fired[i][1] > HEIGHT:   yup = 1
                pygame.draw.circle(screen, (160, 120, 180), (self.fired[i][0], self.fired[i][1]), 2)
            if yup: self.fired = [x for x in self.fired if x[0] < WIDTH and x[1] < HEIGHT and x[0] > 0 and x[1] > 0]


    def fire(self):
        self.fired.append([self.pos_u[0], self.pos_u[1], 
        ((self.pos_u[0] - self.pos_initial[0]) / SPEED) + self.vel[0], ((self.pos_u[1] - self.pos_initial[1]) / SPEED) + self.vel[1]])

    def rotate_friction(self):
        if math.fabs(self.move_angle) <= 0.001745:   self.move_angle = 0
        elif math.fabs(self.move_angle) <= 0.1:
            self.angle += self.move_angle
        elif self.move_angle < 0: 
            self.move_angle = -0.1
            self.angle += self.move_angle
        elif self.move_angle > 0: 
            self.move_angle = 0.1
            self.angle += self.move_angle

    def move(self, keys):
        self.get_keys(keys)
        self.rotate_friction()
        self.pos_initial[0] += self.vel[0] * 0.95
        self.pos_initial[1] += self.vel[1] * 0.95
        self.wall()
        self.calculate_positions()
        self.update_fired()
        self.draw()


class Asteroids:
    def __init__(self):
        self.asteroids = []
        self.where = 0
        self.new()
    
    def render(self):
        for i in self.asteroids:
            pygame.draw.circle(screen, (180, 180, 180), i['pos'], i['width'], 2)
    
    def new(self):
        self.where = random.randint(0, 3)
        if not self.where:  # left side
            self.asteroids.append({'pos': [0, random.randint(0, HEIGHT)], 'vector': 
            [random.randint(8, 20) / 10, random.randint(-10, 10) / 10], 'width': random.choice([15, 25, 40])})
        elif self.where == 1:   # top side
            self.asteroids.append({'pos': [random.randint(0, WIDTH), 0], 'vector': 
            [random.randint(-10, 10) / 10, random.randint(8, 20) / 10], 'width': random.choice([15, 25, 40])})
        elif self.where == 2:   # right side
            self.asteroids.append({'pos': [WIDTH, random.randint(0, HEIGHT)], 'vector': 
            [-random.randint(8, 20) / 10, random.randint(-10, 10) / 10], 'width': random.choice([15, 25, 40])})
        elif self.where == 3:   # bottom side
            self.asteroids.append({'pos': [random.randint(0, WIDTH), HEIGHT], 'vector': 
            [random.randint(-10, 10) / 10, -random.randint(8, 20) / 10], 'width': random.choice([15, 25, 40])})

    def update_positions(self):
        if self.asteroids != {}:
            yup = 0
            for i in range(len(self.asteroids)):
                self.asteroids[i]['pos'][0] += self.asteroids[i]['vector'][0]
                self.asteroids[i]['pos'][1] += self.asteroids[i]['vector'][1]
                if self.asteroids[i]['pos'][0] < -self.asteroids[i]['width'] or self.asteroids[i]['pos'][0] > WIDTH + self.asteroids[i][
                    'width'] or self.asteroids[i]['pos'][1] < -self.asteroids[i][
                        'width'] or self.asteroids[i]['pos'][1] > HEIGHT + self.asteroids[i]['width']:
                    yup = 1
            if yup:
                for x in self.asteroids:
                    if x['pos'][0] < 0 or x['pos'][1] < 0 or x['pos'][0] > WIDTH or x['pos'][1] > HEIGHT:
                        self.asteroids.remove(x)
                        
    def update(self): 
        self.update_positions()
        self.render()

class Collisions:
    def __init__(self):
        self.to_death_enemy = []
        self.to_death_bullet = []
        self.tolerance = 2

    def new_v(self):
        return [random.randint(-20, 20) / 8, random.randint(-20, 20) / 8]

    def remove(self, enemies=[], bullets=[]):
        prev = 0
        if enemies == []:   return  False
        for i in self.to_death_enemy:
            if i != prev:
                enemies.pop(enemies.index(i))
            else:   
                self.to_death_enemy.pop(self.to_death_enemy.index(prev))
            prev = i
        self.to_death_enemy = []

        if bullets == []:   return  False
        for i in self.to_death_bullet:
            if i != prev:
                bullets.pop(bullets.index(i))
            else:
                self.to_death_bullet.pop(self.to_death_bullet.index(prev))
            prev = i
        self.to_death_bullet = []
    
    def collide_asteroid(self, bullets, enemies):
        for bullet in bullets:
            for enemy in enemies:
                if bullet[0] - enemy['pos'][0] < enemy['width'] and bullet[0] - enemy['pos'][0] > -enemy['width']:
                    if bullet[1] - enemy['pos'][1] < enemy['width'] and bullet[1] - enemy['pos'][1] > -enemy['width']:
                        if enemy['width'] == 15:  
                            self.to_death_bullet.append(bullet)
                            self.to_death_enemy.append(enemy)  
                        elif enemy['width'] == 25:  
                            enemies.append({'pos': [enemy['pos'][0] - 10, enemy['pos'][1]], 'vector': self.new_v(),'width': 15})
                            enemies.append({'pos': [enemy['pos'][0] + 10, enemy['pos'][1]], 'vector': self.new_v(),'width': 15})
                            self.to_death_bullet.append(bullet)
                            self.to_death_enemy.append(enemy) 
                        elif enemy['width'] == 40:
                            enemies.append({'pos': [enemy['pos'][0] - 10, enemy['pos'][1]], 'vector': self.new_v(),'width': 25})
                            enemies.append({'pos': [enemy['pos'][0] + 10, enemy['pos'][1]], 'vector': self.new_v(),'width': 25})
                            self.to_death_bullet.append(bullet)
                            self.to_death_enemy.append(enemy) 
    

    def collide_player(self, enemies, ship):
        for i in enemies:
            if math.hypot(math.fabs(i['pos'][0] - ship.pos_l[0]), i['pos'][1] - ship.pos_l[1]) <= i['width'] - self.tolerance or math.hypot(
                math.fabs(i['pos'][0] - ship.pos_r[0]), math.fabs(i['pos'][1] - ship.pos_r[1])) <= i['width'] - self.tolerance or math.hypot(
                    math.fabs(i['pos'][0] - ship.pos_u[0]), math.fabs(i['pos'][1] - ship.pos_u[1])) <= i['width'] - self.tolerance:
                return True
        return False


    def update(self, bullets, enemies, ship):
        self.collide_asteroid(bullets, enemies)
        self.remove(enemies, bullets)
        if self.collide_player(enemies, ship): return True

class Main:
    def __init__(self):
        self.score = 0
        self.menu = Menu(screen, self)
        self.menu.run()
    
    def rate(self, count, enemy):
        if not count % 90 and self.score <= 20:  
            enemy.new()
            self.score += 1
        elif not count % 60 and self.score <= 40 and self.score > 20:
            enemy.new()
            self.score += 1
        elif not count % 40 and self.score > 40 and self.score <= 80:
            enemy.new()
            self.score += 1
        elif not count % 20 and self.score > 80:
            enemy.new()
            self.score += 1

    def main(self):
        ship = Ship([WIDTH // 2, HEIGHT // 2])
        enemy = Asteroids()
        collide = Collisions()
        clock = pygame.time.Clock()
        fps = 60
        count = 0
        while True:
            clock.tick(fps)
            screen.fill((0, 0, 0))
            count += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ship.fire()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ship.fire()

            ship.move(pygame.key.get_pressed())  
            enemy.update()
            self.rate(count, enemy)
            
            if collide.update(ship.fired, enemy.asteroids, ship):   
                del ship
                del enemy
                del collide
                gc.collect()
                self.menu.game_over(self.score)
            pygame.display.update()
    

if __name__ == "__main__":
    main = Main()