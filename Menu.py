import pygame
import sys
from Mechanics import reset_game

class Menu():
    def __init__(self, screen_size):
        render_width = int(screen_size[0]/2)

        self.game_title_img = pygame.image.load("menu/game_title.png").convert()
        self.game_title_rect = self.game_title_img.get_rect(center = (render_width, 100))
        self.button_images = [
                pygame.image.load("menu/play.png").convert(), 
                pygame.image.load("menu/settings.png").convert(), 
                pygame.image.load("menu/quit.png").convert()
            ]

        render_height = self.game_title_rect.bottomleft[1] + 50
        self.button_images_rect = []
        for img in self.button_images:
            self.button_images_rect.append(img.get_rect(midtop = (render_width, render_height)))
            render_height += self.button_images_rect[0].height + 20
    
    def render_game_title(self, screen):
        screen.blit(self.game_title_img, self.game_title_rect)

    def render_menu(self, screen):
        for i in range(len(self.button_images_rect)):
            screen.blit(self.button_images[i], self.button_images_rect[i])
    
    def check_if_button_clicked(self, settings, mpHandler, maps, physics, level_events, streamer):
        mouse_pos = pygame.mouse.get_pos()
        index = 0
        for img_rect in self.button_images_rect:
            if pygame.Rect.collidepoint(img_rect, mouse_pos) and pygame.mouse.get_pressed()[0]:
                if index == 0:
                    settings.game_state = "game"
                    maps.same_map(settings.screen_size)
                    streamer.reset_animation_parameters()
                    reset_game(settings, physics, level_events)
                elif index == 1:
                    settings.game_state = "settings"
                elif index == 2:
                    mpHandler.cap.release()
                    sys.exit()

            index += 1