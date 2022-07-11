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
                if settings.game_state == "game":
                    Mechanics.check_for_events(mpHandler)
                    Mechanics.game_state_hand(player, maps, screen, settings, screen_size, results)

                elif settings.game_state == "menu":
                    Mechanics.check_for_events(mpHandler)
                    Mechanics.menu_state(menu, screen, settings, mpHandler)

                elif settings.game_state == "settings":
                    Mechanics.check_for_events(mpHandler)
                    Mechanics.settings_state(settings, screen, mpHandler)
                
                pygame.display.update()
                clock.tick(60)
    else:
        while True:
            if settings.game_state == "game":
                Mechanics.check_for_events(mpHandler)
                Mechanics.game_state_mouse(player, maps, screen, screen_size)

            elif settings.game_state == "menu":
                Mechanics.check_for_events(mpHandler)
                Mechanics.menu_state(menu, screen, settings, mpHandler)

            elif settings.game_state == "settings":
                Mechanics.check_for_events(mpHandler)
                Mechanics.settings_state(settings, screen, mpHandler)
            
            pygame.display.update()
            clock.tick(60)

if __name__ == '__main__':
    main()
