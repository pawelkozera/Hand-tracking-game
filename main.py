import pygame
import sys
import os
import mediapipe as mp
import cv2


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
        pygame.mouse.set_pos([300, 300])
    
    def check_for_ending_of_map(self):
        if self.level_map_rect.top >= 0:
            self.map_speed = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__
        self.border = 4
        self.color = "Black"
        self.controler = "hand"
        self.x_pos = 300
        self.y_pos = 300
    
    def draw_player(self, screen):
        if self.controler != "hand":
            self.x_pos, self.y_pos = pygame.mouse.get_pos()

        pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.border)
    
    def check_for_collision(self, maps, width, height):
        in_borders = self.x_pos - self.border > 0 and self.y_pos - self.border > 0 and self.y_pos + self.border < height and self.x_pos + self.border < width

        if in_borders:
            collision_positions = {
                'right': [self.x_pos + self.border, self.y_pos],
                'left': [self.x_pos - self.border, self.y_pos],
                'up': [self.x_pos, self.y_pos + self.border],
                'down': [self.x_pos, self.y_pos - self.border]
            }

            for position in collision_positions.values():
                if maps.level_map.get_at((position[0], position[1] - maps.level_map_rect.y))[:3] == maps.color_win:
                    print("win")
                if maps.level_map.get_at((position[0], position[1] - maps.level_map_rect.y))[:3] == maps.color_lose:
                    print("lose")


class MediapipeHandler():
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.cap = cv2.VideoCapture(0)
        self.image, self.success = self.cap.read()
        self.x_speed = 1
        self.y_speed = 1.5
    
    def get_image(self):
        self.success, self.image = self.cap.read()
        self.image = cv2.flip(self.image, 1)
    
    def get_image_result(self, hands):
        self.image.flags.writeable = False
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        return hands.process(self.image)

    def get_hand_position(self, results, width, height, player):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for index, landmark in enumerate(hand_landmarks.landmark):
                    if index == 8 and player.controler == "hand":
                        player.x_pos = int(landmark.x * width * self.x_speed)
                        player.y_pos = int(landmark.y * height * self.y_speed)
                        if player.y_pos < 0:
                            player.y_pos = 0 + player.border
                        if player.y_pos > height:
                            player.y_pos = height - player.border
    
    def draw_hand(self, results):
        self.image.flags.writeable = True
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    self.image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())

        cv2.imshow('Hand', self.image)


class Settings():
    def __init__(self):
        self.game_active = False
        self.music_volume = 0


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
    
    def check_if_button_clicked(self, settings):
        mouse_pos = pygame.mouse.get_pos()
        index = 0
        for img_rect in self.button_images_rect:
            if pygame.Rect.collidepoint(img_rect, mouse_pos) and pygame.mouse.get_pressed()[0]:
                if index == 0:
                    settings.game_active = True

            index += 1


def check_for_events(mpHandler):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mpHandler.cap.release()
            sys.exit()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    screen_size = width, height = 800, 600
    screen = pygame.display.set_mode(screen_size)

    maps = Maps()
    maps.select_map(0, width, height)

    player = Player()

    mpHandler = MediapipeHandler()

    settings = Settings()

    menu = Menu(screen_size)

    with mpHandler.mp_hands.Hands(
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
        while True:
            if settings.game_active:
                #mediapipe
                mpHandler.get_image()
                if not mpHandler.success:
                    print("Ignoring empty camera frame.")
                    continue
                
                results = mpHandler.get_image_result(hands)
                mpHandler.get_hand_position(results, width, height, player)
                mpHandler.draw_hand(results)

                #pygame
                check_for_events(mpHandler)
                
                maps.check_for_ending_of_map()
                maps.level_map_rect.y += maps.map_speed
                screen.blit(maps.level_map, maps.level_map_rect)

                player.draw_player(screen)
                player.check_for_collision(maps, width, height)
            else:
                menu.render_menu(screen)
                check_for_events(mpHandler)
                menu.check_if_button_clicked(settings)
            
            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    main()
