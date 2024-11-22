import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.surface((4,20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)