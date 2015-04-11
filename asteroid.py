__author__ = 'marcellovirzi'

import pygame
import random


class Asteroid(pygame.sprite.Sprite):

    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except pygame.error as message:
            print("Cannot load image: " + image_name)
            raise SystemExit(message)
        return image.convert_alpha()

    def load_sound(self, sound_name):
        try:
            sound = pygame.mixer.Sound(sound_name)
        except pygame.error as message:
            print("Cannot load sound: " + sound_name)
            raise SystemExit(message)
        return sound

    def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

    def __init__(self, WINDOWWIDTH, ang, ang_vel):
        pygame.sprite.Sprite.__init__(self)
        self._species = random.choice(["asteroid1", "asteroid2"])
        self.image = self.load_image("images/" + self._species + ".png")
        self.image = pygame.transform.rotate(self.image, random.randint(-35, 35))
        self.rect = self.image.get_rect()
        self.rect.y = 0 - self.rect.height
        self.rect.x = (random.uniform(self.rect.width/2, (WINDOWWIDTH - self.rect.width)))
        self.angle = ang
        self.angle_vel = ang_vel
        sound = self.load_sound("spinning.wav")
        sound.set_volume(.1)
        sound.play()

    def update_position(self, level, WINDOWHEIGHT, game):
        # update angle

        # update position in canvas
        if self.rect.y <= (WINDOWHEIGHT):
            self.rect.y += 2 + level
            #self.rect = self.image.get_rect()
            #self.image = pygame.transform.rotate(self.image, 2)

        else:
            game.update_score(-80)
            self.kill()

    def shot(self,game):
        game.update_score(30)
        self.kill()