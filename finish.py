import pygame

class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/finish.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
