import pygame
import random

import constants
from img_sound_loader import load_image
from img_sound_loader import load_sound


def create_item(classname,x,y,player):
    enemy_dict = {HP_Potion.__name__:HP_Potion(x,y,player),
                  }
    try:
        return enemy_dict[classname]
    except KeyError:
        print("item doesn't match the key.")
        raise
    
class Item(pygame.sprite.Sprite):
    def __init__(self,x,y,player):
        super().__init__()
        
        # Set hit player sound.
        self.hit_player_sound = None
        
        # Moving frames sprite.
        self.moving_frames = []
        
        # Current image of item
        self.image = None
        self.rect = None
        
        # Get sound when hit
        self.hit_sound = None
        
        # Frame count
        self.frame_count = 0
    def update(self):
        pass
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
    def use_item(self):
        pass
        
class HP_Potion(Item):
    def __init__(self,x,y,player):
        super().__init__(x,y,player)
        
        self.player = player
        
        self.hit_sound = load_sound("HP_potion_hit.ogg","resources/sounds")
        
        # Add the picture of each frames for this item.
        image,rect = load_image("HP_potion1.png","resources/items",-1)
        self.moving_frames.append(image)
        image,rect = load_image("HP_potion2.png","resources/items",-1)
        self.moving_frames.append(image)
        
        self.image = self.moving_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        # Change image every 60 frames.(1 second)
        self.frame_count = (self.frame_count + 1) % 120
        frame = (self.frame_count // 60) % len(self.moving_frames)
        self.image = self.moving_frames[frame]
    def use_item(self):
        self.player.HP += 2