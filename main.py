__author__ = 'marcellovirzi'

import math
import random
import pygame
import sys
import pickle
import os

from game import *
from turret import *
from bullet import *
from asteroid import *
from paratrooper import *
from ufo import *

## TOP LEVEL CONSTANTS
FPS = 30
WINDOWWIDTH = 480
WINDOWHEIGHT = 640
GAMETITLE = "!! Alien Invasion !!"
WHITE = [255, 255, 255]; RED = [255, 0, 0]; GREEN = [0, 255, 0]; BLUE = [0, 0, 255]; BLACK = [0, 0, 0]
NUMBER_OF_LEVELS = 5

def main():

    def load_sound(name):
        class NoneSound:
            def play(self):
               pass
        if not pygame.mixer:
            return NoneSound()
        #fullname = os.path.join("/sounds" ,name)
        try:
            sound = pygame.mixer.Sound(name)
        except pygame.error as message:
            print('Cannot load sound:', name)
            raise SystemExit(message)
        return sound

    def check_collision(typology_live_sprites):
        for sprite in typology_live_sprites:  # go through all collisions and check
            sprite.shot(game)

    # booting game's class
    game = Game()

    # INITIAL SETUP
    pygame.init()
    pygame.key.set_repeat(1, 75)
    pygame.mouse.set_visible(False)
    displayFont = pygame.font.Font("256BYTES.TTF", 28)
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])
    pygame.display.set_caption(GAMETITLE)

    # sound
    explosion = load_sound("explosion.wav")
    explosion.set_volume(.1)
    screaming = load_sound("Screaming-SoundBible.wav")
    screaming.set_volume(.1)
    tank_firing = load_sound("Tank_Firing-SoundBible.wav")
    tank_firing.set_volume(.1)
    tank = load_sound("Tank-SoundBible.wav")
    tank.set_volume(.1)
    ufo_landing = load_sound("UFO_Landing-SoundBible.wav")
    ufo_landing.set_volume(.1)
    pain = load_sound("Pain-SoundBible.wav")
    pain.set_volume(.1)
    laser = load_sound("Laser-SoundBible.wav")
    laser.set_volume(.1)
    siren = load_sound("Tornado_Siren_II-Delilah-747233690.wav")
    siren.set_volume(.1)
    pygame.mixer.music.load("AstroTurf.ogg")
    pygame.mixer.music.set_volume(.1)
    pygame.mixer.music.play(-1)

    # SPLASH SCREEN -----------------------------------------------------------------------
    splash = pygame.image.load("images/splash.png")
    surface.blit(splash, (0, 0))
    pygame.display.update()
    game_over = False
    start_game = False

    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    resume = False
                    start_game = True
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    resume = True
                    start_game = True

    if resume:  # if they want to pick up a saved game
        if os.path.exists("savedata.dat"):
            game.load_game()
    # --------------------------------------------------------------------------------------

    # MAIN GAME LOOP -----------------------------------------------------------------------    
    while game.get_level() <= NUMBER_OF_LEVELS and not game_over:

        # SHOW LEVEL NUMBER
        surface.fill(BLACK)
        levelText = displayFont.render('Level: ' + str(game.get_level()), True, GREEN)
        surface.blit(levelText, (150, 300))
        pygame.display.update()
        pygame.time.wait(1500)

        # SET UP VARIABLES FOR LEVEL
        game.save_game()
        game._aliens_killed = 0
        game._para_saved = 0

        bullet_sprites = pygame.sprite.Group()
        other_sprites = pygame.sprite.Group()
        live_asteroid_sprites = pygame.sprite.Group()
        live_para_sprites = pygame.sprite.Group()
        live_ufo_sprites = pygame.sprite.Group()

        # load turret
        turret = Turret(WINDOWWIDTH, WINDOWHEIGHT)
        other_sprites.add(turret)
        tank.play(-1)

        ufo_ticktock = 1
        asteroids_ticktock = 1
        para_ticktock = 1
        level_over = False

        if game.get_level() == 4:
            siren.play()

        # PLAY INDIVIDUAL LEVEL
        while not level_over and not game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                    elif event.key == pygame.K_LEFT:
                        turret.update_position("left", WINDOWWIDTH, game.get_level())
                    elif event.key == pygame.K_RIGHT:
                        turret.update_position("right", WINDOWWIDTH, game.get_level())
                    elif event.key == pygame.K_SPACE:
                        bullet = Bullet(turret.get_gun_position())
                        bullet_sprites.add(bullet)
                        tank_firing.play()

            if ufo_ticktock >= 140:
                ufo_ticktock = 0

                if len(live_ufo_sprites) < 2:
                    live_ufo_sprites.add(Ufo(WINDOWWIDTH))


            if asteroids_ticktock >= 120:
                asteroids_ticktock = 0

                if len(live_asteroid_sprites) < 10:
                    live_asteroid_sprites.add(Asteroid(WINDOWWIDTH, 2, random.random() * .2 - .1))

            if para_ticktock >= 250:
                para_ticktock = 0

                if len(live_para_sprites) < 1:
                    live_para_sprites.add(Paratrooper(WINDOWWIDTH))

            # update bullet's position
            for sprite in bullet_sprites:
                sprite.update_position()

            # check collisions ---------------------------------------------------------------------------------

            # typology_sprite_collision
            aster_collisions = pygame.sprite.groupcollide(live_asteroid_sprites, bullet_sprites, False, True)
            para_collisions = pygame.sprite.groupcollide(live_para_sprites, bullet_sprites, False, True)
            ufo_collisions = pygame.sprite.groupcollide(live_ufo_sprites, bullet_sprites, False, True)

            if aster_collisions:
                check_collision(aster_collisions)
                explosion.play()

            if para_collisions:  # if there are any
                check_collision(para_collisions)
                pain.play()
                explosion.play()

            if ufo_collisions:  # if there are any
                check_collision(ufo_collisions)
                explosion.play()
            # --------------------------------------------------------------------------------------------------

            background = pygame.image.load("images/gameBoard.png")
            surface.blit(background, (0, 0))

            bullet_sprites.draw(surface)
            other_sprites.draw(surface)

            for sprite in live_asteroid_sprites:
                sprite.update_position(game.get_level(), WINDOWHEIGHT, game)
                live_asteroid_sprites.draw(surface)

            for sprite in live_ufo_sprites:
                sprite.update_position(game.get_level(), WINDOWHEIGHT, game)
                live_ufo_sprites.draw(surface)

            for sprite in live_para_sprites:
                sprite.update_position(game.get_level(), WINDOWHEIGHT, game)
                live_para_sprites.draw(surface)


            scoreText = displayFont.render('Score: ' + str(game.get_score()), True, GREEN)
            levelText = displayFont.render('Level: ' + str(game.get_level()), True, WHITE)
            aliensText = displayFont.render('Aliens killed: ' + str(game.get_aliens_killed()), True, RED)
            paraText = displayFont.render('Paratroopers saved: ' + str(game.get_para_saved()), True, WHITE)

            surface.blit(scoreText, (10, 10))
            surface.blit(levelText, (10, 50))
            surface.blit(aliensText, (10, 90))
            surface.blit(paraText, (10, 130))

            pygame.display.update()
            ufo_ticktock += game.get_level()
            para_ticktock += game.get_level()
            asteroids_ticktock += game.get_level()

            if game.get_aliens_killed() >= 10:
                game.update_level(1)
                level_over = True
            clock.tick(FPS)

    # handle end of game
    surface.fill(BLACK)
    scoreText = displayFont.render('Game over. Score: ' + str(game.get_score()), True, GREEN)
    surface.blit(scoreText, (10, 200))
    pygame.display.update()

    input("press any key")

if __name__ == '__main__':
    main()