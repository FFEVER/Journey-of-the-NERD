'''
This module is for mapping obstacle and wall
'''

import pygame

import constants
from img_sound_loader import load_image

# List of obstacles' location
TREE = ["Tree.png","resources/obstacles"]
GATE = ["Gate.png","resources/obstacles"]
DEAD_TREE = ["Dead_tree.png","resources/obstacles"]
CACTUS = ["Cactus.png","resources/obstacles"]

class Wall(pygame.sprite.Sprite):
    '''This class represents the basic invisible wall '''
 
    def __init__(self, x, y, width, height):
        super().__init__()
 
        # Create a blank image
        self.image = pygame.Surface([width, height])   
        #self.image.fill(constants.BLACK)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
class Obstacle(pygame.sprite.Sprite):
    ''' This class represents the obstacles. '''
    def __init__(self, x, y,filename,directory = ''):
        super().__init__()
        
        # Load the image for this obstacle.
        self.image,self.rect = load_image(filename,directory,-1)
        self.rect.x = x
        self.rect.y = y
        
        