import pygame

import Maps
import Menu
import Player
import MediapipeHandler
import Settings
import Mechanics
import Streamer
import Chat
import Physics
import Level_events

def main():
    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()
    
    info = pygame.display.Info()
    screen_size = width, height = info.current_w - 200, info.current_h - 200
    screen = pygame.display.set_mode(screen_size)

    settings = Settings.Settings(screen_size, screen)

    physics = Physics.Physics()

    streamer = Streamer.Streamer("jerry")
    chat = Chat.Chat()
    maps = Maps.Maps()
    maps.select_map(width, height)

    player = Player.Player(screen_size)

    mpHandler = MediapipeHandler.MediapipeHandler()
    #mpHandler.find_camera_indexes()

    level_events = Level_events.Level_events()

    menu = Menu.Menu(screen_size)

    #settings.choose_camera(mpHandler, player)

    if player.controler_hand:
        with mpHandler.mp_hands.Hands(
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
            while True:
                settings.events = pygame.event.get()
                #mediapipe
                mpHandler.get_image()

                if not mpHandler.success:
                    print("Ignoring empty camera frame.")
                    continue
                
                results = mpHandler.get_image_result(hands)
                mpHandler.get_hand_position(results, width, height, player)
                
                #pygame
                if settings.game_state == "game":
                    pygame.mouse.set_visible(False)
                    Mechanics.game_state_running(player, maps, settings, streamer, chat, physics, level_events)

                elif settings.game_state == "menu":
                    pygame.mouse.set_visible(True)
                    Mechanics.menu_state(menu, settings, mpHandler, maps, physics, level_events, streamer)

                elif settings.game_state == "settings":
                    pygame.mouse.set_visible(True)
                    Mechanics.settings_state(settings, menu)
                
                physics.space.step(1/50)
                pygame.display.update()
                clock.tick(60)
    else:
        while True:
            settings.events = pygame.event.get()
            if settings.game_state == "game":
                pygame.mouse.set_visible(False)
                player.get_mouse_position()
                Mechanics.game_state_running(player, maps, settings, streamer, chat, physics, level_events)

            elif settings.game_state == "menu":
                pygame.mouse.set_visible(True)
                Mechanics.menu_state(menu, settings, mpHandler, maps, physics, level_events, streamer)

            elif settings.game_state == "settings":
                pygame.mouse.set_visible(True)
                Mechanics.settings_state(settings, menu)
            
            physics.space.step(1/50)
            pygame.display.update()
            clock.tick(60)

if __name__ == '__main__':
    main()
