'''
This module is used to managed with the images and sounds that will be loaded
into the game.
'''
import pygame
import os,sys

import constants

def load_image(filename,directory = '',colorkey = None):
    ''' This will load the image if exist '''
    # Get the full path of the file
    fullname = os.path.join(directory,filename)
    # Try to load image. If error, end the program.
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print("Cannot Load image: ",filename)
        raise
    # Check for transparent color
    if colorkey is not None:
        if colorkey is -1:
            # Get the transparent color from the top-left corner.
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)    
    # Convert image to pygame Surface obj.
    image = image.convert()
    # return image obj and image.get_rect() obj
    return image,image.get_rect()

def resize_image(image_list,width,height):
    ''' This will resize the image '''
    new_image_list = []
    for image in image_list:
        new_image_list.append(pygame.transform.scale(image,(width,height)))
    return new_image_list

def load_sound(filename,directory = ''):
    ''' This will load the sound file is exist '''
    
    # If the pygame.mixer module wasn't imported correctly
    # when call play(), do nothing
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    
    fullname = os.path.join(directory,filename)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print("Cannot load sound:", filename)
        raise SystemExit
    return sound