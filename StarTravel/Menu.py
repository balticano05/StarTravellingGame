import pygame

class Menu:

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.active = True
        self.score = 0
        self.high_score = 0

        self.buttons = [
            {"text": "Новая игра", "rect": pygame.Rect(0, 0, 300, 50), "action": "start"},
            {"text": "Выйти", "rect": pygame.Rect(0, 0, 300, 50), "action": "exit"}
        ]

        y = height // 2 - 100
        for btn in self.buttons:
            btn["rect"].center = (width // 2, y)
            y += 100

    def draw(self):
        self.screen.fill((30, 30, 30))
        text = self.font.render("Космический Смолет", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 4))
        self.screen.blit(text, text_rect)

        score_text = self.small_font.render(
            f"Последний счет: {self.score} | Рекорд: {self.high_score}",
            True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        for btn in self.buttons:
            color = (100, 100, 200) if btn["rect"].collidepoint(pygame.mouse.get_pos()) else (50, 50, 150)
            pygame.draw.rect(self.screen, color, btn["rect"])
            text = self.small_font.render(btn["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=btn["rect"].center)
            self.screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn["rect"].collidepoint(event.pos):
                    return btn["action"]
        return None