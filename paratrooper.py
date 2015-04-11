__author__ = 'marcellovirzi'

import pygame
import random


class Paratrooper(pygame.sprite.Sprite):

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

    def __init__(self, WINDOWWIDTH):
        pygame.sprite.Sprite.__init__(self)
        self._species = random.choice(["parachute"])
        self.image = self.load_image("images/" + self._species + ".png")
        self.image = pygame.transform.rotate(self.image, random.randint(-35, 35))
        self.rect = self.image.get_rect()
        self.rect.y = 0 - self.rect.height
        self.rect.x = (random.uniform(self.rect.width/2, (WINDOWWIDTH - self.rect.width)))
        #sound = self.load_sound("spinning.wav")
        #sound.play()

    def update_position(self, level, WINDOWHEIGHT, game):
        # update angle

        # update position in canvas
        if self.rect.y <= (WINDOWHEIGHT):
            self.rect.y += 2 + level
            # game.update_score(100)
        else:
            game.update_score(80)
            game.update_para_saved()
            self.kill()

    def shot(self,game):
        game.update_score(-200)
        self.kill()