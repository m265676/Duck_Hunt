import pygame
import math
from constants import *


class Duck(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, speed, amp):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (40, 40))
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.rect.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.rect.center = (x, y)
        self.speed = speed
        self.height = y
        self.angle = 0
        self.amp = amp

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()

        self.angle += math.pi / 60
        self.rect.y = self.height + TILE_SIZE * self.amp * math.sin(self.angle)

    def chg_speed(self):
        self.speed += 10


# Make each sprite group from the class Duck
green_ducks = pygame.sprite.Group()
blue_ducks = pygame.sprite.Group()
red_ducks = pygame.sprite.Group()
