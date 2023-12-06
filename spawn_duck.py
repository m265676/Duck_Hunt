from constants import *
import pygame
from duck import green_ducks, blue_ducks, red_ducks, Duck
import math


def spawn_duck(duck_group, image_path, speed, last_spawn_time, spawn_delay, y_coordinate, amp):
    now = pygame.time.get_ticks()
    if len(duck_group) < DUCK_NUM:
        if now - last_spawn_time >= spawn_delay * 250:
            last_spawn_time = now
            duck_group.add(Duck(SCREEN_WIDTH, y_coordinate, image_path, speed, amp))
    return last_spawn_time