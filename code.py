#!/usr/bin/env python3

# Created by: Felipe Garcia Affonso
# Created on: April 2021
# This program setts a background to the game

import ugame
import stage
import constants
import time
import random
import board
import neopixel


def menu_scene():
    # this function is the game menu_scene

    # images bank for circuitpython
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # add text
    text1 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE)
    text1.move(20, 10)
    text1.text("MT Game Studios")

    text2 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE)
    text2.move(40, 110)
    text2.text("Press Start")
    text = [text1, text2]

    # render game visuals
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X,
                            constants.SCREEN_GRID_Y)

    game = stage.Stage(ugame.display, constants.FPS)

    game.layers = text + [background]

    game.render_block()

    # repeat forever loop
    while True:
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_X != 0:
            pass
        if keys & ugame.K_O:
            pass
            # print("B")
        if keys & ugame.K_START:
            game_scene()
        if keys & ugame.K_SELECT:
            pass
            # print(ship.x)
        if keys & ugame.K_RIGHT:
            pass
        if keys & ugame.K_LEFT:
            pass
        if keys & ugame.K_UP:
            pass
            # if ship.y > 0:
            #    ship.move(ship.x, ship.y -1)
        if keys & ugame.K_DOWN:
            pass
            # if ship.y < constants.SCREEN_Y - constants.SPRITE_SIZE:
            #     ship.move(ship.x, ship.y + 1)

        game.tick()


def splash_scene():
    # this function is the game splash_scene

    # get sound ready
    coin_sound = open("coin.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)

    # images bank for circuitpython
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # render game visuals
    background = stage.Grid(image_bank_mt_background, constants.SCREEN_GRID_X,
                            constants.SCREEN_GRID_Y)

    # used this program to split the image into tile:
    #   https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png
    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    game = stage.Stage(ugame.display, constants.FPS)

    game.layers = [background]

    game.render_block()

    while True:
        # wait for 2 seconds
        time.sleep(2)
        menu_scene()


def game_scene():
    # this function is the main game game_scene

    def show_alien():
        # this function puts the alien in the screen
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x < 0:
                aliens[alien_number].move(random.randint(0 + constants.SPRITE_SIZE,
                    constants.SCREEN_X - constants.SPRITE_SIZE),
                    constants.OFF_TOP_SCREEN)
                break

    # images bank for circuitpython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # buttons that you want to keep state information on
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # render sound
    pew_sound = open("pew.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # render game visuals
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X,
                            constants.SCREEN_GRID_Y)
    for x_location in range(constants.SCREEN_X):
        for y_location in range(constants.SCREEN_Y):
            title_picked = random.randint(1, 3)
            background.tile(x_location, y_location, title_picked)

    ship = stage.Sprite(image_bank_sprites, 4, 75,
                        constants.SCREEN_Y - constants.SPRITE_SIZE * 2)

    aliens = []

    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        a_single_alien = stage.Sprite(image_bank_sprites, 9,
                        constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        aliens.append(a_single_alien)

    show_alien()

    # list of lasers
    lasers = []
    for laser_number in range(0, constants.TOTAL_NUMBER_OF_LASERS):
        a_single_laser = stage.Sprite(image_bank_sprites, 10,
                        constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        lasers.append(a_single_laser)

    game = stage.Stage(ugame.display, constants.FPS)

    game.layers = lasers + [ship] + aliens + [background]

    game.render_block()

    # render led
    neopixels = neopixel.NeoPixel(board.D8, constants.NEOPIXEL_COUNT, brightness=constants.BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB)

    # repeat forever loop
    while True:
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_X != 0:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]
        if keys & ugame.K_O:
            pass
            # print("B")
        if keys & ugame.K_START:
            pass
            # print(ship.y)
        if keys & ugame.K_SELECT:
            menu_scene()
        if keys & ugame.K_RIGHT:
            if ship.x < constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(ship.x + 1, ship.y)
            else:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
        if keys & ugame.K_LEFT:
            if ship.x > 0:
                ship.move(ship.x - 1, ship.y)
            else:
                ship.move(0, ship.y)
        if keys & ugame.K_UP:
            pass
            # if ship.y > 0:
            #    ship.move(ship.x, ship.y -1)
        if keys & ugame.K_DOWN:
            pass
            # if ship.y < constants.SCREEN_Y - constants.SPRITE_SIZE:
            #     ship.move(ship.x, ship.y + 1)

        # game logic
        if a_button == constants.button_state["button_just_pressed"]:
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x < 0:
                    lasers[laser_number].move(ship.x, ship.y)
                    sound.play(pew_sound)
                    break

        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                lasers[laser_number].move(lasers[laser_number].x,
                        lasers[laser_number].y - constants.LASER_SPEED)
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN:
                    lasers[laser_number].move(constants.OFF_SCREEN_X,
                            constants.OFF_SCREEN_Y)

        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                neopixels.fill(constants.RED)
            elif lasers[laser_number].x < 0:
                neopixels.fill(constants.GREEN)
            else:
                neopixels.fill(constants.YELLOW)

        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
                aliens[alien_number].move(aliens[alien_number].x,
                        lasers[laser_number].y + constants.SPRITE_MOVEMENT_SPEED)
                if aliens[alien_number].y > constants.SCREEN_Y:
                    aliens[alien_number].move(constants.OFF_SCREEN_X,
                            constants.OFF_SCREEN_Y)
                    show_alien()


        neopixels.show()
        neopixels.brightness = constants.BRIGHTNESS

        game.render_sprites(lasers + [ship] + aliens)
        game.tick()


if __name__ == "__main__":
    splash_scene()
