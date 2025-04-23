# game.py
from pathlib import Path
import pygame
import sys
from starship import StarShip
from meteor import Meteor
from game_functions import create_meteors
from explosion import Explosion

class Game:

    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 700, 1100
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Звездный сомолет")

        self.background = pygame.transform.scale(
            pygame.image.load("textures/background.png"),
            (self.WIDTH, self.HEIGHT)
        )

        self.all_sprites = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.starship = StarShip(self.WIDTH, self.HEIGHT, "textures/starship.png")
        self.all_sprites.add(self.starship)

        self.meteor_images = [
            "textures/meteors/meteor_1.png",
            "textures/meteors/meteor_2.png",
            "textures/meteors/meteor_3.png"
        ]
        create_meteors(8, self.all_sprites, self.meteors,
                      self.WIDTH, self.HEIGHT, self.meteor_images)

        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.high_score = 0  # Инициализируем рекорд нулем
        self.last_score_update = pygame.time.get_ticks()

        self.menu_active = True
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.buttons = [
            {"text": "Новая игра", "rect": pygame.Rect(0, 0, 300, 50), "action": "start"},
            {"text": "Выйти", "rect": pygame.Rect(0, 0, 300, 50), "action": "exit"}
        ]

        self.setup_menu()

        self.init_sounds()

        self.highscore_path = Path("highscore.txt")
        self.high_score = self.load_high_score()

    def init_sounds(self):
        try:
            pygame.mixer.init()
            self.laser_sound = pygame.mixer.Sound("sound/laser.mp3")
            self.meteor_explosion = pygame.mixer.Sound("sound/meteor_explosion.mp3")
            self.ship_explosion = pygame.mixer.Sound("sound/ship_explosion.mp3")

            self.laser_sound.set_volume(0.3)
            self.meteor_explosion.set_volume(0.5)
            self.ship_explosion.set_volume(0.7)
        except Exception as e:
            print(f"Ошибка загрузки звуков: {e}")
            self.sound_enabled = False
        else:
            self.sound_enabled = True

    def setup_menu(self):

        y = self.HEIGHT // 2 - 100
        for btn in self.buttons:
            btn["rect"].center = (self.WIDTH // 2, y)
            y += 100

    def load_high_score(self):

        try:
            with open(self.highscore_path, "r") as f:
                content = f.read().strip()
                return int(content) if content else 0
        except (FileNotFoundError, ValueError, PermissionError) as e:
            print(f"Error loading high score: {e}")
            return 0

    def save_high_score(self):

        try:
            with open(self.highscore_path, "w") as f:  # Исправлено здесь
                f.write(str(self.high_score))
            print(f"High score saved to: {self.highscore_path}")
        except Exception as e:
            print(f"Error saving high score: {e}")

    def format_score(self, score):

        if score >= 10000:
            return "{:.1e}".format(score)
        return f"{score}"

    def check_and_save_highscore(self):

        if self.score > self.high_score:
            self.high_score = self.score
        self.save_high_score()

    def reset_game(self):

        self.all_sprites.empty()
        self.meteors.empty()
        self.bullets.empty()

        self.starship = StarShip(self.WIDTH, self.HEIGHT, "textures/starship.png")
        self.all_sprites.add(self.starship)
        create_meteors(8, self.all_sprites, self.meteors,
                       self.WIDTH, self.HEIGHT, self.meteor_images)

        self.score = 0
        self.menu_active = False
        self.last_score_update = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.menu_active and event.type == pygame.MOUSEBUTTONDOWN:
                action = self.handle_menu_click(event)
                if action == "start":
                    self.reset_game()
                elif action == "exit":
                    return False
            elif not self.menu_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.starship.shoot(self.all_sprites, self.bullets)
                    if self.sound_enabled:
                        self.laser_sound.play()
        return True

    def handle_menu_click(self, event):

        for btn in self.buttons:
            if btn["rect"].collidepoint(event.pos):
                return btn["action"]

        return None

    def update(self):

        if not self.menu_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_score_update >= 1000:
                self.score += 1
                self.last_score_update = current_time

            self.all_sprites.update()
            self.explosions.update()

            hits = pygame.sprite.groupcollide(self.meteors, self.bullets, True, True)
            for meteor in hits:

                if self.sound_enabled:
                    self.meteor_explosion.play()

                explosion = Explosion(meteor.rect.center)
                self.all_sprites.add(explosion)
                self.explosions.add(explosion)

                self.score += 10
                meteor = Meteor(self.WIDTH, self.HEIGHT, self.meteor_images)
                self.all_sprites.add(meteor)
                self.meteors.add(meteor)

            if pygame.sprite.spritecollide(self.starship, self.meteors, False):
                if self.sound_enabled:
                    self.ship_explosion.play()

                if self.score > self.high_score:
                    self.high_score = self.score
                self.menu_active = True

    def draw(self):

        if self.menu_active:
            self.draw_menu()
        else:
            self.screen.blit(self.background, (0, 0))
            self.all_sprites.draw(self.screen)
            self.explosions.draw(self.screen)
            score_text = self.small_font.render(
                f"Счет: {self.format_score(self.score)}",
                True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def draw_menu(self):
        self.screen.fill((30, 30, 30))
        title = self.font.render("Космический Самолет", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4))
        self.screen.blit(title, title_rect)

        score_text = self.small_font.render(
            f"Последний счет: {self.format_score(self.score)} | "
            f"Рекорд: {self.format_score(self.high_score)}",
            True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        for btn in self.buttons:
            color = (100, 100, 200) if btn["rect"].collidepoint(pygame.mouse.get_pos()) else (50, 50, 150)
            pygame.draw.rect(self.screen, color, btn["rect"])
            text = self.small_font.render(btn["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=btn["rect"].center)
            self.screen.blit(text, text_rect)

    def run(self):
        try:
            while True:
                self.clock.tick(60)
                if not self.handle_events():
                    break
                self.update()
                self.draw()
        finally:
            self.check_and_save_highscore()
            pygame.quit()
            sys.exit()
