import pygame
import cv2
import Mechanics
from sys import exit

class Settings():
    def __init__(self, screen_size, screen):
        self.game_state = "menu"
        self.screen_size = screen_size
        self.screen = screen
        self.events = pygame.event.get()
        self.font = pygame.font.Font('fonts/NotoSerif-Regular.ttf', 30)
        self.font_chat = pygame.font.Font('fonts/NotoSerif-Regular.ttf', 14)

        music_volume_border_rect = pygame.Rect(self.screen_size[0]/2, 100, 400, 50)
        music_volume_border_rect.center = (self.screen_size[0]/2, 100)
        music_volume_rect = pygame.Rect(self.screen_size[0]/2, 100, 400, 50)
        music_volume_rect.midleft = music_volume_border_rect.midleft

        voice_volume_border_rect = pygame.Rect(self.screen_size[0]/2, 0, 400, 50)
        voice_volume_border_rect.midtop = (self.screen_size[0]/2, music_volume_border_rect.midtop[1] + 100)
        voice_volume_rect = pygame.Rect(self.screen_size[0]/2, 100, 400, 50)
        voice_volume_rect.midleft = voice_volume_border_rect.midleft

        fake_option_border_rect = pygame.Rect(self.screen_size[0]/2, 0, 400, 50)
        fake_option_border_rect.midtop = (self.screen_size[0]/2, voice_volume_border_rect.midtop[1] + 100)
        fake_option_rect = pygame.Rect(self.screen_size[0]/2, 100, 400, 50)
        fake_option_rect.midleft = fake_option_border_rect.midleft

        fake2_option_border_rect = pygame.Rect(self.screen_size[0]/2, 0, 400, 50)
        fake2_option_border_rect.midtop = (self.screen_size[0]/2, fake_option_border_rect.midtop[1] + 100)
        fake2_option_rect = pygame.Rect(self.screen_size[0]/2, 100, 400, 50)
        fake2_option_rect.midleft = fake2_option_border_rect.midleft

        self.option_rects = [
            ["Music volume", music_volume_border_rect, music_volume_rect, 50],
            ["Voice volume", voice_volume_border_rect, voice_volume_rect, 50],
            ["Resolution", fake_option_border_rect, fake_option_rect, 100],
            ["Quantum Turing machine", fake2_option_border_rect, fake2_option_rect, 69]
        ]
    
    def render_settings(self, menu):
        self.screen.fill((214, 85, 37))
        menu.render_back_button(self.screen, self.screen_size[0]/2, self.screen_size[1] - 100)
        self.render_music_settings()
        self.music_settings_collision()

        if menu.check_back_button_events(self):
            self.game_state = "menu"

    def render_music_settings(self, border_color = (0, 0, 0), bar_color = (189, 164, 109)):
        for option_rect in self.option_rects:
            music_volume_percentage_to_pixels = int(option_rect[3]/100*option_rect[1].width)
            self.draw_text(option_rect[0], self.screen_size[0]/2, option_rect[1].midtop[1] - 20, (255, 255, 255))
            option_rect[2].width = music_volume_percentage_to_pixels
            pygame.draw.rect(self.screen, bar_color, option_rect[2])
            pygame.draw.rect(self.screen, border_color, option_rect[1], 2)
    
    def music_settings_collision(self):
        for option_rect in self.option_rects:
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect.collidepoint(option_rect[1], mouse_pos) and pygame.mouse.get_pressed()[0]:
                max_volume = option_rect[1].width
                x = mouse_pos[0] - option_rect[1].x
                volume_percentage = int(x/max_volume  * 100)
                if volume_percentage == 99:
                    volume_percentage = 100
                option_rect[3] = volume_percentage

    def choose_camera(self, mpHandler, player):
        buttons_rects = self.draw_cameras_selection(mpHandler)
        highlighted_button = -1
        choosen_camera_index = -1
        selected_camera = False
        
        while True:
            self.events = pygame.event.get()
            new_camera_index = self.check_pressed_camera_button(buttons_rects)

            if new_camera_index != -1:
                buttons_rects = self.draw_cameras_selection(mpHandler)
                if highlighted_button != -1:
                    self.draw_selected_option(buttons_rects, highlighted_button, (0, 0, 0))
                self.draw_selected_option(buttons_rects, new_camera_index, (255, 255, 255))
                highlighted_button = new_camera_index

            if new_camera_index == len(buttons_rects) - 1: #accept
                self.game_state = "menu"
                break
            
            elif new_camera_index == len(buttons_rects) - 2: #mouse
                player.controler_hand = False
                if selected_camera:
                    selected_camera = False
                    mpHandler.cap.release()
                choosen_camera_index = -1

            elif new_camera_index == len(buttons_rects) - 3: #IPwebcam
                if selected_camera:
                    mpHandler.cap.release()
                selected_camera = True
                self.ip_webcam(mpHandler)
                buttons_rects = self.draw_cameras_selection(mpHandler)
                choosen_camera_index = -1

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
                    self.draw_text("Cannot open camera, using mouse instead.", self.screen_size[0]/1.5, self.screen_size[1]/4, (0, 0, 0))
                    mouse_rect = buttons_rects[len(buttons_rects) - 2]
                    self.draw_text("Play with mouse", mouse_rect.centerx, mouse_rect.centery, (255, 255, 255))
                else:
                    player.controler_hand = True
                    mpHandler.get_image()
                    opencv_to_pygame_img = pygame.image.frombuffer(mpHandler.image.tostring(), mpHandler.image.shape[1::-1], "RGB")
                    opencv_to_pygame_img = self.resize_camera_image(opencv_to_pygame_img)
                    self.screen.blit(opencv_to_pygame_img, (int(self.screen_size[0]/2), int(self.screen_size[1]/4)))

            Mechanics.check_for_events(self)
            pygame.display.update()

    def ip_webcam(self, mpHandler):
        accept_rect = self.draw_ip_webcam_menu()
        typing = True
        text = ""
        prev_text = text
        while typing:
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect.collidepoint(accept_rect, mouse_pos) and pygame.mouse.get_pressed()[0]:
                self.draw_text("Connecting with IP webcam...", self.screen_size[0]/2, self.screen_size[1]/2 + 80, (255, 255, 255))
                pygame.display.update()
                mpHandler.cap = cv2.VideoCapture("https://" + text + "/video")
                typing = False

            text = self.check_typing(text)
            if text != prev_text:
                prev_text = text
                accept_rect = self.draw_ip_webcam_menu()
            self.draw_text(text, self.screen_size[0]/2, self.screen_size[1]/3, (0, 0, 0))
            pygame.display.update()
    
    def draw_ip_webcam_menu(self):
        self.screen.fill((214, 85, 37))
        self.draw_text("Example: 111.111.11.1:2020", self.screen_size[0]/2, self.screen_size[1]/5, (0, 0, 0))
        self.draw_text("Start typing", self.screen_size[0]/2, self.screen_size[1]/4, (0, 0, 0))

        accept_rect = self.draw_text("Accept", self.screen_size[0]/2, self.screen_size[1]/2, (0, 0, 0))
        
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

    def resize_camera_image(self, opencv_to_pygame_img):
        size = opencv_to_pygame_img.get_size()
        if size[0] > self.screen_size[0]/2 or size[1] > self.screen_size[1]/1.5:
            opencv_to_pygame_img = pygame.transform.scale(opencv_to_pygame_img, (self.screen_size[0]/3, self.screen_size[1]/2))
        
        return opencv_to_pygame_img

    def draw_cameras_selection(self, mpHandler):
        self.screen.fill((214, 85, 37))
        render_width = int(self.screen_size[0]/4)
        render_height = int(self.screen_size[1]/5)

        self.draw_text("Select camera", render_width, render_height, (0, 0, 0))
        render_height += 40
        self.draw_text("(not recommended, low performance)", render_width, render_height, (0, 0, 0))
        render_height += 60

        camera_rects = []
        
        for index in mpHandler.camera_indexes:
            text = "Camera " + str(index)
            text_rect = self.draw_text(text, render_width, render_height, (0, 0, 0))
            camera_rects.append(text_rect)
            render_height += 40
        
        text_rect = self.draw_text("IP Webcam", render_width, render_height, (0, 0, 0))
        camera_rects.append(text_rect)
        render_height += 80

        text_rect = self.draw_text("Play with mouse", render_width, render_height, (0, 0, 0))
        camera_rects.append(text_rect)
        render_height += 40

        text_rect = text_rect = self.draw_text("Accept", render_width, render_height, (0, 0, 0))
        camera_rects.append(text_rect)

        return camera_rects
    
    def draw_selected_option(self, rect, index, color):
        if index == len(rect) - 1:
            self.draw_text("Accept", rect[index].centerx, rect[index].centery, color)
        elif index == len(rect) - 2:
            self.draw_text("Play with mouse", rect[index].centerx, rect[index].centery, color)
        elif index == len(rect) - 3:
            self.draw_text("IP Webcam", rect[index].centerx, rect[index].centery, color)
        else:
            text = "Camera " + str(index)
            self.draw_text(text, rect[index].centerx, rect[index].centery, color)
    
    def draw_text(self, text, x, y, color = (255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(int(x), int(y)))
        self.screen.blit(text_surface, text_rect)

        return text_rect

    def check_pressed_camera_button(self, rects):
        choosen_camera_index = -1
        mouse_pos = pygame.mouse.get_pos()

        for index, rect in enumerate(rects):
            if pygame.Rect.collidepoint(rect, mouse_pos) and pygame.mouse.get_pressed()[0]:
                choosen_camera_index = index
        
        return choosen_camera_index