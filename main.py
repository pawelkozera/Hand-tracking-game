import pygame

import Maps
import Menu
import Player
import MediapipeHandler
import Settings

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
    
    settings.choose_camera(screen, screen_size, mpHandler, clock)

    menu = Menu.Menu(screen_size)

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
                Settings.check_for_events(mpHandler)

                if player.in_borders(maps, height) or not player.controler_hand:
                    screen.fill((214, 85, 37))
                    maps.check_for_ending_of_map()
                    screen.blit(maps.level_map, maps.level_map_rect)
                    player.draw_player(screen)
                    player.check_for_collision(maps, screen)
                else:
                    player.draw_hand_not_detected(settings, screen, screen_size)

            elif settings.game_state == "menu":
                menu.render_menu(screen)
                Settings.check_for_events(mpHandler)
                menu.check_if_button_clicked(settings, mpHandler)

            elif settings.game_state == "settings":
                settings.render_settings(screen, mpHandler, results)
                Settings.check_for_events(mpHandler)
            
            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    main()
