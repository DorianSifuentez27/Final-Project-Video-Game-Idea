import pygame, sys
from player import Player
import formation
from alien import Alien
from random import choice
from laser import Laser

class Game:
    def __init__(self):
        player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.shape = formation.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.formation_amount = 4
        self.formation_x_positions = [num * (screen_width / self.formation_amount) for num in range(self.formation_amount)]
        self.create_mul_formation(*self.formation_x_positions, x_start = screen_width / 15, y_start = 480)

        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()

    def create_formation(self, x_start, y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = formation.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def create_mul_formation(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_formation(x_start,y_start,offset_x)

    def alien_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                alien_sprite = Alien('red',x,y)
                self.aliens.add(alien_sprite) 

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self,distance):
        if self.aliens: 
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,6,screen_height)
            self.alien_lasers.add(laser_sprite)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.player.sprite.laser.draw(screen)  
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.update()
        self.alien_lasers.draw(screen)
        self.collision_checks()

    def collision_checks(self):
        if self.player.sprite.laser:
            for laser in self.player.sprite.laser:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser,self.aliens,True):
                    laser.kill()
            
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    pygame.quit()
                    sys.exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien,self.player,False):
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    pygame.init ()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30,30,30))
        game.run()

        pygame.display.flip()
        clock.tick(60)