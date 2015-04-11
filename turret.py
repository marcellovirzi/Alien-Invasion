__author__ = 'marcellovirzi'

import pygame


class Turret(pygame.sprite.Sprite):
    def __init__(self, LARGHEZZAFINESTRA, ALTEZZAFINESTRA):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/turret.png")
        self.rect = self.image.get_rect()
        self.rect.x = (LARGHEZZAFINESTRA - self.rect.width)/2
        self.rect.y = ALTEZZAFINESTRA - self.rect.height

    def update_position(self, direction, LARGHEZZAFINESTRA, level):
        if direction == "left" and self.rect.x > 10:
            self.rect.x -= 15 + level
        elif direction == "right" and self.rect.x < (LARGHEZZAFINESTRA - 10):
            self.rect.x += 15 + level

    def get_gun_position(self):
        position = {}
        position["x"] = self.rect.x + (self.rect.width/2)
        position["y"] = self.rect.y - (self.rect.height/2)
        return position