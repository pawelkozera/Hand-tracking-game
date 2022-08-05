import pygame
import random

class Chat():
    def __init__(self):
        self.users = ["ralph", "max", "tobby", "robert", "master21", "cornelius"]
        self.texts = ["haha", "start!! pogchamp pogchamp pogchamp pogchamp pogchamp pogchamp pogchamp pogchamp koniec!!"]
        self.used_texts = []
        self.used_users = []
        self.color_for_used_users = []
        
        self.chats = ["imgs/chat_t.png"]
        self.chat_rect = None
        self.live_t = ["imgs/live_t1.png", "imgs/live_t2.png"]
        self.live_t_index = 0

        self.time_since_live_animation = 0
        self.time_since_new_text = 0
        self.miliseconds_for_new_text = 1000

    def draw_text_to_chat(self, settings):
        x, y = self.chat_rect.bottomleft
        _, font_height = settings.font_chat.size("t")
        height_padding = 0

        for index, used_text in reversed(list(enumerate(self.used_texts))):
            string = self.used_users[index] + " : " + used_text
            text_width, _ = settings.font.size(string)
            
            if text_width >= self.chat_rect.width - 8:
                new_strings = self.split_text(string, settings)
                height_padding = self.draw_text_with_split(settings, new_strings, height_padding, font_height, x, y, index)
            else:
                height_padding = self.draw_text_without_split(settings, string, height_padding, font_height, x, y, index)
    
    def draw_text_without_split(self, settings, string, height_padding, font_height, x, y, color_index):
        index = string.find(":")
        if index == -1:
            text_surface = settings.font_chat.render(string, True, (255, 255, 255))
            text_rect = text_surface.get_rect(bottomleft=(x + 8, y - 10 - height_padding))
        else:
            text_surface_name = settings.font_chat.render(string[:index], True, self.color_for_used_users[color_index])
            text_rect_name = text_surface_name.get_rect(bottomleft=(x + 8, y - 10 - height_padding))

            text_surface = settings.font_chat.render(string[index:], True, (255, 255, 255))
            text_rect = text_surface.get_rect(bottomleft=(text_rect_name.bottomright[0], y - 10 - height_padding))
        
        height_padding += font_height

        if text_rect.y <= self.chat_rect.y + 64:
            self.remove_used_text_from_chat()
        else:
            if index == -1:
                settings.screen.blit(text_surface, text_rect)
            else:
                settings.screen.blit(text_surface_name, text_rect_name)
                settings.screen.blit(text_surface, text_rect)
        
        return height_padding

    def draw_text_with_split(self, settings, new_strings, height_padding, font_height, x, y, color_index):
        last_text_surface = settings.font_chat.render(new_strings[-1], True, (255, 255, 255))
        last_text_rect = last_text_surface.get_rect(bottomleft=(x + 8, y - 10 - height_padding))

        if last_text_rect.y <= self.chat_rect.y + 64:
            self.remove_used_text_from_chat()
        else:
            end_of_name = new_strings[0].find(":")
            last_element = 0
            for index, strings in reversed(list(enumerate(new_strings))):
                if index == last_element and end_of_name != -1:
                    text_surface_name = settings.font_chat.render(strings[:end_of_name], True, self.color_for_used_users[color_index])
                    text_rect_name = text_surface_name.get_rect(bottomleft=(x + 8, y - 10 - height_padding))

                    text_surface = settings.font_chat.render(strings[end_of_name:], True, (255, 255, 255))
                    text_rect = text_surface.get_rect(bottomleft=(text_rect_name.bottomright[0], y - 10 - height_padding))
                else:
                    text_surface = settings.font_chat.render(strings, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(bottomleft=(x + 8, y - 10 - height_padding))

                height_padding += font_height

                if text_rect.y > self.chat_rect.y + 64:
                    if index != last_element:
                        settings.screen.blit(text_surface, text_rect)
                    else:
                        settings.screen.blit(text_surface_name, text_rect_name)
                        settings.screen.blit(text_surface, text_rect)

        return height_padding
    
    def remove_used_text_from_chat(self):
        self.used_texts.pop(0)
        self.used_users.pop(0)
        self.color_for_used_users.pop(0)

    def random_color(self):
        r = random.randint(50, 255)
        g = random.randint(50, 255)
        b = random.randint(50, 255)

        return (r, g, b)

    def split_text(self, string_to_split, settings):
        split_text = string_to_split.split(" ")
        new_strings = []
        text = split_text[0]
        text_prev = text

        for string in split_text[1:]:
            text = text + " " + string
            text_width, _ = settings.font_chat.size(text)

            if text_width >= self.chat_rect.width - 8:
                new_strings.append(text_prev)
                text = string
                text_prev = text
            else:
                text_prev = text
        
        new_strings.append(text)

        return new_strings

    def select_text_to_show_on_chat(self):
        not_used_texts = list(set(self.texts)-set(self.used_texts))
        if len(not_used_texts) == 0:
            text = random.choice(self.texts)
            self.used_texts.append(text)
        else:
            text = random.choice(not_used_texts)
            self.used_texts.append(text)
        self.used_users.append(random.choice(self.users))
        self.color_for_used_users.append(self.random_color())
    
    def draw_chat(self, maps, settings):
        x, _ = maps.level_map_rect.midright
        x = x + (settings.screen_size[0] - x)/2
        y = settings.screen_size[1]/2
        chat_img = pygame.image.load(self.chats[0]).convert_alpha()
        self.chat_rect = chat_img.get_rect(center = (x, y))
        settings.screen.blit(chat_img, self.chat_rect)

    def draw_live_sign(self, settings):
        x, y = self.chat_rect.topright
        live_t_img = pygame.image.load(self.live_t[self.live_t_index]).convert_alpha()
        live_t_rect = live_t_img.get_rect(bottomright = (x, y - 20))
        settings.screen.blit(live_t_img, live_t_rect)
    
    def check_passed_time(self):
        current_time = pygame.time.get_ticks()
        time_difference_live_animation = current_time - self.time_since_live_animation
        time_difference_new_text = current_time - self.time_since_new_text

        if time_difference_live_animation >= 1000:
            if self.live_t_index == 1:
                self.live_t_index = 0
            else:
                self.live_t_index = 1

            self.time_since_live_animation = current_time
        
        if time_difference_new_text >= self.miliseconds_for_new_text:
            self.select_text_to_show_on_chat()
            self.miliseconds_for_new_text = random.randint(1, 2) * 1000
            self.time_since_new_text = current_time
        