import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width=50, height=30):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self,direction):
        self.rect.x += direction