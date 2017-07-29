'''
This modle is used to define each stage definition
'''

import pygame
import os,sys

import constants
import img_sound_loader as img_loader
from img_sound_loader import load_sound
import obstacles
import enemies
import items

class Stage():
    ''' This is a super-class used to define a stage. '''
    # Background image
    background = None
    
    def __init__(self,player):
        self.music_bg = None# Load the music background
        self.channel_01 = pygame.mixer.find_channel()
        
        self.monster_list = pygame.sprite.Group()
        self.obstacle_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.bullet_passable_obj_list = pygame.sprite.Group()
        # Add bullet_list for the boss bullet.
        self.bullet_list = pygame.sprite.Group()        
        self.item_list = pygame.sprite.Group()
        self.player = player
        # Did the stage is complete
        self.complete = False
        
        # Are we ready to change to the next stage
        self.next_stage = False
        
        # Do we need to restart.
        self.restart = False
        
        # Frame count
        self.frame_count = 0
        
        self.ARROW,self.ARROW_RECT = \
            img_loader.load_image("arrow_right.png","resources/menu",-1)
        
    def update(self):
        ''' Update everything on this level. '''
        # Update sound.
        # Check if channel 01 is playing or not. If not play it
        if not self.channel_01.get_busy() and not self.next_stage and not self.player.game_over:
            self.channel_01.play(self.music_bg)               
        
        self.monster_list.update()
        for monster in self.monster_list:
            if monster.HP <= 0:
                self.monster_list.remove(monster)
        self.obstacle_list.update()
        self.wall_list.update()
        self.bullet_passable_obj_list.update()
        self.item_list.update()
        
    def draw(self, screen):
        ''' Draw everything on this level. '''
        # Draw the background
        screen.fill(constants.BLACK)
        screen.blit(self.background,(0,0))
        
        # Draw all sprite lists
        self.monster_list.draw(screen)
        self.obstacle_list.draw(screen)
        self.bullet_list.draw(screen)
        self.item_list.draw(screen)

