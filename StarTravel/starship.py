import pygame
import logging
from bullet import Bullet

class StarShip(pygame.sprite.Sprite):
    def __init__(self, width, height, image_path):
        super().__init__()
        self.logger = logging.getLogger('SpaceGame.StarShip')
        try:
            self.original_image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.original_image, (90, 90))
            self.rect = self.image.get_rect()
            self.rect.center = (width // 2, height - 50)
            self.speed = 5
            self.width = width
            self.height = height
            self.logger.debug("Корабль создан")
        except Exception as e:
            self.logger.error(f"Ошибка создания корабля: {str(e)}")
            raise

    def update(self):
        try:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < self.width:
                self.rect.x += self.speed
        except Exception as e:
            self.logger.error(f"Ошибка обновления корабля: {str(e)}")

    def shoot(self, all_sprites, bullets):
        try:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.logger.info("Произведен выстрел")
        except Exception as e:
            self.logger.error(f"Ошибка при выстреле: {str(e)}")