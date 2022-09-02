import os
import pygame

class Maps():
    def __init__(self):
        self.color_lose = (214, 85, 37) #(214, 85, 37)
        self.color_win = (34, 177, 76)
        self.level = 6
        self.map_speed = 3
        self.maps = []

        self.level_map = pygame.image.load("levels/level_" + str(self.level) + ".png").convert()
        self.level_map_rect = self.level_map.get_rect(midtop = (0, 0))
    
    def select_map(self, width, height):
        self.level_map = pygame.image.load("levels/level_" + str(self.level) + ".png").convert()
        self.level_map_rect = self.level_map.get_rect(midtop = (int(width/2), self.level_map.get_height()*(-1) + height))
    
    def next_map_after_win(self, screen_size):
        self.level += 1
        self.map_speed = 3
        self.select_map(screen_size[0], screen_size[1])
    
    def same_map(self, screen_size):
        self.map_speed = 3
        self.select_map(screen_size[0], screen_size[1])
    
    def check_for_ending_of_map(self):
        if self.level_map_rect.top >= 0:
            self.map_speed = 0
        else:
            self.level_map_rect.y += self.map_speed