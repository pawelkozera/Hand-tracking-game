import pygame
import sys


def state_handler(settings, mpHandler, player, maps, screen, screen_size, menu):
    if settings.game_state == "game":
        check_for_events(mpHandler)
        game_state(player, maps, screen, settings, screen_size)

    elif settings.game_state == "menu":
        check_for_events(mpHandler)
        menu_state(menu, screen, settings, mpHandler)

    elif settings.game_state == "settings":
        check_for_events(mpHandler)
        settings_state(settings, screen, mpHandler)

def game_state(player, maps, screen, settings, screen_size):
    if player.in_borders(maps, screen_size[1]) or not player.controler_hand:
        screen.fill((214, 85, 37))
        maps.check_for_ending_of_map()
        screen.blit(maps.level_map, maps.level_map_rect)
        player.draw_player(screen)
        player.check_for_collision(maps, screen)
    else:
        player.draw_hand_not_detected(settings, screen, screen_size)

def menu_state(menu, screen, settings, mpHandler):
    menu.render_menu(screen)
    menu.check_if_button_clicked(settings, mpHandler)

def settings_state(settings, screen, mpHandler):
    settings.render_settings(screen, mpHandler)

def check_for_events(mpHandler):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mpHandler.cap.release()
            sys.exit()