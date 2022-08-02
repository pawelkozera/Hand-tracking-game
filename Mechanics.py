import pygame
from sys import exit

def game_state_hand(player, maps, screen, settings, results, streamer):
    if player.in_borders(maps, settings.screen_size[1]) and results.multi_hand_landmarks:
        screen.fill((214, 85, 37))
        maps.check_for_ending_of_map()
        screen.blit(maps.level_map, maps.level_map_rect)
        #streamer.render_streamer(screen)
        player.draw_player(screen)
        player.check_for_collision(maps, screen, settings.screen_size)
    else:
        player.draw_hand_not_detected(settings, screen,)

def game_state_mouse(player, maps, screen, settings, streamer):
    player.get_mouse_position()
    if player.in_borders(maps, settings.screen_size[1]):
        screen.fill((214, 85, 37))
        maps.check_for_ending_of_map()
        screen.blit(maps.level_map, maps.level_map_rect)
        streamer.render_dialogue(screen, settings, maps)
        streamer.render_streamer(screen)
        player.check_for_collision(maps, screen, settings.screen_size)
        player.draw_player(screen)

def menu_state(menu, screen, settings, mpHandler, maps):
    menu.render_menu(screen)
    menu.check_if_button_clicked(settings, mpHandler, maps)

def settings_state(settings, screen, mpHandler):
    settings.render_settings(screen, mpHandler)

def check_for_events(settings):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings.game_state = "menu"