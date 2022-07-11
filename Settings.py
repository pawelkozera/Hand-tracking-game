import pygame
import cv2
import Mechanics

class Settings():
    def __init__(self):
        self.game_state = "menu"
        self.music_volume = 0
        self.font = pygame.font.SysFont('arial', 30)
    
    def render_settings(self, screen, mpHandler):
        screen.fill((214, 85, 37))

    def choose_camera(self, screen, screen_size, mpHandler, clock, player):
        buttons_rects = self.draw_cameras_selection(screen, screen_size, mpHandler)
        choosen_camera_index = -1
        selected_camera = False
        
        while True:
            new_camera_index = self.check_pressed_camera_button(buttons_rects)

            if new_camera_index == len(buttons_rects) - 1: #accept
                self.game_state = "menu"
                break
            
            elif new_camera_index == len(buttons_rects) - 2: #mouse
                player.controler_hand = False
                choosen_camera_index = -1
                if selected_camera:
                    selected_camera = False
                    mpHandler.cap.release()

            elif new_camera_index == len(buttons_rects) - 3: #IPwebcam
                if selected_camera:
                    mpHandler.cap.release()
                selected_camera = True
                mpHandler.cap = cv2.VideoCapture('https://192.168.43.1:8080/video')

            elif new_camera_index != choosen_camera_index and new_camera_index != -1:
                if selected_camera:
                    mpHandler.cap.release()
                selected_camera = True
                choosen_camera_index = new_camera_index
                mpHandler.cap = cv2.VideoCapture(choosen_camera_index)

            if selected_camera:
                player.controler_hand = True
                mpHandler.get_image()
                opencv_to_pygame_img = pygame.image.frombuffer(mpHandler.image.tostring(), mpHandler.image.shape[1::-1], "RGB")
                opencv_to_pygame_img = self.resize_camera_image(opencv_to_pygame_img, screen_size)

                screen.blit(opencv_to_pygame_img, (int(screen_size[0]/2), int(screen_size[1]/4)))

            Mechanics.check_for_events(mpHandler)
            pygame.display.update()
            clock.tick(60)

    def resize_camera_image(self, opencv_to_pygame_img, screen_size):
        size = opencv_to_pygame_img.get_size()
        if size[0] > screen_size[0]/2 or size[1] > screen_size[1]/1.5:
            opencv_to_pygame_img = pygame.transform.scale(opencv_to_pygame_img, (screen_size[0]/3, screen_size[1]/2))
        
        return opencv_to_pygame_img

    def draw_cameras_selection(self, screen, screen_size, mpHandler):
        screen.fill((214, 85, 37))
        render_width = int(screen_size[0]/4)
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
        
        text_surface = self.font.render("IP Webcam (Not recommended)", False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(render_width, render_height))
        camera_rects.append(text_rect)
        screen.blit(text_surface, text_rect)
        render_height += 40

        text_surface = self.font.render("Play with mouse", False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(render_width, render_height))
        camera_rects.append(text_rect)
        screen.blit(text_surface, text_rect)
        render_height += 40

        text_surface = self.font.render("Accept", False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(render_width, render_height + 40))
        camera_rects.append(text_rect)
        screen.blit(text_surface, text_rect)

        return camera_rects

    def check_pressed_camera_button(self, rects):
        choosen_camera_index = -1
        mouse_pos = pygame.mouse.get_pos()
        index = 0

        for rect in rects:
            if pygame.Rect.collidepoint(rect, mouse_pos) and pygame.mouse.get_pressed()[0]:
                choosen_camera_index = index
            index += 1
        
        return choosen_camera_index