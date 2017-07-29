import pygame

import constants
from img_sound_loader import load_image
from img_sound_loader import resize_image

class Bullet(pygame.sprite.Sprite):
    def __init__(self,direction,posx,posy):
        
        super().__init__()
        
        self.image = None
        self.rect = None
        
        # Speed of bullet.
        self.speed_x = 0
        self.speed_y = 0
        
        # Set bullet damage.
        self.damage = 0
        
    def update(self):
        ''' Update itself position '''
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
        
    def isOutOfMap(self):
        return self.rect.x > constants.SCREEN_WIDTH or self.rect.x < -10 or\
               self.rect.y > constants.SCREEN_HEIGHT or self.rect.y < -10

class Bullet_01(Bullet):
    ''' This class represent a normal bullet. '''
    def __init__(self,direction,posx,posy):
        super().__init__(direction,posx,posy)
        
        # Add the picture for this bullet.
        self.image,self.rect = load_image("bullet01.png","resources/bullets",-1)
        self.image = resize_image([self.image],10,10)[0]
        
        # Determine the speed.
        if direction == "U":
            self.speed_y = -6
        if direction == "D":
            self.speed_y = 6
        if direction == "R":
            self.speed_x = 6
        if direction == "L":
            self.speed_x = -6
        
        # The position (x,y) that will spawn bullet.
        self.rect.x = posx
        self.rect.y = posy     
        
        # Set the bullet damage.
        self.damage = 1.5

class Bullet_02(Bullet):
    ''' This class represent Fire bullet for boss '''
    def __init__(self,direction,posx,posy):
        super().__init__(direction,posx,posy)
        
        
        self.moving_frames = []
        # Add the picture of each frames for this bullet.
        image,rect = load_image("skull_bullet1.png","resources/bullets",-1)
        self.moving_frames.append(image)
        image,rect = load_image("skull_bullet2.png","resources/bullets",-1)
        self.moving_frames.append(image)
        image,rect = load_image("skull_bullet3.png","resources/bullets",-1)
        self.moving_frames.append(image)
        image,rect = load_image("skull_bullet2.png","resources/bullets",-1)
        self.moving_frames.append(image) 
        
        # Determine the speed.
        if direction == "U":
            self.speed_y = -6
        if direction == "D":
            self.speed_y = 6
        if direction == "R":
            self.speed_x = 6
        if direction == "L":
            self.speed_x = -6        
        
        # Set the bullet damage.
        self.damage = 1
        
        # Set the begining frames
        self.image = self.moving_frames[0]
        self.rect = self.image.get_rect()
        # The position (x,y) that will spawn bullet.
        self.rect.x = posx
        self.rect.y = posy           
        
    def update(self):
        super().update()
        frame = (self.rect.y // 20) % len(self.moving_frames)
        self.image = self.moving_frames[frame]
        
        
        