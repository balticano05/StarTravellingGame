import pygame
from meteor import Meteor

def handle_events(starship, all_sprites, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                starship.shoot(all_sprites, bullets)
    return True

def update_game(starship, all_sprites, meteors, bullets, width, height, game):
    all_sprites.update()

    # Проверка столкновений пуль с метеоритами
    hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
    for hit in hits:
        game.score += 10  # Увеличиваем счет
        meteor = Meteor(width, height, [
            "textures/meteors/meteor_1.png",
            "textures/meteors/meteor_2.png",
            "textures/meteors/meteor_3.png"
        ])
        all_sprites.add(meteor)
        meteors.add(meteor)

    # Проверка столкновения корабля с метеоритами
    if pygame.sprite.spritecollide(starship, meteors, False):
        return False
    return True


def draw_game(screen, all_sprites, background, score):
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    # Отображение счета
    font = pygame.font.Font(None, 36)
    text = font.render(f"Счет: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()

def create_meteors(num_meteors, all_sprites, meteors, width, height, image_paths):
    for _ in range(num_meteors):
        meteor = Meteor(width, height, image_paths)
        all_sprites.add(meteor)
        meteors.add(meteor)