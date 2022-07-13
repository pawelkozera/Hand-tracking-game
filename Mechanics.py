import pygame
from sys import exit

def game_state_hand(player, maps, screen, settings, screen_size, results):
    if player.in_borders(maps, screen_size[1]) and results.multi_hand_landmarks:
        screen.fill((214, 85, 37))
        maps.check_for_ending_of_map()
        screen.blit(maps.level_map, maps.level_map_rect)
        player.draw_player(screen)
        player.check_for_collision(maps, screen)
    else:
        player.draw_hand_not_detected(settings, screen, screen_size)

def game_state_mouse(player, maps, screen, screen_size):
    player.get_mouse_position()
    if player.in_borders(maps, screen_size[1]):
        screen.fill((214, 85, 37))
        maps.check_for_ending_of_map()
        screen.blit(maps.level_map, maps.level_map_rect)
        player.draw_player(screen)
        player.check_for_collision(maps, screen)

def menu_state(menu, screen, settings, mpHandler):
    menu.render_menu(screen)
    menu.check_if_button_clicked(settings, mpHandler)

def settings_state(settings, screen, mpHandler):
    settings.render_settings(screen, mpHandler)

def check_for_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()