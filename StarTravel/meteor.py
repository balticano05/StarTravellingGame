import pygame
import random

class Meteor(pygame.sprite.Sprite):

    def __init__(self, width, height, image_paths):
        super().__init__()
        self.width = width
        self.height = height
        self.image_paths = image_paths
        self.load_random_image()

        self.size = random.randint(30, 100)
        self.angle = 0
        self.rotate_speed = random.randint(-5, 5)
        self.speed = random.randint(1, 5)

        self.base_image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(
            center=(random.randint(50, width - 50), random.randint(-200, -50))
        )

    def load_random_image(self):
        self.original_image = pygame.image.load(random.choice(self.image_paths)).convert_alpha()

    def update(self):
        self.angle = (self.angle + self.rotate_speed) % 360
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.y += self.speed

        if self.rect.top > self.height:
            self.respawn()

    def respawn(self):
        self.load_random_image()
        self.size = random.randint(30, 100)
        self.base_image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect(
            center=(random.randint(50, self.width - 50), random.randint(-200, -50))
        )
        self.speed = random.randint(1, 5)
        self.rotate_speed = random.randint(-5, 5)