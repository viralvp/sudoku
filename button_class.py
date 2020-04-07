import pygame


class Button:
    def __init__(self, x, y, width, height, text=None, color=(73, 73, 73), highlighted_color=(189, 189, 189), function=None, params=None):
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.color = color
        self.highlighted_color = highlighted_color
        self.function = function
        self.params = params
        self.highlighted = False

    def update(self, mouse):
        self.highlighted = self.rect.collidepoint(mouse)

    def draw(self, window):
        self.image.fill(self.highlighted_color if self.highlighted else self.color)
        window.blit(self.image, self.pos)
