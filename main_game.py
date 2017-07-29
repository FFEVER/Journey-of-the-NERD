import pygame

import constants
import stages
import characters
from img_sound_loader import load_image

def main_game_loop(screen):
    ''' Main Game Loop '''
    
    # Create the player
    player = characters.Player()
    
    # Set the player HP font.
    HP_font = pygame.font.Font(None,50)
    # Set the background for displaying HP
    HP_bg,HP_rect = load_image("HP_bar.png","resources/menu")
    
    # Create all the Stages
    stage_list = []
    stage_list.append(stages.Stage_01(player))
    stage_list.append(stages.Stage_02(player))
    stage_list.append(stages.Stage_03(player))
    
    # Set the current stage
    current_stage_no = 0
    current_stage = stage_list[current_stage_no]
    
    active_sprite_list = pygame.sprite.Group()
    player.stage = current_stage
    
    #--------add player starting position -----------
    player.rect.x = constants.SCREEN_WIDTH / 2
    player.rect.y = constants.SCREEN_HEIGHT / 2
    active_sprite_list.add(player)
    #----------------------------------------------------
    
    # Loop until the user clicks the close button.
    done = False
    
    # Restart game or not
    restart = False
    
    # Used to managed how fast the screen updates
    clock = pygame.time.Clock()
    
    # ---------- Main Program Loop ----------
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True
            if event.type == pygame.KEYDOWN:        
                if event.key == pygame.K_w:
                    player.move_up()
                if event.key == pygame.K_s:
                    player.move_down()
                if event.key == pygame.K_a:
                    player.move_left()
                if event.key == pygame.K_d:
                    player.move_right()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w and player.change_y < 0:
                    player.stop_vertical_move()
                if event.key == pygame.K_s and player.change_y > 0:
                    player.stop_vertical_move()
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop_horizontal_move()
                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop_horizontal_move()
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or\
                   event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop_shoot()
        # Check if user hold the arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.shoot_left()
        elif keys[pygame.K_RIGHT]:
            player.shoot_right()
        elif keys[pygame.K_UP]:
            player.shoot_up()
        elif keys[pygame.K_DOWN]:
            player.shoot_down()
        # Check if player is game over or not.
        if player.game_over:
            if current_stage.__name__ != stages.Game_Over_Stage.__name__:
                # Stop the previous background music.
                current_stage.channel_01.fadeout(500)
                # Change stage to game over stage.
                current_stage = stages.Game_Over_Stage(player)
            # Remove bullets
            player.bullets_list.empty()
            # Remove player.
            active_sprite_list.remove(player)
        
        # Check if it is ready to change to the next stage.
        if current_stage.next_stage == True:
            # Remove bullets
            player.bullets_list.empty()
            try:
                current_stage_no += 1
                current_stage = stage_list[current_stage_no]
                player.stage = current_stage
                player.rect.x = 0
                if current_stage_no == 2:
                    player.rect.y = 0
            except IndexError: # If index out of range. The player WIN!!
                if current_stage.__name__ != stages.Win_Stage.__name__:
                    # Stop the previous background music.
                    current_stage.channel_01.fadeout(500)
                    # Change stage to win stage.
                    current_stage = stages.Win_Stage(player)
                # remove player from the screen.
                active_sprite_list.remove(player)
                
        restart = current_stage.restart
        if restart:
            return restart
        # Update the player.
        active_sprite_list.update()
        
        # Update obstacle and monster in the stage
        current_stage.update()
        
        # ---- Game Logic ----
        
        
        
        # ---- Drawing state ----
        current_stage.draw(screen)
        active_sprite_list.draw(screen)
        for bullet in player.bullets_list:
            bullet.draw(screen)
        HP_obj = HP_font.render(str(player.HP),1,(10,10,10))
        screen.blit(HP_bg,(600,75))
        screen.blit(HP_obj,(665,83))
        
        
        # Limit the FPS
        clock.tick(constants.FPS)
        
        # Update the screen what we've drawn.
        pygame.display.flip()
    pygame.quit() #Close the pygame window on exit
    return restart