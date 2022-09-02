import pygame
from sys import exit

def game_state_running(player, maps, settings, streamer, chat, physics, level_events):
    settings.screen.fill((214, 85, 37))
    maps.check_for_ending_of_map()
    settings.screen.blit(maps.level_map, maps.level_map_rect)
    
    level_events.select_events_for_level(maps, physics, settings, streamer, chat, player)

    streamer.render_dialogue(settings, maps)
    streamer.check_passed_time()
    streamer.render_streamer(settings.screen)

    chat.draw_chat(maps, settings)
    chat.check_passed_time()
    chat.draw_text_to_chat(settings)
    chat.draw_live_sign(settings)
    chat.draw_view_box(settings.screen)
    chat.draw_number_of_viewers(settings)
    
    collision = player.check_for_collision(maps, settings)
    if collision == 1:
        maps.next_map_after_win(settings.screen_size)
        streamer.reset_animation_parameters()
        level_events.delete_classes_after_win()
        reset_game(settings, physics, level_events)
    elif collision == 2:
        maps.same_map(settings.screen_size)
        reset_game(settings, physics, level_events)
    elif collision == -1:
        maps.same_map(settings.screen_size)
        reset_game(settings, physics, level_events)
    elif collision >= 3 and collision <= 5:
        level_events.collision_handler(collision, maps, player)

    player.draw_player(settings.screen)

    check_for_events(settings)

def reset_game(settings, physics, level_events):
    physics.reset_space()
    level_events.reset()
    pygame.mouse.set_pos([int(settings.screen_size[0]/2), settings.screen_size[1] - 100])

def menu_state(menu, settings, mpHandler, maps, physics, level_events, streamer):
    settings.screen.fill((214, 85, 37))
    if not menu.show_how_to_play:
        menu.game_title_hover(settings.screen_size)
        menu.render_game_title(settings.screen)
        menu.render_menu(settings.screen)
        menu.check_if_button_clicked(settings, mpHandler, maps, physics, level_events, streamer)
    else:
        menu.render_how_to_play(settings)
    check_for_events(settings)

def settings_state(settings, menu):
    settings.render_settings(menu)
    check_for_events(settings)

def check_for_events(settings):
    for event in settings.events:
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                settings.game_state = "menu"