import pygame
import cv2
import sys

class Settings():
    def __init__(self):
        self.game_state = "menu"
        self.music_volume = 0
        self.font = pygame.font.SysFont('arial', 30)
    
    def render_settings(self, screen, mpHandler, results):
        screen.fill((214, 85, 37))

    def choose_camera(self, screen, screen_size, mpHandler, clock):
        camera_rects = self.draw_cameras_selection(screen, screen_size, mpHandler)
        choosen_camera_index = 0
        mpHandler.cap = cv2.VideoCapture(choosen_camera_index)
        
        while True:
            new_camera_index = self.check_pressed_camera_button(camera_rects, mpHandler)

            if new_camera_index == len(camera_rects) - 1:
                self.game_state = "menu"
                break

            if new_camera_index != choosen_camera_index and new_camera_index != -1:
                choosen_camera_index = new_camera_index
                mpHandler.cap.release()
                mpHandler.cap = cv2.VideoCapture(choosen_camera_index)

            mpHandler.get_image()
            opencv_to_pygame_img = pygame.image.frombuffer(mpHandler.image.tostring(), mpHandler.image.shape[1::-1], "RGB")
            screen.blit(opencv_to_pygame_img, (int(screen_size[0]/2), int(screen_size[1] - 250)))

            check_for_events(mpHandler)
            pygame.display.update()
            clock.tick(60)     

    def draw_cameras_selection(self, screen, screen_size, mpHandler):
        screen.fill((214, 85, 37))
        render_width = int(screen_size[0]/2)
        render_height = int(screen_size[1]/5)

        text_surface = self.font.render("Select camera", False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(render_width, render_height))
        screen.blit(text_surface, text_rect)
        render_height += 60

        camera_rects = []
        
        for index in mpHandler.camera_indexes:
            text = "Camera " + str(index)
            text_surface = self.font.render(text, False, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(render_width, render_height))
            camera_rects.append(text_rect)
            screen.blit(text_surface, text_rect)
            render_height += 40
        
        text_surface = self.font.render("Accept", False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(render_width, render_height + 40))
        camera_rects.append(text_rect)
        screen.blit(text_surface, text_rect)

        return camera_rects

    def check_pressed_camera_button(self, rects, mpHandler):
        choosen_camera_index = -1
        mouse_pos = pygame.mouse.get_pos()
        index = 0

        for rect in rects:
            if pygame.Rect.collidepoint(rect, mouse_pos) and pygame.mouse.get_pressed()[0]:
                choosen_camera_index = index
            index += 1
        
        return choosen_camera_index

def check_for_events(mpHandler):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mpHandler.cap.release()
            sys.exit()