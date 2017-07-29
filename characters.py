'''
This module define the characters
'''

import pygame

from spritesheet_functions import SpriteSheet
from img_sound_loader import resize_image
from img_sound_loader import load_sound
import constants
import bullets

class Player(pygame.sprite.Sprite):
    ''' This class represents the character that the player control. '''
    def __init__(self):
        super().__init__()
        
        # The game over state.
        self.game_over = False
        
        # Set player HP.
        self.HP = 5
        
        # Set the sound when player hit monster.
        # Load sound
        self.hit_monster_sound = load_sound("hit_monster.ogg","resources/sounds")        
        
        # Set speed of player
        self.speed = 3
        self.change_x = 0
        self.change_y = 0
        
        # This holds all the images for the animated walk up/down/left/right
        # of the player.
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.walking_frames_u = []
        self.walking_frames_d = []
        
        # The direction that player is facing.
        self.direction = "D"
        
        # The player state shooting or not.
        self.isShooting = False
        
        # List of bullets that have been shot.
        self.bullets_list = None
        self.bullets_list = pygame.sprite.Group()
        
        # Bullet count and shoot rate.
        self.bullet_count = 0
        self.shoot_rate = 20
        
        # List of sprites we can bump against
        self.stage = None
        
        
        sprite_sheet = SpriteSheet("player_sprite_blue.png","resources/characters")
        # Get the posture while walking downwards
        image = sprite_sheet.get_image(0,0,32,48,-1)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(32,0,32,48,-1)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(64,0,32,48,-1)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(96,0,32,48,-1)
        self.walking_frames_d.append(image)
        self.walking_frames_d = \
            resize_image(self.walking_frames_d,int(32*1.5),int(48*1.5))
        # Get the posture while walking left
        image = sprite_sheet.get_image(0,48,32,48,-1)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(32,48,32,48,-1)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(64,48,32,48,-1)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(96,48,32,48,-1)
        self.walking_frames_l.append(image)
        self.walking_frames_l = \
                    resize_image(self.walking_frames_l,int(32*1.5),int(48*1.5))        
        # Get the posture while walking right
        image = sprite_sheet.get_image(0,96,32,48,-1)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(32,96,32,48,-1)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(64,96,32,48,-1)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(96,96,32,48,-1)
        self.walking_frames_r.append(image)
        self.walking_frames_r = \
                    resize_image(self.walking_frames_r,int(32*1.5),int(48*1.5))        
        # Get the posture while walking upwards
        image = sprite_sheet.get_image(0,144,32,48,-1)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(32,144,32,48,-1)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(64,144,32,48,-1)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(96,144,32,48,-1)
        self.walking_frames_u.append(image)
        self.walking_frames_u = \
                    resize_image(self.walking_frames_u,int(32*1.5),int(48*1.5))        
        
        # Set the starting image
        self.image = self.walking_frames_d[0]
        
        # Get the reference of the image rect.
        self.rect = self.image.get_rect()
        print(self.rect.x,self.rect.y)
    
    def update(self):
        '''Move the player and move the bullet'''
        
        #print(self.direction)
        #print(self.rect)
        #print(self.change_x,self.change_y)
        
        # Move left/right
        self.rect.x += self.change_x
        if self.direction == "R":
            # The frame will change on every 30 pixels moves
            if self.change_y != 0:
                frame = (self.rect.y // 30) % len(self.walking_frames_r)
            else:
                frame = (self.rect.x // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        if self.direction == "L":
            if self.change_y != 0:
                frame = (self.rect.y // 30) % len(self.walking_frames_l)
            else:
                frame = (self.rect.x // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
            
            
        # Check if the moves make us hit any wall.
        self.check_hit_obj_LR(self.stage.wall_list)
        # Check if the moves make us hit any bullet passable object.
        self.check_hit_obj_LR(self.stage.bullet_passable_obj_list)
        #Check if we hit any obstacle
        self.check_hit_obj_LR(self.stage.obstacle_list)      
        
        # Move up/down
        self.rect.y += self.change_y
        if self.direction == "U":
            # The frame will change on every 30 pixels moves
            if self.change_x != 0:
                frame = (self.rect.x // 30) % len(self.walking_frames_u)
            else:
                frame = (self.rect.y // 30) % len(self.walking_frames_u)
            self.image = self.walking_frames_u[frame]
        if self.direction == "D":
            # The frame will change on every 30 pixels moves
            if self.change_x != 0:
                frame = (self.rect.x // 30) % len(self.walking_frames_d)
            else:
                frame = (self.rect.y // 30) % len(self.walking_frames_d)
            self.image = self.walking_frames_d[frame]
        
        # Check if the moves make us hit any wall.
        self.check_hit_obj_UD(self.stage.wall_list)
        # Check if the moves make us hit any bullet passable object.
        self.check_hit_obj_UD(self.stage.bullet_passable_obj_list)
        #Check if we hit any obstacle
        self.check_hit_obj_UD(self.stage.obstacle_list)    
        # Check if we hit any monster
        self.check_hit_monster(self.stage.monster_list)
        # Check if we hit any bullet from monster.
        self.check_hit_bullet(self.stage.bullet_list)
        # Check if we hit any item.
        self.check_hit_item(self.stage.item_list)
        
        self.bullets_list.update()
        
        #Check if our bullet hit anything or out of map.
        for bullet in self.bullets_list:
            # Check if our bullet hit any wall.
            wall_hit_list = \
                pygame.sprite.spritecollide(bullet, self.stage.wall_list, False)
            for wall in wall_hit_list:
                self.bullets_list.remove(bullet)
            # Check if our bullet hit any obstacle.
            obstacle_hit_list = \
                pygame.sprite.spritecollide(bullet,self.stage.obstacle_list, False)
            for obstacle in obstacle_hit_list:
                self.bullets_list.remove(bullet)
            # Check if our bullet is out of map.
            if bullet.isOutOfMap():
                self.bullets_list.remove(bullet)   
        
    def check_hit_obj_LR(self,obj,remove = False):
        ''' 
        Check if this character hit obj while moving LEFT/RIGHT or not. 
        If hit, manage it. 
        '''
        block_hit_list = pygame.sprite.spritecollide(self,obj,remove)  
        for block in block_hit_list:
            # If we are moving right, set our left to the wall left.
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise, if we are moving left, do the opposite.
                self.rect.left = block.rect.right     
    def check_hit_obj_UD(self,obj,remove = False):
        ''' 
        Check if this character hit obj while moving UP/DOWN or not. 
        If hit, manage it. 
        '''
        block_hit_list = pygame.sprite.spritecollide(self,obj,remove)
        for block in block_hit_list:
            # If we are moving down, set our base to the wall top.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                # Otherwise, if we are moving up, do the opposite.
                self.rect.top = block.rect.bottom
    def check_hit_monster(self,monster,remove = False):
        '''
        Check if this character hit any monster.
        If hit, decrease HP by monster damage.
        '''
        monster_hit_list = pygame.sprite.spritecollide(self,monster,remove)
        for monster in monster_hit_list:
            #play the sound
            self.hit_monster_sound.play()
            # Decrease HP by monster damage
            self.HP -= monster.damage
            self.stage.monster_list.remove(monster)
            if self.HP <= 0:
                # No minus HP
                self.HP = 0
                self.game_over = True
    def check_hit_bullet(self,bullet,remove = False):
        '''
        Check if this character hit any monster.
        If hit, decrease HP by bullet damage.
        '''
        bullet_hit_list = pygame.sprite.spritecollide(self,bullet,remove)
        for bullet in bullet_hit_list:
            #play the sound
            self.hit_monster_sound.play()
            # Decrease HP by bullet damage
            self.HP -= bullet.damage
            # Remove bullet from stage
            self.stage.bullet_list.remove(bullet)
            if self.HP <= 0:
                # No minus HP
                self.HP = 0
                self.game_over = True
    def check_hit_item(self,item,remove = False):
        '''
        Check if player hit any item.
        If hit, use it.
        '''
        item_hit_list = pygame.sprite.spritecollide(self,item,remove)
        for item in item_hit_list:
            # Use item.
            item.use_item()
            item.hit_sound.play()
            # Remove the item from stage.
            self.stage.item_list.remove(item)
    def move_left(self):
        ''' Called when user press 'A' '''
        self.change_x = -1 * self.speed
        if not self.isShooting:
            self.direction = "L"
        
    def move_right(self):
        ''' Called when user press 'D' ''' 
        self.change_x = 1 * self.speed
        if not self.isShooting:
            self.direction = "R"
        
    def move_up(self):
        ''' Called when user press 'W' '''
        self.change_y = -1 * self.speed
        if not self.isShooting:
            self.direction = "U"
        
    def move_down(self):
        ''' Called when user press 'S' '''
        self.change_y = 1 * self.speed
        if not self.isShooting:
            self.direction = "D"
        
    def stop_vertical_move(self):
        ''' Called when user lets off the keyboard '''
        self.change_y = 0
        if not self.isShooting:
            if self.change_x < 0:
                self.direction = "L"
            if self.change_x > 0:
                self.direction = "R"            
    def stop_horizontal_move(self):
        ''' Called when user lets off the keyboard '''
        self.change_x = 0
        if not self.isShooting:
            if self.change_y < 0:
                self.direction = "U"
            if self.change_y > 0:
                self.direction = "D"  
                
    def create_bullet(self):
        ''' Create new bullet and Add bullet to bullets_list '''
        # Get the center of player.
        posx = self.rect.x + ((self.rect.right - self.rect.left) // 2)
        posy = self.rect.y + ((self.rect.bottom - self.rect.top) // 2)        
        
        # Create the bullet that moves to the left.
        bullet = bullets.Bullet_01(self.direction,posx,posy)
        self.bullets_list.add(bullet)
        
    def shoot_left(self):
        ''' Called when user press arrow 'left' '''
        self.direction = "L"
        self.isShooting = True
        self.bullet_count = (self.bullet_count + 1) % 1200
        # The bullet will come out depends on shoot_rate
        if (self.bullet_count % self.shoot_rate) == 0:
            self.create_bullet()
        
    def shoot_right(self):
        ''' Called when user press arrow 'right' '''
        self.direction = "R"
        self.isShooting = True
        
        self.bullet_count = (self.bullet_count + 1) % 1200
        # The bullet will come out depends on shoot_rate
        if (self.bullet_count % self.shoot_rate) == 0:
            self.create_bullet()
        
    def shoot_up(self):
        ''' Called when user press arrow 'up' '''
        self.direction = "U"
        self.isShooting = True
        
        self.bullet_count = (self.bullet_count + 1) % 1200
        # The bullet will come out depends on shoot_rate
        if (self.bullet_count % self.shoot_rate) == 0:
            self.create_bullet()
        
    def shoot_down(self):
        ''' Called when user press arrow 'down' '''
        self.direction = "D"
        self.isShooting = True
        
        self.bullet_count = (self.bullet_count + 1) % 1200
        # The bullet will come out depends on shoot_rate
        if (self.bullet_count % self.shoot_rate) == 0:
            self.create_bullet()
        
    def stop_shoot(self):
        ''' Called when user lets off the keyboard '''
        self.isShooting = False
        # Reset the bullet count to zero.
        self.bullet_count = 0
        # Reset the direction to the facing direction.
        if self.change_x < 0:
            self.direction = "L"
        if self.change_x > 0:
            self.direction = "R"
        if self.change_y < 0:
            self.direction = "U"
        if self.change_y > 0:
            self.direction = "D"