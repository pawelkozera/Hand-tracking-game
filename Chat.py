import pygame
from random import randint, choice
from collections import deque

class Chat():
    def __init__(self):
        self.users = ["Max"]
        self.texts = ["asd", "123", "345"]
        self.used_texts = deque()
        self.used_users = deque()
        self.color_for_used_users = deque()
        self.users_in_chat = 147295
        self.users_division = [147105, 147895]
        
        self.chats = [pygame.image.load("chat/chat_t.png").convert_alpha()]
        self.chat_rect = None
        self.live_t = [pygame.image.load("chat/live_t1.png").convert_alpha(), pygame.image.load("chat/live_t2.png").convert_alpha()]
        self.live_t_index = 0

        self.image_view_box = pygame.image.load("chat/view_box.png").convert_alpha()
        self.image_view_box_rect = self.image_view_box.get_rect(center = (0, 0))
        self.image_view_eye = pygame.image.load("chat/view_eye.png").convert_alpha()
        self.image_view_eye_rect = self.image_view_eye.get_rect(center = (0, 0))

        self.time_since_live_animation = 0
        self.time_since_new_text = 0
        self.time_since_viewers_update = 0
        self.miliseconds_for_new_text = 1000

    def draw_view_box(self, screen):
        x, y = self.chat_rect.midbottom
        padding = 20
        self.image_view_box_rect = self.image_view_box.get_rect(midtop = (x, y + padding))
        screen.blit(self.image_view_box, self.image_view_box_rect)
    
    def draw_number_of_viewers(self, settings):
        number_of_viewers = self.add_comma_to_viewers_number()
        x, y = self.image_view_box_rect.center
        number_of_viewers_rect = settings.draw_text(number_of_viewers, x, y, (255, 255, 255))

        x, y = number_of_viewers_rect.midleft
        padding = 10
        self.image_view_eye_rect = self.image_view_eye.get_rect(midright = (x - padding, y))
        settings.screen.blit(self.image_view_eye, self.image_view_eye_rect)
    
    def add_comma_to_viewers_number(self):
        number_of_viewers = str(self.users_in_chat)
        new_string = ""
        count_numbers = 0

        for number in reversed(number_of_viewers):
            if count_numbers == 3:
                new_string += ","
                count_numbers = 0
            new_string += number
            count_numbers += 1

        return new_string[::-1]

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
        self.used_texts.popleft()
        self.used_users.popleft()
        self.color_for_used_users.popleft()

    def random_color(self):
        r = randint(50, 255)
        g = randint(50, 255)
        b = randint(50, 255)

        return (r, g, b)

    def split_text(self, string_to_split, settings):
        split_text = string_to_split.split(" ")
        new_strings = []
        text = split_text[0]
        text_prev = text

        for string in split_text[1:]:
            text = text + " " + string
            text_width, _ = settings.font_chat.size(text)

            if text_width >= self.chat_rect.width - 14:
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
            text = choice(self.texts)
            self.used_texts.append(text)
        else:
            text = choice(not_used_texts)
            self.used_texts.append(text)
        self.used_users.append(choice(self.users))
        self.color_for_used_users.append(self.random_color())
    
    def draw_chat(self, maps, settings):
        x, _ = maps.level_map_rect.midright
        x = x + (settings.screen_size[0] - x)/2
        y = settings.screen_size[1]/2
        self.chat_rect = self.chats[0].get_rect(center = (x, y))
        settings.screen.blit(self.chats[0], self.chat_rect)

    def draw_live_sign(self, settings):
        x, y = self.chat_rect.topright
        live_t_rect = self.live_t[self.live_t_index].get_rect(bottomright = (x, y - 20))
        settings.screen.blit(self.live_t[self.live_t_index], live_t_rect)
    
    def change_number_of_users_in_chat(self, new_number_of_users):
        self.users_in_chat = new_number_of_users
        min = new_number_of_users - randint(1, int(new_number_of_users/8))
        max = new_number_of_users + randint(1, int(new_number_of_users/8))
        self.users_division[0] = min
        self.users_division[1] = max
    
    def load_chat_users_from_file(self, how_many_to_load = None):
        self.users.clear()
        with open("chat/nicknames.txt", "r") as file:
            lines = (line for line in file)
            if how_many_to_load is None:
                for user in lines:
                    self.users.append(user.strip())
            else:
                for index, user in enumerate(lines):
                    if index >= how_many_to_load:
                        break
                    self.users.append(user.strip())
    
    def load_texts_from_file(self, how_many_to_load = None):
        self.texts.clear()
        with open("chat/texts.txt", "r") as file:
            lines = (line for line in file)
            if how_many_to_load is None:
                for text in lines:
                    self.texts.append(text.strip())
            else:
                for index, text in enumerate(lines):
                    if index >= how_many_to_load:
                        break
                    self.texts.append(text.strip())

    def check_passed_time(self):
        current_time = pygame.time.get_ticks()
        time_difference_live_animation = current_time - self.time_since_live_animation
        time_difference_new_text = current_time - self.time_since_new_text
        time_difference_viewers_update = current_time - self.time_since_viewers_update

        if time_difference_live_animation >= 1000:
            if self.live_t_index == 1:
                self.live_t_index = 0
            else:
                self.live_t_index = 1

            self.time_since_live_animation = current_time
        
        if time_difference_viewers_update >= 2000:
            min, max = self.users_division
            self.users_in_chat = randint(min, max)
            self.time_since_viewers_update = current_time
        
        if len(self.texts) > 0:
            if time_difference_new_text >= self.miliseconds_for_new_text:
                self.select_text_to_show_on_chat()
                self.miliseconds_for_new_text = randint(1, 2) * 1000
                self.time_since_new_text = current_time
        