__author__ = 'marcellovirzi'

import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.x = position["x"]
        self.rect.y = position["y"]

    def update_position(self):

        if self.rect.y >= -self.rect.height:
            self.rect.y -= 5
        else:
            self.kill()