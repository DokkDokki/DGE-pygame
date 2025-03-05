import pygame

class NotificationMessage:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(None, 30)

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.x, self.y))

    def set_text(self, text):
        self.text = text