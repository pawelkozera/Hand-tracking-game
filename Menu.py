import pygame
import sys

class Menu():
    def __init__(self, screen_size):
        self.button_images = [pygame.image.load("menu/play.png").convert(), pygame.image.load("menu/settings.png").convert(), pygame.image.load("menu/quit.png").convert()]
        self.button_images_rect = []

        render_width = int(screen_size[0]/2)
        render_height = int(screen_size[1]/2)
        for img in self.button_images:
            self.button_images_rect.append(img.get_rect(midtop = (render_width, render_height)))
            render_height += 60
    
    def render_menu(self, screen):
        screen.fill((214, 85, 37))

        for i in range(len(self.button_images_rect)):
            screen.blit(self.button_images[i], self.button_images_rect[i])
    
    def check_if_button_clicked(self, settings, mpHandler, maps):
        mouse_pos = pygame.mouse.get_pos()
        index = 0
        for img_rect in self.button_images_rect:
            if pygame.Rect.collidepoint(img_rect, mouse_pos) and pygame.mouse.get_pressed()[0]:
                if index == 0:
                    settings.game_state = "game"
                    maps.same_map(settings.screen_size)
                elif index == 1:
                    settings.game_state = "settings"
                elif index == 2:
                    mpHandler.cap.release()
                    sys.exit()

            index += 1