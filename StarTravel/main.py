import pygame
from game import Game
import sys
from starship import StarShip
from game_functions import handle_events, update_game, draw_game, create_meteors

pygame.init()

WIDTH, HEIGHT = 700, 1100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Звездный сомолет")

background = pygame.image.load("textures/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

def main():
    # Группы спрайтов
    game = Game()
    game.run()

    all_sprites = pygame.sprite.Group()
    meteors = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Создание корабля
    starship = StarShip(WIDTH, HEIGHT, "textures/starship.png")
    all_sprites.add(starship)

    meteor_images = [
        "textures/meteors/meteor_1.png",
        "textures/meteors/meteor_2.png",
        "textures/meteors/meteor_3.png"
    ]

    create_meteors(8, all_sprites, meteors, WIDTH, HEIGHT, meteor_images)

    # Основной игровой цикл
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        running = handle_events(starship, all_sprites, bullets)
        running = update_game(starship, all_sprites, meteors, bullets, WIDTH, HEIGHT)
        draw_game(screen, all_sprites, background)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()