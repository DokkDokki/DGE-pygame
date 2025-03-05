import pygame

class StatusWindow:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen, total_weight, object_size):
        pygame.draw.rect(screen, (240, 240, 240), self.rect)
        text_surface = self.font.render(f"Total Weight: {total_weight:.2f} kg", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 15))
        screen.blit(text_surface, text_rect)

        size_surface = self.font.render(f"Object Size: {object_size:.2f} kg", True, (0, 0, 0))
        size_rect = size_surface.get_rect(center=(self.rect.centerx, self.rect.centery + 15))
        screen.blit(size_surface, size_rect)