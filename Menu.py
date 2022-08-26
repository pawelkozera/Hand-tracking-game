import pygame
import sys
from random import choice
from Mechanics import reset_game

class Menu():
    def __init__(self, screen_size):
        self.show_how_to_play = False
        render_width = int(screen_size[0]/2)

        self.how_to_player_instruction_img = pygame.image.load("menu/how_instruction.png").convert()
        self.how_to_player_instruction_rect = self.how_to_player_instruction_img.get_rect(midtop = (render_width, 20))

        self.back_button_img = pygame.image.load("menu/back.png").convert()
        self.back_button_rect = self.back_button_img.get_rect(center = (0, 0))

        self.current_game_title = 0
        self.game_title_img = [
                pygame.image.load("menu/game_title0.png").convert(),
                pygame.image.load("menu/game_title90.png").convert(),
                pygame.image.load("menu/game_title270.png").convert()
            ]
        self.game_title_rect = self.game_title_img[0].get_rect(center = (render_width, 100))
        self.button_images = [
                pygame.image.load("menu/play.png").convert(), 
                pygame.image.load("menu/settings.png").convert(),
                pygame.image.load("menu/how.png").convert(),
                pygame.image.load("menu/quit.png").convert()
            ]

        render_height = self.game_title_rect.bottomleft[1] + 50
        self.button_images_rect = []
        for img in self.button_images:
            self.button_images_rect.append(img.get_rect(midtop = (render_width, render_height)))
            render_height += self.button_images_rect[0].height + 20
    
    def render_game_title(self, screen):
        screen.blit(self.game_title_img[self.current_game_title], self.game_title_rect)
    
    def game_title_hover(self, screen_size):
        def random_game_title():
            if self.current_game_title == 0:
                deg = choice([90, 270])
                self.current_game_title = 1 if deg == 90 else 2
            elif self.current_game_title == 90:
                deg = choice([0, 270])
                self.current_game_title = 0 if deg == 0 else 2
            else:
                deg = choice([0, 90])
                self.current_game_title = 0 if deg == 0 else 1

        def img_get_rect():
            if self.current_game_title == 0:
                self.game_title_rect = self.game_title_img[0].get_rect(center = (x/2, 100))
            elif self.current_game_title == 1:
                self.game_title_rect = self.game_title_img[1].get_rect(center = (200, y/2))
            else:
                self.game_title_rect = self.game_title_img[2].get_rect(center = (x - 200, y/2))

        x, y = screen_size
        mouse_pos = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(self.game_title_rect, mouse_pos):
            random_game_title()
            img_get_rect()

    def render_menu(self, screen):
        for i in range(len(self.button_images_rect)):
            screen.blit(self.button_images[i], self.button_images_rect[i])
    
    def render_how_to_play(self, settings):
        x, y = settings.screen_size

        settings.screen.fill((214, 85, 37))
        settings.screen.blit(self.how_to_player_instruction_img, self.how_to_player_instruction_rect)
        self.render_back_button(settings.screen, x/2, y - 200)
        if self.check_back_button_events(settings):
            self.show_how_to_play = False
    
    def check_back_button_events(self, settings):
        for event in settings.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pygame.Rect.collidepoint(self.back_button_rect, mouse_pos):
                    return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
        
        return False

    def render_back_button(self, screen, x, y):
        self.back_button_rect = self.back_button_img.get_rect(center = (x, y))
        screen.blit(self.back_button_img, self.back_button_rect)
    
    def check_if_button_clicked(self, settings, mpHandler, maps, physics, level_events, streamer):
        mouse_pos = pygame.mouse.get_pos()

        for index, img_rect in enumerate(self.button_images_rect):
            if pygame.Rect.collidepoint(img_rect, mouse_pos):
                for event in settings.events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if index == 0:
                            settings.game_state = "game"
                            maps.same_map(settings.screen_size)
                            streamer.reset_animation_parameters()
                            reset_game(settings, physics, level_events)
                        elif index == 1:
                            settings.game_state = "settings"
                        elif index == 2:
                            self.show_how_to_play = True
                        elif index == 3:
                            mpHandler.cap.release()
                            sys.exit()