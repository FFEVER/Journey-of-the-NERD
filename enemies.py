import pygame
import math
import random

import constants
from img_sound_loader import load_image
from img_sound_loader import resize_image
from img_sound_loader import load_sound
import bullets


def create_enemy(classname,x,y,player):
    enemy_dict = {Mushroom.__name__:Mushroom(x,y,player),
                  Green_Slime.__name__:Green_Slime(x,y,player),
                  Orange_Slime.__name__:Orange_Slime(x,y,player),
                  Red_Slime.__name__:Red_Slime(x,y,player),
                  Troll.__name__:Troll(x,y,player),
                  Skeleton.__name__:Skeleton(x,y,player),
                  Cthulu.__name__:Cthulu(x,y,player),
                  Golem.__name__:Golem(x,y,player),
                  Necromancer.__name__:Necromancer(x,y,player)
                  }
    try:
        return enemy_dict[classname]
    except KeyError:
        print("Monster doesn't match the key.")
        raise

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,player):
        super().__init__()
        
        # Set hit bullet sound.
        self.hit_bullet_sound = None
        
        # This holds all the images for the animated walk up/down/left/right
        # of the monster.
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.walking_frames_u = []
        self.walking_frames_d = [] 
        
        # The direction that player is facing.
        self.direction = None
        
        self.change_x = 0
        self.change_y = 0
        self.speed = 0
        
        # Set enemy damage
        self.damage = 0
        
        # Hits point of monster
        self.HP = 1
        
        # Player object
        self.player = player
        
        # List of object we can dump in the stage.
        self.stage = None
        
        # Current image of monster
        self.image = None
        self.rect = None
        
        # Frame count
        self.frame_count = 0
        
    def update(self):
        # Move a monster into maps first.
        self.move_into_map()
        
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
        if self.direction == "U" and self.rect.x != self.player.rect.x:
            # The frame will change on every 30 pixels moves
            if self.change_x != 0:
                frame = (self.rect.x // 30) % len(self.walking_frames_u)
            else:
                frame = (self.rect.y // 30) % len(self.walking_frames_u)
            self.image = self.walking_frames_u[frame]
        if self.direction == "D" and self.rect.x != self.player.rect.x:
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
        
        # Check if we hit any bullet.
        self.check_hit_bullet(self.player.bullets_list)
    
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
    def check_hit_bullet(self,bullet_list,remove = False):
        '''
        Check if this monster hit any bullets.
        If hit, decrease HP by bullet damage.
        '''
        bullet_hit_list = pygame.sprite.spritecollide(self,bullet_list,remove)
        for bullet in bullet_hit_list:
            self.hit_bullet_sound.play()
            self.HP -= bullet.damage
            self.player.bullets_list.remove(bullet)
            
    def move_left(self):
        ''' Move monster to the left '''
        self.change_x = -1 * self.speed
        self.direction = "L"
        
    def move_right(self):
        ''' Move monster to the right '''
        self.change_x = 1 * self.speed
        self.direction = "R"
        
    def move_up(self):
        ''' Move monster up '''
        self.change_y = -1 * self.speed
        self.direction = "U"
        
    def move_down(self):
        ''' Move monster down '''
        self.change_y = 1 * self.speed
        self.direction = "D"
    def move_towards_player(self):
        ''' Move towards player '''
        # If on the right side of player. Move left.
        if self.rect.x > self.player.rect.x:
            self.move_left()
        # If on the left side of player. Move right.
        elif self.rect.x < self.player.rect.x:
            self.move_right()
        # If on the bottom side of player. Move up.
        if self.rect.y > self.player.rect.y:
            self.move_up()
        # If on the top side of player. Move down.
        elif self.rect.y < self.player.rect.y:
            self.move_down()
        # Chck if on the same x or y axis of player.
        if self.rect.x == self.player.rect.x:
            self.stop_horizontal_move()
        if self.rect.y == self.player.rect.y:
            self.stop_vertical_move()
    def move_into_map(self):
        ''' Check if a monster is out of map or not. If yes, move it into map. '''
        if self.rect.x < 0:
            self.move_right()
            self.stop_vertical_move()
        if self.rect.x > constants.SCREEN_WIDTH:
            self.move_left()
            self.stop_vertical_move()
        if self.rect.y < 0:
            self.move_down()   
            self.stop_horizontal_move()
        if self.rect.y > constants.SCREEN_HEIGHT:
            self.move_up()
            self.stop_horizontal_move()
    def random_move(self):
        move = random.randrange(4)
        if move == 0:
            self.move_left()
        elif move == 1:
            self.move_right()
        elif move == 2:
            self.move_up()
        elif move == 3:
            self.move_down()        
    
    def stop_vertical_move(self):
        ''' Stop the vertical moves. '''
        self.change_y = 0
    def stop_horizontal_move(self):
        ''' Stop the horizontal moves. '''
        self.change_x = 0
    def stop_move(self):
        ''' Stop all moves. '''
        self.change_x = 0
        self.change_y = 0
            
class Mushroom(Enemy):
    def __init__(self,x,y,player):
        super().__init__(x,y,player)
        self.hit_bullet_sound = load_sound("mushroom_hit.ogg","resources/sounds")
        
        self.HP = 2
        self.speed = 1
        
        self.direction = "D"
        
        # Get the posture while walking downwards
        image,rect = load_image("mushroom_down1.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("mushroom_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("mushroom_down3.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("mushroom_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        
        # Get the posture while walking left
        image,rect = load_image("mushroom_left1.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("mushroom_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("mushroom_left3.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("mushroom_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)

        # Get the posture while walking right
        image,rect = load_image("mushroom_right1.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("mushroom_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("mushroom_right3.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("mushroom_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
     
        # Get the posture while walking upwards
        image,rect = load_image("mushroom_up1.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("mushroom_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("mushroom_up3.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("mushroom_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        
        # Resize the image
        self.walking_frames_d = \
            resize_image(self.walking_frames_d,int(22*2),int(20*2))
        self.walking_frames_u = \
            resize_image(self.walking_frames_u,int(22*2),int(20*2))
        self.walking_frames_l = \
            resize_image(self.walking_frames_l,int(22*2),int(20*2))        
        self.walking_frames_r = \
            resize_image(self.walking_frames_r,int(22*2),int(20*2))        
        # Set the starting image
        self.image = self.walking_frames_d[0]
        
        # Get the reference of the image rect.
        self.rect = self.image.get_rect()
        # Set the spawn point.
        self.rect.x = x
        self.rect.y = y
        
        # Set enemy damage
        self.damage = 1      
    
    def update(self):
        self.frame_count = (self.frame_count + 1) % 300
        
        # Move towards the player for 180 frames.
        if self.frame_count < 180:
            self.move_towards_player()
        #Move randomly for 60 frames.
        elif self.frame_count / 180 == 1:
            self.random_move()
        # Move randomly again for 60 frames.
        elif self.frame_count / 240 == 1:
            self.random_move()
            
        super().update()
        
class Orange_Slime(Enemy):
    def __init__(self,x,y,player):
        super().__init__(x,y,player)
        self.hit_bullet_sound = load_sound("slime_hit.ogg","resources/sounds")
        
        self.HP = 1
        self.speed = 1
        
        self.direction = "D"
        
        # Get the posture while walking downwards left right and upwards.
        image,rect = load_image("orange_slime1.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        image,rect = load_image("orange_slime2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        image,rect = load_image("orange_slime3.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        image,rect = load_image("orange_slime2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        
        # Resize the image
        self.walking_frames_d = \
            resize_image(self.walking_frames_d,int(16*1.5),int(12*1.5))
        self.walking_frames_u = \
            resize_image(self.walking_frames_u,int(16*1.5),int(12*1.5))
        self.walking_frames_l = \
            resize_image(self.walking_frames_l,int(16*1.5),int(12*1.5))        
        self.walking_frames_r = \
            resize_image(self.walking_frames_r,int(16*1.5),int(12*1.5))
        
        # Set the starting image
        self.image = self.walking_frames_d[0]
        
        # Get the reference of the image rect.
        self.rect = self.image.get_rect()
        # Set the spawn point.
        self.rect.x = x
        self.rect.y = y
        
        # Set enemy damage
        self.damage = 1      
    
    def update(self):
        self.frame_count = (self.frame_count + 1) % 180
        
        # Move towards the player for 120 frames.
        if self.frame_count < 120:
            self.move_towards_player()
        #Move randomly for 60 frames.
        elif self.frame_count / 120 == 1:
            self.random_move()
        # Move randomly again for 60 frames.
        elif self.frame_count / 180 == 1:
            self.random_move()
            
        super().update()
        
class Green_Slime(Enemy):
    def __init__(self,x,y,player):
        super().__init__(x,y,player)
        self.hit_bullet_sound = load_sound("slime_hit.ogg","resources/sounds")
        
        self.HP = 1
        self.speed = 1
        
        self.direction = "D"
        
        # Get the posture while walking downwards left right and upwards.
        image,rect = load_image("green_slime1.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        image,rect = load_image("green_slime2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        image,rect = load_image("green_slime3.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        image,rect = load_image("green_slime2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        
        # Resize the image
        self.walking_frames_d = \
            resize_image(self.walking_frames_d,int(16*1.5),int(12*1.5))
        self.walking_frames_u = \
            resize_image(self.walking_frames_u,int(16*1.5),int(12*1.5))
        self.walking_frames_l = \
            resize_image(self.walking_frames_l,int(16*1.5),int(12*1.5))        
        self.walking_frames_r = \
            resize_image(self.walking_frames_r,int(16*1.5),int(12*1.5))
        
        
        # Set the starting image
        self.image = self.walking_frames_d[0]
        
        # Get the reference of the image rect.
        self.rect = self.image.get_rect()
        # Set the spawn point.
        self.rect.x = x
        self.rect.y = y
        
        # Set enemy damage
        self.damage = 1      
    def update(self):
        self.frame_count = (self.frame_count + 1) % 180
        
        # Move towards the player for 120 frames.
        if self.frame_count < 120:
            self.move_towards_player()
        #Move randomly for 60 frames.
        elif self.frame_count / 120 == 1:
            self.random_move()
        # Move randomly again for 60 frames.
        elif self.frame_count / 180 == 1:
            self.random_move()
            
        super().update()        
        
class Red_Slime(Enemy):
    def __init__(self,x,y,player):
        super().__init__(x,y,player)
        self.hit_bullet_sound = load_sound("slime_hit.ogg","resources/sounds")
        
        self.HP = 1
        self.speed = 1
        
        self.direction = "D"
        
        # Get the posture while walking downwards left right and upwards.
        image,rect = load_image("red_slime1.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        image,rect = load_image("red_slime2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        image,rect = load_image("red_slime3.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        image,rect = load_image("red_slime2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        self.walking_frames_l.append(image)
        self.walking_frames_r.append(image)
        self.walking_frames_u.append(image)
        
        # Resize the image
        self.walking_frames_d = \
            resize_image(self.walking_frames_d,int(16*1.5),int(12*1.5))
        self.walking_frames_u = \
            resize_image(self.walking_frames_u,int(16*1.5),int(12*1.5))
        self.walking_frames_l = \
            resize_image(self.walking_frames_l,int(16*1.5),int(12*1.5))        
        self.walking_frames_r = \
            resize_image(self.walking_frames_r,int(16*1.5),int(12*1.5))
        
        # Set the starting image
        self.image = self.walking_frames_d[0]
        
        # Get the reference of the image rect.
        self.rect = self.image.get_rect()
        # Set the spawn point.
        self.rect.x = x
        self.rect.y = y
        
        # Set enemy damage
        self.damage = 1      
    def update(self):
        self.frame_count = (self.frame_count + 1) % 180
        
        # Move towards the player for 120 frames.
        if self.frame_count < 120:
            self.move_towards_player()
        #Move randomly for 60 frames.
        elif self.frame_count / 120 == 1:
            self.random_move()
        # Move randomly again for 60 frames.
        elif self.frame_count / 180 == 1:
            self.random_move()
            
        super().update()        

        
class Troll(Enemy):
    def __init__(self,x,y,player):
        super().__init__(x,y,player)
        self.hit_bullet_sound = load_sound("troll_hit.ogg","resources/sounds")
        
        self.HP = 4
        self.speed = 1
        
        self.direction = "D"
        
        # Get the posture while walking downwards
        image,rect = load_image("troll_down1.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("troll_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("troll_down3.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("troll_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        
        # Get the posture while walking left
        image,rect = load_image("troll_left1.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("troll_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("troll_left3.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("troll_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)

        # Get the posture while walking right
        image,rect = load_image("troll_right1.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("troll_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("troll_right3.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("troll_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
     
        # Get the posture while walking upwards
        image,rect = load_image("troll_up1.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("troll_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("troll_up3.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("troll_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        
        # Resize the image
        self.walking_frames_d = \
            resize_image(self.walking_frames_d,int(26*2),int(30*2))
        self.walking_frames_u = \
            resize_image(self.walking_frames_u,int(26*2),int(30*2))
        self.walking_frames_l = \
            resize_image(self.walking_frames_l,int(15*2),int(29*2))        
        self.walking_frames_r = \
            resize_image(self.walking_frames_r,int(15*2),int(29*2))
        
        
        # Set the starting image
        self.image = self.walking_frames_d[0]
        
        # Get the reference of the image rect.
        self.rect = self.image.get_rect()
        # Set the spawn point.
        self.rect.x = x
        self.rect.y = y
        
        # Set enemy damage
        self.damage = 1      
    
    def update(self):
        self.frame_count = (self.frame_count + 1) % 270
        
        # Move towards the player for 150 frames. (2.5 seconds)
        if self.frame_count < 150:
            self.move_towards_player()
        #Move randomly for 60 frames.
        elif self.frame_count / 150 == 1:
            self.random_move()
        # Move randomly again for 60 frames.
        elif self.frame_count / 210 == 1:
            self.random_move()
            
        super().update()
        
class Skeleton(Enemy):
    def __init__(self,x,y,player):
        super().__init__(x,y,player)
        self.hit_bullet_sound = load_sound("skeleton_hit.ogg","resources/sounds")
        
        self.HP = 1
        self.speed = 1
        
        self.direction = "D"
        
        # Get the posture while walking downwards
        image,rect = load_image("skeleton_down1.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("skeleton_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("skeleton_down3.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("skeleton_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        
        # Get the posture while walking left
        image,rect = load_image("skeleton_left1.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("skeleton_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("skeleton_left3.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("skeleton_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)

        # Get the posture while walking right
        image,rect = load_image("skeleton_right1.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("skeleton_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("skeleton_right3.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("skeleton_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
     
        # Get the posture while walking upwards
        image,rect = load_image("skeleton_up1.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("skeleton_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("skeleton_up3.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("skeleton_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        
        # Resize the image
        self.walking_frames_d = \
            resize_image(self.walking_frames_d,int(15*2),int(20*2))
        self.walking_frames_u = \
            resize_image(self.walking_frames_u,int(15*2),int(20*2))
        self.walking_frames_l = \
            resize_image(self.walking_frames_l,int(11*2),int(19*2))        
        self.walking_frames_r = \
            resize_image(self.walking_frames_r,int(11*2),int(19*2))
        
        
        # Set the starting image
        self.image = self.walking_frames_d[0]
        
        # Get the reference of the image rect.
        self.rect = self.image.get_rect()
        # Set the spawn point.
        self.rect.x = x
        self.rect.y = y
        
        # Set enemy damage
        self.damage = 1      
    
    def update(self):
        self.frame_count = (self.frame_count + 1) % 240
        
        # Move towards the player for 120 frames. (2 seconds)
        if self.frame_count < 120:
            self.move_towards_player()
        #Move randomly for 60 frames.
        elif self.frame_count / 120 == 1:
            self.random_move()
        # Move randomly again for 60 frames.
        elif self.frame_count / 180 == 1:
            self.random_move()
            
        super().update()
        
class Cthulu(Enemy):
    ''' 
    This represents Cthulu monster.
    Nothing can block him.
    '''
    def __init__(self,x,y,player):
        super().__init__(x,y,player)
        self.hit_bullet_sound = load_sound("cthulu_hit.ogg","resources/sounds")
        
        self.HP = 4
        self.speed = 2
        
        self.direction = "D"
        
        # Get the posture while walking downwards
        image,rect = load_image("cthulu_down1.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("cthulu_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("cthulu_down3.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("cthulu_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        
        # Get the posture while walking left
        image,rect = load_image("cthulu_left1.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("cthulu_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("cthulu_left3.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("cthulu_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)

        # Get the posture while walking right
        image,rect = load_image("cthulu_right1.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("cthulu_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("cthulu_right3.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("cthulu_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
     
        # Get the posture while walking upwards
        image,rect = load_image("cthulu_up1.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("cthulu_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("cthulu_up3.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("cthulu_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        
        # Resize the image
        self.walking_frames_d = \
            resize_image(self.walking_frames_d,int(13*4),int(16*4))
        self.walking_frames_u = \
            resize_image(self.walking_frames_u,int(13*4),int(15*4))
        self.walking_frames_l = \
            resize_image(self.walking_frames_l,int(15*4),int(16*4))        
        self.walking_frames_r = \
            resize_image(self.walking_frames_r,int(15*4),int(16*4))
        
        
        # Set the starting image
        self.image = self.walking_frames_d[0]
        
        # Get the reference of the image rect.
        self.rect = self.image.get_rect()
        # Set the spawn point.
        self.rect.x = x
        self.rect.y = y
        
        # Set enemy damage
        self.damage = 2
    def check_hit_obj_LR(self,obj,remove = False):
        ''' 
        Override the origianl function to do nothing.
        '''
        pass  
    def check_hit_obj_UD(self,obj,remove = False):
        ''' 
        Override the origianl function to do nothing.
        '''
        pass
    
    def update(self):
        self.frame_count = (self.frame_count + 1) % 240
        
        # Move towards the player for 180 frames. (3 seconds)
        if self.frame_count < 180:
            self.move_towards_player()
        #Move randomly for 30 frames.
        elif self.frame_count / 180 == 1:
            self.random_move()
        # Move randomly again for 30 frames.
        elif self.frame_count / 210 == 1:
            self.random_move()
        super().update()
        
class Golem(Enemy):
    def __init__(self,x,y,player):
        super().__init__(x,y,player)
        self.hit_bullet_sound = load_sound("golem_hit.ogg","resources/sounds")
        
        self.HP = 5
        self.speed = 1
        
        self.direction = "D"
        
        # Get the posture while walking downwards
        image,rect = load_image("golem_down1.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("golem_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("golem_down3.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("golem_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        
        # Get the posture while walking left
        image,rect = load_image("golem_left1.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("golem_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("golem_left3.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("golem_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)

        # Get the posture while walking right
        image,rect = load_image("golem_right1.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("golem_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("golem_right3.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("golem_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
     
        # Get the posture while walking upwards
        image,rect = load_image("golem_up1.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("golem_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("golem_up3.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("golem_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        
        # Resize the image
        self.walking_frames_d = \
            resize_image(self.walking_frames_d,int(32*2),int(34*2))
        self.walking_frames_u = \
            resize_image(self.walking_frames_u,int(32*2),int(34*2))
        self.walking_frames_l = \
            resize_image(self.walking_frames_l,int(21*2),int(33*2))        
        self.walking_frames_r = \
            resize_image(self.walking_frames_r,int(21*2),int(33*2))
        
        
        # Set the starting image
        self.image = self.walking_frames_d[0]
        
        # Get the reference of the image rect.
        self.rect = self.image.get_rect()
        # Set the spawn point.
        self.rect.x = x
        self.rect.y = y
        
        # Set enemy damage
        self.damage = 2
    
    def update(self):
        self.frame_count = (self.frame_count + 1) % 240
        
        # Move towards the player for 120 frames. (2 seconds)
        if self.frame_count < 120:
            self.move_towards_player()
        #Move randomly for 60 frames.
        elif self.frame_count / 120 == 1:
            self.random_move()
        # Move randomly again for 60 frames.
        elif self.frame_count / 180 == 1:
            self.random_move()
            
        super().update()
        
class Necromancer(Enemy):
    def __init__(self,x,y,player):
        super().__init__(x,y,player)
        self.hit_bullet_sound = load_sound("necro_hit.ogg","resources/sounds")
        
        self.HP = 20
        self.speed = 3
        
        # The player state shooting or not.
        self.isShooting = False
        
        # List of bullets that have been shot.
        self.bullets_list = None
        self.bullets_list = pygame.sprite.Group()
        
        # Bullet count and shoot rate.
        self.bullet_count = 0
        self.shoot_rate = 10
        
        # Set the direction.
        self.direction = "D"
        
        # Get the posture while walking downwards
        image,rect = load_image("necro_down1.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("necro_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("necro_down3.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        image,rect = load_image("necro_down2.png","resources/monsters",-1)
        self.walking_frames_d.append(image)
        
        # Get the posture while walking left
        image,rect = load_image("necro_left1.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("necro_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("necro_left3.png","resources/monsters",-1)
        self.walking_frames_l.append(image)
        image,rect = load_image("necro_left2.png","resources/monsters",-1)
        self.walking_frames_l.append(image)

        # Get the posture while walking right
        image,rect = load_image("necro_right1.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("necro_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("necro_right3.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
        image,rect = load_image("necro_right2.png","resources/monsters",-1)
        self.walking_frames_r.append(image)
     
        # Get the posture while walking upwards
        image,rect = load_image("necro_up1.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("necro_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("necro_up3.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        image,rect = load_image("necro_up2.png","resources/monsters",-1)
        self.walking_frames_u.append(image)
        
        # Resize the image
        self.walking_frames_d = \
            resize_image(self.walking_frames_d,int(26*2),int(32*2))
        self.walking_frames_u = \
            resize_image(self.walking_frames_u,int(26*2),int(32*2))
        self.walking_frames_l = \
            resize_image(self.walking_frames_l,int(16*2),int(31*2))        
        self.walking_frames_r = \
            resize_image(self.walking_frames_r,int(22*2),int(31*2))
    
        
        # Set the starting image
        self.image = self.walking_frames_d[0]
        
        # Get the reference of the image rect.
        self.rect = self.image.get_rect()
        # Set the spawn point.
        self.rect.x = x
        self.rect.y = y
        
        # Set enemy damage
        self.damage = 2
    
    def update(self):
        self.frame_count = (self.frame_count + 1) % 240
        
        if self.frame_count < 120:
            self.shoot_up()
        # Move towards the player for 60 frames. (1 seconds)
        if self.frame_count < 60:
            self.move_towards_player()
        #Move randomly for 60 frames.
        elif self.frame_count / 60 == 1:
            self.random_move()
        # Move randomly again for 60 frames.
        elif self.frame_count / 120 == 1:
            self.random_move()
        elif self.frame_count / 180 == 1:
            self.random_move()
            
        super().update()
        
        self.bullets_list.update()
        
        #Check if our bullet hit anything or out of map.
        for bullet in self.bullets_list:
            # Check if our bullet hit any wall.
            wall_hit_list = \
                pygame.sprite.spritecollide(bullet, self.stage.wall_list, False)
            for wall in wall_hit_list:
                self.bullets_list.remove(bullet)
                self.stage.bullet_list.remove(bullet)
            # Check if our bullet hit any obstacle.
            obstacle_hit_list = \
                pygame.sprite.spritecollide(bullet,self.stage.obstacle_list, False)
            for obstacle in obstacle_hit_list:
                self.bullets_list.remove(bullet)
                self.stage.bullet_list.remove(bullet)
            # Check if our bullet is out of map.
            if bullet.isOutOfMap():
                self.bullets_list.remove(bullet)  
                self.stage.bullet_list.remove(bullet)

    def create_bullet(self):
        ''' Create new bullet and Add bullet to bullets_list '''
        # Get the center of player.
        posx = self.rect.x + ((self.rect.right - self.rect.left) // 2)
        posy = self.rect.y + ((self.rect.bottom - self.rect.top) // 2)        
        
        # Create the bullet that moves to the left.
        bullet = bullets.Bullet_02(self.direction,posx,posy)
        self.bullets_list.add(bullet)
        # Add bullets to monster list of the current stage.
        self.stage.bullet_list.add(bullet)
     
    def shoot_up(self):
        ''' Shoot upwards. '''
        self.direction = "U"
        self.isShooting = True
        
        self.bullet_count = (self.bullet_count + 1) % 1200
        # The bullet will come out depends on shoot_rate
        if (self.bullet_count % self.shoot_rate) == 0:
            self.create_bullet()
    def stop_shoot(self):
        ''' Stop shooting.'''
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
    def check_hit_bullet(self,bullet_list,remove = False):
        super().check_hit_bullet(bullet_list)
        # If HP is equal or less than 0, empty the bullet list.
        if self.HP <= 0:
            self.bullets_list.empty()
            self.stage.bullet_list.empty()