class Stage_01(Stage):
    ''' Definition for Stage 1 '''
    
    def __init__(self,player):
        ''' Create Stage 1. '''
        self.__name__ = "Stage_01"
        super().__init__(player)
        
        # Load sound
        self.music_bg = load_sound("stage_1.ogg","resources/sounds")
        
        # Load a backgound image.
        self.background,self.background_rect = \
            img_loader.load_image("stage1_bg.png","resources/backgrounds")
        
        # Get the monster spawning pattern
        monsters_pattern = [[enemies.Mushroom.__name__,-100,400,player], # Left side
                            [enemies.Green_Slime.__name__,400,-100,player], # Top
                            [enemies.Green_Slime.__name__,410,-100,player], # Top
                            [enemies.Green_Slime.__name__,390,-100,player], # Top
                            [enemies.Mushroom.__name__,900,400,player], # Right
                            [enemies.Green_Slime.__name__,390,900,player], # Bottom
                            [enemies.Green_Slime.__name__,400,900,player], # Bottom
                            [enemies.Green_Slime.__name__,410,900,player], # Bottom
                            [enemies.Mushroom.__name__,-100,400,player], # Left
                            [enemies.Green_Slime.__name__,400,-100,player], # Top
                            [enemies.Mushroom.__name__,900,400,player], # Right
                            [enemies.Green_Slime.__name__,400,900,player], # Bottom
                            [enemies.Orange_Slime.__name__,-100,390,player], # Left
                            [enemies.Orange_Slime.__name__,-100,410,player], # Left
                            [enemies.Orange_Slime.__name__,-100,420,player], # Left
                            [enemies.Orange_Slime.__name__,-100,430,player], # Left
                            [enemies.Troll.__name__,-300,400,player], # Left
                            [enemies.Troll.__name__,1100,415,player], # Left
                            [enemies.Troll.__name__,400,-300,player], # Left
                            [enemies.Troll.__name__,400,1100,player], # Left
                            ]
        for item in monsters_pattern:
            monster = enemies.create_enemy(item[0],item[1],item[2],item[3])
            monster.stage = self
            self.monster_list.add(monster)

        # Define the border of the stage
        walls_pattern = [[0,0,347,45], # Top-left
                         [503,0,300,45], # Top-right
                         [0,800-45,350,45], # Bottom-left
                         [500,800-45,350,45], # Bottom-right
                         [0,0,45,340], # Left-top
                         [0,500,45,300], # Left-bottom
                         [800-45,0,45,347], # Right-top
                         [800-45,500,45,347], # Right-bottom
                         [-400,300,400,45], # Left-outer-Top
                         [-400,300,45,200], # Left-outer-Left
                         [-400,500,400,34], # Left-outer-Bottom
                         [305,800,45,400], # Bottom-outer-Left
                         [305,1200,200,45], # Bottom-outer-Bottom
                         [500,800,45,400], # Bottom-outer-Right
                         [302,-400,45,400], # Top-outer-Left
                         [302,-400,200,45], # Top-outer-Top
                         [503,-400,45,400], # Top-outer-Right
                         [800,302,400,45], # Right-outer-Top
                         [1200,347,45,150], # Right-outer-Right
                         [800,500,400,45] # Right-outer-Bottom
                        ]
        for item in walls_pattern:
            wall = obstacles.Wall(item[0],item[1],item[2],item[3])
            self.wall_list.add(wall)
    def update(self):
        if self.complete and (self.player.rect.x > constants.SCREEN_WIDTH-50):
            self.next_stage = True
            self.channel_01.fadeout(500)
                 
        super().update()
        if len(self.monster_list) == 0:
            self.complete = True
    def draw(self,screen):
        super().draw(screen)
        if self.complete:
            self.frame_count = (self.frame_count + 1) % 100
            if self.frame_count < 60 :
                screen.blit(self.ARROW,(650,400))
            
            
            
