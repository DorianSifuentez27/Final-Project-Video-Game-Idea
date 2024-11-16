import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,barrier,speed):
        super().__init__()
        self.image = pygame.image.load('../graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_barrier = barrier
        self.ready = True
        self.laser_time = 0
        self.lazer_cooldown = 600

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE]:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()    

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >+ self.laser_cooldown:
                self.ready = True

    def shoot_laser(self):
        print('shoot laser')

    def barrier(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_barrier:
            self.rect.right = self.max_x_barrier

    def update(self):
        self.get_input()
        self.barrier()
        self.recharge()