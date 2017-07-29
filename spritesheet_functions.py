'''
This module is used to crop the individual sprites from sprite sheets.
'''

import pygame

import img_sound_loader as img_loader
import constants

class SpriteSheet(object):
    ''' Class used to grab images out of a sprite sheet. '''
    def __init__(self, file_name,directory=''):
        # Load the sprite sheet.
        self.sprite_sheet,self.sprite_sheet_rect = \
            img_loader.load_image(file_name,directory)
    
    def get_image(self,x,y,width,height,colorkey = None):
        ''' Grab a single image out of a larger spritesheet.
        Pass in the x, y location of the sprite
        and the width an height of the sprite.
        And also check the transparent color.
        '''
        
        # Create a new blank image
        image = pygame.Surface([width,height]).convert()
        
        # Copy the image sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0,0), (x,y,width,height))
        
        # Check for transparent color
        if colorkey is not None:
            if colorkey is -1:
                # Get the transparent color from the top-left corner.
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
       
        return image