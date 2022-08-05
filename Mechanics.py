import pygame
from sys import exit

def game_state_hand(player, maps, settings, results, streamer, chat):
    if player.in_borders(maps, settings.screen_size[1]) and results.multi_hand_landmarks:
        settings.screen.fill((214, 85, 37))
        maps.check_for_ending_of_map()
        settings.screen.blit(maps.level_map, maps.level_map_rect)
    
        streamer.render_dialogue(settings, maps)
        streamer.render_streamer(settings.screen)

        chat.draw_chat(maps, settings)
        chat.check_passed_time()
        chat.draw_text_to_chat(settings)
        chat.draw_live_sign(settings)

        player.draw_player(settings.screen)
        player.check_for_collision(maps, settings)
    else:
        player.draw_hand_not_detected(settings)

def game_state_mouse(player, maps, settings, streamer, chat):
    player.get_mouse_position()
    if player.in_borders(maps, settings.screen_size[1]):
        settings.screen.fill((214, 85, 37))
        maps.check_for_ending_of_map()
        settings.screen.blit(maps.level_map, maps.level_map_rect)

        streamer.render_dialogue(settings, maps)
        streamer.render_streamer(settings.screen)

        chat.draw_chat(maps, settings)
        chat.check_passed_time()
        chat.draw_text_to_chat(settings)
        chat.draw_live_sign(settings)
        
        player.check_for_collision(maps, settings)
        player.draw_player(settings.screen)

def menu_state(menu, settings, mpHandler, maps):
    menu.render_menu(settings.screen)
    menu.check_if_button_clicked(settings, mpHandler, maps)

def settings_state(settings):
    settings.render_settings()

def check_for_events(settings):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings.game_state = "menu"