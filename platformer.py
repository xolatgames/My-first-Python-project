#Music by timbeek.com
#Sounds: https://jdwasabi.itch.io/8-bit-16-bit-sound-effects-pack

import pygame

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((832,600))
pygame.display.set_caption("Platformer")

pygame.mixer.music.load("sounds/Music.ogg")
pygame.mixer.music.play(-1)

jump_sound = pygame.mixer.Sound("sounds/jump.wav")
coin_sound = pygame.mixer.Sound("sounds/coin.wav")
enemy_sound = pygame.mixer.Sound("sounds/enemy.wav")

bg = [
    pygame.image.load("images/bg.png"),
    pygame.image.load("images/bg2.png")
]
bg_frame = 0

font = pygame.font.SysFont(None, 32)
lose_text = font.render("You Lose! Press Enter to restart!", True, "Dark Blue")
win_text = font.render("You Win!", True, "Dark Blue")
tip_text = font.render("Collect all coins!", True, "Dark Blue")

players = []
grounds = []
enemies = []
finishes = []
coins = []

lose = [False]
finish = [False]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/player right.png")
        self.rect = pygame.Rect(x + 4, y + 4, 28, 32)
        self.rect.x = x
        self.rect.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.onGround = False
        self.jump_speed = 9
        self.max_vspeed = 8
    
    def update(self):
        if not self.onGround:
            self.vspeed += 0.5
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.vspeed -= self.jump_speed
                jump_sound .play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.hspeed = -4
            self.image = pygame.image.load("images/player left.png")
        if keys[pygame.K_RIGHT]:
            self.hspeed = 4
            self.image = pygame.image.load("images/player right.png")

        self.rect.x += self.hspeed

        self.collisionPlatform(self.hspeed, 0)

        self.hspeed = 0

        self.rect.y += self.vspeed
        
        self.onGround = False

        self.collisionPlatform(0, self.vspeed)

        if self.vspeed >= self.max_vspeed:
            self.vspeed = self.max_vspeed
        
        self.collisionEnemy()

        self.collisionFinish()

        self.collisionCoin()
    
    def collisionPlatform(self, hspeed, vspeed):
        for gr in grounds:
            if pygame.sprite.collide_rect(self, gr):
                if hspeed < 0:
                    self.rect.left = gr.rect.right
                if hspeed > 0:
                    self.rect.right = gr.rect.left
                if vspeed > 0:
                    self.rect.bottom = gr.rect.top
                    self.onGround = True
                    self.vspeed = 0
                if vspeed < 0:
                    self.rect.top = gr.rect.bottom
    
    def collisionEnemy(self):
        for en in enemies:
            if pygame.sprite.collide_rect(self, en):
                Clear()

                lose.clear()

                enemy_sound.play()
    
    def collisionFinish(self):
        for fin in finishes:
            if pygame.sprite.collide_rect(self, fin):
                if len(coins) == 0:
                    Clear()

                    finish.clear()
    
    def collisionCoin(self):
        for cn in coins:
            if pygame.sprite.collide_rect(self, cn):
                coin_sound.play()
                coins.remove(cn)
                sprites.remove(cn)

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/ground.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, jump_speed, gravity):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy.png")
        self.rect = pygame.Rect(x + 2, y + 2, 30, 30)
        self.rect.x = x
        self.rect.y = y
        self.jump_speed = jump_speed
        self.gravity = gravity
        self.vspeed = 0

    def update(self):
        self.vspeed += self.gravity
        
        self.rect.y += self.vspeed

        for gr in grounds:
            if pygame.sprite.collide_rect(self, gr):
                self.vspeed = -self.jump_speed


class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/finish.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/coin.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

sprites = pygame.sprite.Group()

def Map():
    level = []

    x = y = 0

    file = open("level.txt", "r")
    map = file.readlines()

    for line in map:
        level.append(line[:-1])
    
    for row in level:
        for i in row:
            if i == "P":
                player = Player(x, y)
                players.append(player)
                sprites.add(player)
            elif i == "G":
                ground = Ground(x, y)
                grounds.append(ground)
                sprites.add(ground)
            elif i == "E":
                enemy = Enemy(x, y, 0, 0)
                enemies.append(enemy)
                sprites.add(enemy)
            elif i == "J":
                enemy = Enemy(x, y, 7, 0.5)
                enemies.append(enemy)
                sprites.add(enemy)
            elif i == "F":
                finish = Finish(x, y)
                finishes.append(finish)
                sprites.add(finish)
            elif i == "M":
                coin = Coin(x, y)
                coins.append(coin)
                sprites.add(coin)
            x += 32
        x = 0
        y += 32

def Clear():
    players.clear()
    enemies.clear()
    grounds.clear()
    finishes.clear()
    coins.clear()
    sprites.empty()

Map()

running = True
while running:
    screen.blit(bg[0], (0, 0))
    if bg_frame > 15:
        screen.blit(bg[1], (0, 0))
    bg_frame += 1

    if bg_frame > 30:
        bg_frame = 0

    for pl in players:
        pl.update()

    for en in enemies:
        en.update()

    sprites.draw(screen)

    if lose == []:
        screen.blit(lose_text, (20, 20))
    
    if finish == []:
        screen.blit(win_text, (20, 20))

    if len(finish) > 0 and len(lose) > 0:
        screen.blit(tip_text, (20, 20))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                Clear()

                lose.append(False)

                finish.append(False)

                Map()
        
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(30)
