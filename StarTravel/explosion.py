import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.radius = 5
        self.max_radius = 40
        self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)
        self.color = (255, 100, 0, 200)

        import random
        self.sound = random.choice([
            pygame.mixer.Sound("sound/laser.mp3"),
            pygame.mixer.Sound("sound/meteor_explosion.mp3"),
            pygame.mixer.Sound("sound/ship_explosion.mp3")
        ]) if hasattr(pygame.mixer, 'Sound') else None

        if self.sound:
            self.sound.set_volume(0.4)
            self.sound.play()

    def update(self):
        self.radius += 3
        if self.radius >= self.max_radius:
            self.kill()
        else:
            self.image.fill((0, 0, 0, 0))
            pygame.draw.circle(
                self.image,
                self.color,
                (self.max_radius, self.max_radius),
                self.radius
            )