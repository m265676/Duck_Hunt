import pygame
import os


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, target_image):
        super().__init__()

        # Use the provided target image
        self.image = target_image
        self.rect = self.image.get_rect()

    def update(self, mouse_x, mouse_y):
        # Update the position of the crosshair based on the mouse position
        self.rect.center = (mouse_x, mouse_y)

