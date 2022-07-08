import os
import pygame

class Maps(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color_lose = (214, 85, 37)
        self.color_win = (34, 177, 76)
        self.level = 0
        self.map_speed = 3
        self.maps = []
        for map_lvl in os.listdir("levels/"):
            self.maps.append(map_lvl)

        self.level_map = pygame.image.load("levels/" + self.maps[self.level]).convert()
        self.level_map_rect = self.level_map.get_rect(midtop = (0, 0))
    
    def select_map(self, level, width, height):
        self.level_map = pygame.image.load("levels/" + self.maps[level]).convert()
        self.level_map_rect = self.level_map.get_rect(midtop = (int(width/2), self.level_map.get_height()*(-1) + height))
    
    def check_for_ending_of_map(self):
        if self.level_map_rect.top >= 0:
            self.map_speed = 0
        else:
            self.level_map_rect.y += self.map_speed