class Stage_02(Stage):
    ''' Definition for Stage 2 '''
    
    def __init__(self,player):
            ''' Create Stage 2. '''
            self.__name__ = "Stage_02"
            super().__init__(player)
            
            # Load sound
            self.music_bg = load_sound("stage_2.ogg","resources/sounds")
            
            self.background,self.background_rect = \
                img_loader.load_image("stage2_bg.png","resources/backgrounds")
            
            # Get item spawn pattern.
            item_pattern = [[items.HP_Potion.__name__,400,400,player]
                            ]
            for item in item_pattern:
                new_item = items.create_item(item[0],item[1],item[2],item[3])
                self.item_list.add(new_item)
            
            # Get the monster spawning pattern.
            monsters_pattern = [[enemies.Red_Slime.__name__,-100,400,player], # Left side
                                [enemies.Green_Slime.__name__,900,400,player], # Right
                                [enemies.Red_Slime.__name__,-100,410,player], # Left side
                                [enemies.Green_Slime.__name__,900,410,player], # Right                                
                                [enemies.Red_Slime.__name__,-100,420,player], # Left side
                                [enemies.Green_Slime.__name__,900,420,player], # Right                                
                                [enemies.Skeleton.__name__,-200,400,player], # Left
                                [enemies.Skeleton.__name__,-250,410,player], # Left
                                [enemies.Skeleton.__name__,-300,420,player], # Left
                                [enemies.Skeleton.__name__,-310,420,player], # Left
                                [enemies.Skeleton.__name__,1000,400,player], # right
                                [enemies.Skeleton.__name__,1000,410,player], # Right
                                [enemies.Skeleton.__name__,1000,420,player], # Right
                                [enemies.Skeleton.__name__,1010,420,player], # Right
                                [enemies.Cthulu.__name__,0,-1000,player], # Corner
                                [enemies.Cthulu.__name__,800,-1000,player], # Corner
                                [enemies.Cthulu.__name__,0,1800,player], # Corner
                                [enemies.Cthulu.__name__,800,1800,player], # Corner
                                [enemies.Cthulu.__name__,400,2600,player], # Top
                                [enemies.Cthulu.__name__,400,-1800,player], # Bottm
                                [enemies.Golem.__name__,-1000,350,player], # Left
                                [enemies.Golem.__name__,-1010,360,player], # Left
                                [enemies.Golem.__name__,-1030,370,player], # Left
                                [enemies.Golem.__name__,1800,350,player], # Right
                                [enemies.Golem.__name__,1810,360,player], # Right
                                [enemies.Golem.__name__,1800,370,player], # Right
                                ]
            for item in monsters_pattern:
                monster = enemies.create_enemy(item[0],item[1],item[2],item[3])
                monster.stage = self
                self.monster_list.add(monster)
            
            #for monster in monster_spawn_pattern:
                #self.monster_list.add(monster)
            # Define the border of the stage
            walls_pattern = [[0,0,constants.SCREEN_WIDTH,45], # Top
                         [0,800-45,constants.SCREEN_WIDTH,45], # Bottom
                         [0,0,45,340], # Right-top
                         [0,500,45,300], # Right-bottom
                         [800-45,0,45,347], # Left-top
                         [800-45,500,45,347], # Left-bottom
                         [-1500,300,1500,45], # Left-outer-Top
                         [-1500,300,45,200], # Left-outer-Left
                         [-1500,500,1500,34], # Left-outer-Bottom
                         [800,302,1500,45], # Right-outer-Top
                         [2300,347,45,150], # Right-outer-Right
                         [800,500,1500,45] # Right-outer-Bottom                         
                        ]
            
            # add the second row tomb to the walls_pattern
            for x in range(100,800,100):
                walls_pattern.append([x,45,48,50])
                walls_pattern.append([x,constants.SCREEN_HEIGHT-100,48,50])
                                     
            for item in walls_pattern:
                wall = obstacles.Wall(item[0],item[1],item[2],item[3])
                self.wall_list.add(wall)            
    def update(self):
        if self.complete and (self.player.rect.x > constants.SCREEN_WIDTH-50):
            self.next_stage = True
            self.channel_01.fadeout(500)
        super().update()
        if len(self.monster_list) == 0:
            self.complete = True        
        
    def draw(self,screen):
        super().draw(screen)
        if self.complete:
            self.frame_count = (self.frame_count + 1) % 100
            if self.frame_count < 60 :
                screen.blit(self.ARROW,(650,400))
                
