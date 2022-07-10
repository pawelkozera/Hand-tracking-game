import pygame

import Maps
import Menu
import Player
import MediapipeHandler
import Settings
import Mechanics

def main():
    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()
    
    info = pygame.display.Info()
    screen_size = width, height = info.current_w - 200, info.current_h - 200
    screen = pygame.display.set_mode(screen_size)

    maps = Maps.Maps()
    maps.select_map(0, width, height)

    player = Player.Player(screen_size)

    mpHandler = MediapipeHandler.MediapipeHandler()
    mpHandler.find_camera_indexes()

    settings = Settings.Settings()
    
    settings.choose_camera(screen, screen_size, mpHandler, clock, player)

    menu = Menu.Menu(screen_size)

    if player.controler_hand:
        with mpHandler.mp_hands.Hands(
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
            while True:
                #mediapipe
                mpHandler.get_image()

                if not mpHandler.success:
                    print("Ignoring empty camera frame.")
                    continue
                
                results = mpHandler.get_image_result(hands)
                mpHandler.get_hand_position(results, width, height, player)
                
                #pygame
                Mechanics.state_handler(settings, mpHandler, player, maps, screen, screen_size, menu)
                
                pygame.display.update()
                clock.tick(60)
    else:
        while True:
            Mechanics.state_handler(settings, mpHandler, player, maps, screen, screen_size, menu)
            
            pygame.display.update()
            clock.tick(60)

if __name__ == '__main__':
    main()
