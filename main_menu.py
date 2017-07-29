import pygame

import constants
import main_game
from img_sound_loader import load_image
from img_sound_loader import load_sound

def main_menu():
    # Initialize sound for pygame
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    # Initialize pygame
    pygame.init()
    
    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("Jouney of the NERD!")
    
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 50)
    #pygame.mouse.set_visible(False)
    TITLE_IMAGE,TITLE_RECT = load_image("menu_title.png","resources/menu",-1)
    TUTORIAL_IMAGE,TUTORIAL_RECT = load_image("How_to_play.png","resources/menu")
    BACKGROUND_IMAGE,BACKGROUND_RECT = load_image("menu_bg.png","resources/backgrounds")
    
    # Load the music background
    music_bg = load_sound("main_menu.ogg","resources/sounds")
    channel_01 = pygame.mixer.find_channel()
    
    CONTINUE_IMAGE_COUNT = 0
    CONTINUE_IMAGE_LIST = []
    CONTINUE_IMAGE,CONTINUE_RECT = load_image("continue1.png","resources/menu")
    CONTINUE_IMAGE_LIST.append(CONTINUE_IMAGE)
    CONTINUE_IMAGE,CONTINUE_RECT = load_image("continue2.png","resources/menu")
    CONTINUE_IMAGE_LIST.append(CONTINUE_IMAGE)
    CONTINUE_IMAGE_CURRENT = CONTINUE_IMAGE_LIST[0]
    
    intro = True
    while intro:
        # Chck if the backgound music is stop
        if not channel_01.get_busy():
            channel_01.play(music_bg)        
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #stop play the backgound music
                    channel_01.fadeout(1000)
                    intro = False
        screen.fill(constants.WHITE)
        screen.blit(BACKGROUND_IMAGE,(0,0))
        
        #text = font.render("JOUNEY of the NERD!!!",1,(10,10,10))
        screen.blit(TITLE_IMAGE,(5,50))
        screen.blit(TUTORIAL_IMAGE,(150,500))
        
        CONTINUE_IMAGE_COUNT = (CONTINUE_IMAGE_COUNT + 1) % 120
        #print(CONTINUE_IMAGE_COUNT)
        
        CONTINUE_IMAGE_CURRENT = CONTINUE_IMAGE_LIST[(CONTINUE_IMAGE_COUNT//10)%2]
        
        screen.blit(CONTINUE_IMAGE_CURRENT,(400,600))
        pygame.display.flip()
        clock.tick(60)
        
    return main_game.main_game_loop(screen)

while True:
    restart = main_menu()
    if not restart:
        break