class Stage_03(Stage):
    ''' Definition for Stage 3 '''
    def __init__(self,player):
            ''' Create Stage 3. '''
            self.__name__ = "Stage_03"
            super().__init__(player)
            
            # Load sound
            self.music_bg = load_sound("stage_3.ogg","resources/sounds")
            
            self.background,self.background_rect = \
                img_loader.load_image("boss_stage_bg.png","resources/backgrounds")
            
            # Get item spawn pattern.
            item_pattern = [[items.HP_Potion.__name__,400,100,player]
                            ]
            for item in item_pattern:
                new_item = items.create_item(item[0],item[1],item[2],item[3])
                self.item_list.add(new_item)
            
            # Get the monster spawning pattern.
            monsters_pattern = [[enemies.Necromancer.__name__,450,650,player], # Boss!!
                                ]
            for item in monsters_pattern:
                monster = enemies.create_enemy(item[0],item[1],item[2],item[3])
                monster.stage = self
                self.monster_list.add(monster)
                
            # List obstacles in this Stage
            obstacles_pattern = [[200,150,obstacles.TREE[0],obstacles.TREE[1]],
                                 [550,150,obstacles.TREE[0],obstacles.TREE[1]],
                                 [350,300,obstacles.GATE[0],obstacles.GATE[1]],
                                 [382,300,obstacles.GATE[0],obstacles.GATE[1]],
                                 [414,300,obstacles.GATE[0],obstacles.GATE[1]],
                                 [300,600,obstacles.DEAD_TREE[0],obstacles.DEAD_TREE[1]],
                                 [550,650,obstacles.DEAD_TREE[0],obstacles.DEAD_TREE[1]],
                                 [100,550,obstacles.GATE[0],obstacles.GATE[1]],
                                 [700,600,obstacles.GATE[0],obstacles.GATE[1]]
                                 ]
            for item in obstacles_pattern:
                obstacle = obstacles.Obstacle(item[0],item[1],item[2],item[3])
                self.obstacle_list.add(obstacle)
            
            # Define the border of the stage
            walls_pattern = [[0,-45,constants.SCREEN_WIDTH,45],
                             [0,800+45,constants.SCREEN_WIDTH,45],
                             [-45,0,45,constants.SCREEN_HEIGHT],
                             [800+45,0,45,constants.SCREEN_HEIGHT],
                            ]
            for item in walls_pattern:
                wall = obstacles.Wall(item[0],item[1],item[2],item[3])
                self.wall_list.add(wall)
                
            river = obstacles.Wall(0,400,constants.SCREEN_WIDTH,45)
            self.bullet_passable_obj_list.add(river)
    def update(self):
        if self.complete and (self.player.rect.x > constants.SCREEN_WIDTH-50):
            self.next_stage = True
            self.channel_01.fadeout(500)
        super().update()
        if len(self.monster_list) == 0:
            self.complete = True
    def draw(self,screen):
        super().draw(screen)
        if self.complete:
            self.frame_count = (self.frame_count + 1) % 100
            if self.frame_count < 60 :
                screen.blit(self.ARROW,(650,200))
            
class Game_Over_Stage(Stage):
    def __init__(self,player):
        super().__init__(player)
        self.__name__ = "Game_Over_Stage"
        
        # Load sound
        self.music_bg = load_sound("game_over.ogg","resources/sounds")
        # For game_over_stage play this only once.
        self.channel_01.play(self.music_bg)
        
        self.background_list = []
        # Load a backgound image.
        background,background_rect = \
            img_loader.load_image("game_over_bg.png","resources/backgrounds")
        self.background_list.append(background)
        
        # Load a backgound image.
        background,background_rect = \
            img_loader.load_image("game_over_bg2.png","resources/backgrounds")
        self.background_list.append(background)
    def draw(self,screen):
        ''' Draw everything on this level. '''
        # Draw the background
        screen.fill(constants.BLACK)
        self.frame_count = (self.frame_count + 1) % 120
        if self.frame_count < 60:
            screen.blit(self.background_list[1],(0,0))
        elif 60 <= self.frame_count < 120:   
            screen.blit(self.background_list[0],(0,0)) 
    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.restart = True
            
class Win_Stage(Stage):
    def __init__(self,player):
        super().__init__(player)
        self.__name__ = "Win_Stage"
        
        # Load sound
        self.music_bg = load_sound("win.ogg","resources/sounds")
        # For game_over_stage play this only once.
        self.channel_01.play(self.music_bg)
        
        self.background_list = []
        # Load a backgound image.
        background,background_rect = \
            img_loader.load_image("win_bg1.png","resources/backgrounds")
        self.background_list.append(background)
        
        # Load a backgound image.
        background,background_rect = \
            img_loader.load_image("win_bg2.png","resources/backgrounds")
        self.background_list.append(background)
    def draw(self,screen):
        ''' Draw everything on this level. '''
        # Draw the background
        screen.fill(constants.BLACK)
        self.frame_count = (self.frame_count + 1) % 120
        if self.frame_count < 60:
            screen.blit(self.background_list[1],(0,0))
        elif 60 <= self.frame_count < 120:   
            screen.blit(self.background_list[0],(0,0)) 
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.restart = True