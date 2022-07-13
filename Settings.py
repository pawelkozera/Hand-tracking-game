import pygame
import cv2
import Mechanics
from sys import exit

class Settings():
    def __init__(self):
        self.game_state = "menu"
        self.music_volume = 0
        self.font = pygame.font.SysFont('arial', 30)
    
    def render_settings(self, screen, mpHandler):
        screen.fill((214, 85, 37))

    def choose_camera(self, screen, screen_size, mpHandler, player):
        buttons_rects = self.draw_cameras_selection(screen, screen_size, mpHandler)
        highlighted_button = -1
        choosen_camera_index = -1
        selected_camera = False
        
        while True:
            new_camera_index = self.check_pressed_camera_button(buttons_rects)

            if new_camera_index != -1:
                buttons_rects = self.draw_cameras_selection(screen, screen_size, mpHandler)
                if highlighted_button != -1:
                    self.draw_selected_option(buttons_rects, highlighted_button, screen, (0, 0, 0))
                self.draw_selected_option(buttons_rects, new_camera_index, screen, (255, 255, 255))
                highlighted_button = new_camera_index

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
                self.ip_webcam(screen, screen_size, mpHandler)
                buttons_rects = self.draw_cameras_selection(screen, screen_size, mpHandler)

            elif new_camera_index != choosen_camera_index and new_camera_index != -1:
                if selected_camera:
                    mpHandler.cap.release()
                selected_camera = True
                choosen_camera_index = new_camera_index
                mpHandler.cap = cv2.VideoCapture(choosen_camera_index)

            if selected_camera:
                if mpHandler.cap is None or not mpHandler.cap.isOpened():
                    selected_camera = False
                    player.controler_hand = False
                    self.draw_text("Cannot open camera, using mouse instead.", screen_size[0]/2, screen_size[1]/4, screen, (0, 0, 0))
                    mouse_rect = buttons_rects[len(buttons_rects) - 2]
                    self.draw_text("Play with mouse", mouse_rect.centerx, mouse_rect.centery, screen, (255, 255, 255))
                else:
                    player.controler_hand = True
                    mpHandler.get_image()
                    opencv_to_pygame_img = pygame.image.frombuffer(mpHandler.image.tostring(), mpHandler.image.shape[1::-1], "RGB")
                    opencv_to_pygame_img = self.resize_camera_image(opencv_to_pygame_img, screen_size)
                    screen.blit(opencv_to_pygame_img, (int(screen_size[0]/2), int(screen_size[1]/4)))

            Mechanics.check_for_events()
            pygame.display.update()

    def ip_webcam(self, screen, screen_size, mpHandler):
        accept_rect = self.draw_ip_webcam_menu(screen, screen_size)
        typing = True
        text = ""
        prev_text = text
        while typing:
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect.collidepoint(accept_rect, mouse_pos) and pygame.mouse.get_pressed()[0]:
                self.draw_text("Connecting with IP webcam...", screen_size[0]/2, screen_size[1]/2 + 80, screen, (255, 255, 255))
                pygame.display.update()
                mpHandler.cap = cv2.VideoCapture("https://" + text + "/video")
                typing = False

            text = self.check_typing(text)
            if text != prev_text:
                prev_text = text
                accept_rect = self.draw_ip_webcam_menu(screen, screen_size)
            self.draw_text(text, screen_size[0]/2, screen_size[1]/3, screen, (0, 0, 0))
            pygame.display.update()
    
    def draw_ip_webcam_menu(self, screen, screen_size):
        screen.fill((214, 85, 37))
        self.draw_text("Example: 111.111.11.1:2020", screen_size[0]/2, screen_size[1]/5, screen, (0, 0, 0))
        self.draw_text("Start typing", screen_size[0]/2, screen_size[1]/4, screen, (0, 0, 0))

        accept_rect = self.draw_text("Accept", screen_size[0]/2, screen_size[1]/2, screen, (0, 0, 0))
        
        return accept_rect
    
    def check_typing(self, text):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        
        return text

    def resize_camera_image(self, opencv_to_pygame_img, screen_size):
        size = opencv_to_pygame_img.get_size()
        if size[0] > screen_size[0]/2 or size[1] > screen_size[1]/1.5:
            opencv_to_pygame_img = pygame.transform.scale(opencv_to_pygame_img, (screen_size[0]/3, screen_size[1]/2))
        
        return opencv_to_pygame_img

    def draw_cameras_selection(self, screen, screen_size, mpHandler):
        screen.fill((214, 85, 37))
        render_width = int(screen_size[0]/4)
        render_height = int(screen_size[1]/5)

        self.draw_text("Select camera", render_width, render_height, screen, (0, 0, 0))
        render_height += 60

        camera_rects = []
        
        for index in mpHandler.camera_indexes:
            text = "Camera " + str(index)
            text_rect = self.draw_text(text, render_width, render_height, screen, (0, 0, 0))
            camera_rects.append(text_rect)
            render_height += 40
        
        text_rect = self.draw_text("IP Webcam", render_width, render_height, screen, (0, 0, 0))
        camera_rects.append(text_rect)
        render_height += 40

        text_rect = self.draw_text("Play with mouse", render_width, render_height, screen, (0, 0, 0))
        camera_rects.append(text_rect)
        render_height += 40

        text_rect = text_rect = self.draw_text("Accept", render_width, render_height, screen, (0, 0, 0))
        camera_rects.append(text_rect)

        return camera_rects
    
    def draw_selected_option(self, rect, index, screen, color):
        if index == len(rect) - 1:
            self.draw_text("Accept", rect[index].centerx, rect[index].centery, screen, color)
        elif index == len(rect) - 2:
            self.draw_text("Play with mouse", rect[index].centerx, rect[index].centery, screen, color)
        elif index == len(rect) - 3:
            self.draw_text("IP Webcam", rect[index].centerx, rect[index].centery, screen, color)
        else:
            text = "Camera " + str(index)
            self.draw_text(text, rect[index].centerx, rect[index].centery, screen, color)
    
    def draw_text(self, text, x, y, screen, color):
        text_surface = self.font.render(text, False, color)
        text_rect = text_surface.get_rect(center=(int(x), int(y)))
        screen.blit(text_surface, text_rect)

        return text_rect

    def check_pressed_camera_button(self, rects):
        choosen_camera_index = -1
        mouse_pos = pygame.mouse.get_pos()
        index = 0

        for rect in rects:
            if pygame.Rect.collidepoint(rect, mouse_pos) and pygame.mouse.get_pressed()[0]:
                choosen_camera_index = index
            index += 1
        
        return choosen_camera_index