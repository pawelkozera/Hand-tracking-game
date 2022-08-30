import mediapipe as mp
import pygame
import cv2

class MediapipeHandler():
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.camera_indexes = []
        self.cap = cv2.VideoCapture(-1)
        self.success, self.image = self.cap.read()
        self.x_speed = 1
        self.y_speed = 1.5
    
    def find_camera_indexes(self):
        self.camera_indexes.clear()
        index = 0

        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                self.camera_indexes.append(index)
            cap.release()
            index += 1

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
                landmark = hand_landmarks.landmark[8]
                player.x_pos = int(landmark.x * width * self.x_speed)
                player.y_pos = int(landmark.y * height * self.y_speed)
                if player.y_pos < 0:
                    player.y_pos = 0 + player.border
                if player.y_pos > height:
                    player.y_pos = height - player.border
    
    def draw_hand(self, results, screen):
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

        opencv_to_pygame_img = pygame.image.frombuffer(self.image.tostring(), self.image.shape[1::-1], "RGB")
        screen.blit(opencv_to_pygame_img, (0, 0))