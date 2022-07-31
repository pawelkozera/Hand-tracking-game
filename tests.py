import unittest
import Streamer
import Settings
import Maps
import Player

import pygame

class Tests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        screen_size = (1920, 1080)
        self.screen = pygame.display.set_mode(screen_size)
        
        self.player = Player.Player(screen_size)
        self.maps = Maps.Maps()
        self.maps.select_map(screen_size[0], screen_size[1])
        self.settings = Settings.Settings(screen_size)
        self.streamer = Streamer.Streamer("toast")
        self.streamer.texts[0] = "Hey Guys!"

    def test_split_dialogue_and_surfaces_rects(self):
        string = self.streamer.split_dialogue(self.settings, self.maps)
        self.assertEqual(string, [" Hey Guys!"], "One line")

        text_surfaces, text_rects = self.streamer.get_surfaces_and_rects(string, self.settings)
        self.assertEqual(len(text_surfaces), 1, "Length of surfaces one line")
        self.assertEqual(len(text_rects), 1, "Length of rects one line")

        self.streamer.texts[0] = "Hey guys! This is your fantastic streamer! Disguised Toast!!!!!!!!!!!"
        string = self.streamer.split_dialogue(self.settings, self.maps)
        self.assertEqual(string, [" Hey guys! This is your fantastic streamer!", "Disguised Toast!!!!!!!!!!!"], "multi line")

        text_surfaces, text_rects = self.streamer.get_surfaces_and_rects(string, self.settings)
        self.assertEqual(len(text_surfaces), 2, "Length of surfaces multi line")
        self.assertEqual(len(text_rects), 2, "Length of rects multi line")
    
    def test_next_map_after_win(self):
        current_lvl = self.maps.level
        current_speed = self.maps.map_speed
        self.maps.next_map_after_win(self.settings.screen_size)
        self.assertEqual(self.maps.level, current_lvl + 1, "Should increase lvl")
        self.assertEqual(self.maps.map_speed, current_speed, "Should have same speed")
    
    def test_same_map_after_lose(self):
        current_lvl = self.maps.level
        current_speed = self.maps.map_speed
        self.maps.same_map_after_lose(self.settings.screen_size)
        self.assertEqual(self.maps.level, current_lvl, "Should have same lvl")
        self.assertEqual(self.maps.map_speed, current_speed, "Should have same speed")
    
    def test_check_for_ending_of_map(self):
        self.maps.map_speed = 3
        self.maps.level_map_rect.y = -2
        self.maps.check_for_ending_of_map()
        self.assertEqual(self.maps.map_speed, 3, "Speed greater than 0, not the end of map")

        self.maps.check_for_ending_of_map()
        self.assertEqual(self.maps.map_speed, 0, "Should have speed equal 0, end of map")
    
    def test_player_in_borders(self):
        in_border = self.player.in_borders(self.maps, self.settings.screen_size[1])
        self.assertTrue(in_border, "Player not in map borders")

        self.player.x_pos = 10
        self.player.y_pos = 10
        in_border = self.player.in_borders(self.maps, self.settings.screen_size[1])
        self.assertFalse(in_border, "Player in map borders")

    def test_check_for_collision(self):
        self.player.x_pos = 10
        self.player.y_pos = 10
        current_lvl = self.maps.level
        current_speed = self.maps.map_speed

        self.player.check_for_collision(self.maps, self.screen, self.settings.screen_size)
        self.assertEqual(self.maps.level, current_lvl, "Should have same lvl after collision")
        self.assertEqual(self.maps.map_speed, current_speed, "Should have same speed after collision")


if __name__ == "__main__":
    unittest.main()