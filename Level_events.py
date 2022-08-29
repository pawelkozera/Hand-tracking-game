import pygame
import random
import math

class Level_events():
    def __init__(self):
        self.events_enabled = False
        self.ending_check_points = [False, False]
        self.y_position_for_animation = 0
        self.speed_of_increasing_y = 5
        self.curse_words = []
        self.budget = 40

        self.list_of_events = []
        self.lmp_pressed = False
        self.moving_points_lines = [] # [x_start, y_start, x_end, y_end, width]
        self.moving_points_circle_radius = [] # [x, y, r, angle, width]
        self.moving_points_rects = [] # [x_start, y_start, x_end, y_end, x_left_border, x_right_border, flag_is_moving_left]

        self.clothes_images = []
        self.clothes_image_rect = []
        self.index_of_drag_rect = 0
    
    def select_events_for_level(self, maps, physics, settings, streamer, chat, player):
        if maps.level == 0:
            self.level_0(streamer, chat)
        elif maps.level == 1:
            self.level_1(physics, maps, settings, streamer, chat)
        elif maps.level == 2:
            self.level_2(physics, maps, settings, streamer, chat)
        elif maps.level == 3:
            self.level_3(streamer, chat, maps)
        elif maps.level == 4:
            self.level_4(streamer, chat, maps, settings)
        elif maps.level == 5:
            self.level_5(streamer, chat, maps, settings, player)
    
    def level_0(self, streamer, chat):
        if not self.events_enabled:
            streamer.texts = [
                    "Hello, my name is Jerry The Instructor.", 
                    "I'm gonna teach you how to be successful streamer.",
                    "Listen to me and in the meantime just solve the puzzles I created.",
                    "I gave all 20% of my creativity to create them."
                    ]

            chat.texts = [
                "Ehh another InFlUeNcEr",
                "message deleted by a moderator",
                "message deleted by a moderator",
                "Hello!!!!",
                "Hi!",
                "Hi!!!",
                "Hi!!",
                "Hi jerry",
                "Hi jerry",
                "Hi Jerry",
                "Hi jerry!!",
                "Hi jerry!",
                "<3 <3 <3 <3 <3 <3 <3 <3 <3",
                "My wife cheated on me",
                "lets' goooooooooo chat",
                "Lorem ipsum!",
                "You can do it newbie!",
                "Hi newbie",
                "Hi newbie!",
                "Hi noobie!!",
                "Hello new streamerrrr",
            ]

            self.events_enabled = True

    def level_1(self, physics, maps, settings, streamer, chat):
        if not self.events_enabled:
            streamer.texts = [
                    "No matter what your skills are, you always start with 0 viewers in the beginning.",
                    ]
            
            chat.texts = []
            chat.users = []
            chat.used_users = []
            chat.used_texts = []

            self.events_enabled = True
            self.y_position_for_animation = -400

            physics.create_static_wall(settings, maps.level_map_rect.x + 200)
            physics.create_static_wall(settings, maps.level_map_rect.topright[0] - 200)
            self.create_static_balls(40, maps, physics)
            self.create_falling_balls(120, physics, maps)
        
            chat.users_in_chat = 1
            chat.users_division = (1, 1)
        physics.remove_unused_objects(settings.screen_size[1])
        physics.draw_ball(settings, maps.color_lose)
        physics.draw_static_ball(settings, maps.color_lose, self.y_position_for_animation)
        self.y_position_for_animation += self.speed_of_increasing_y
    
    def level_2(self, physics, maps, settings, streamer, chat):
        if not self.events_enabled:
            streamer.texts = [
                    "Sometimes it will take a while, but eventually a random guy will show up.",
                    "I think I spawned too many balls.",
                    "Welp you gonna figure this out."
                    ]
            
            chat.texts = ["What's uppppppppppp",
                "My boyfriend gay can't think straight",
                "i have 99 problems but a beach ain't one",
                "Where there's a stream, there's watchers...",
                "I think i have hemorrhoids",
                "let's gooooooo",
                "lol",
                "Yeeeeeeees",
                "noo",
                "How did it go so wrong",
                "That's a hard lvl!",
                "xDD", "xD", "xd", "XDDDD",
                "where do you live?",
                "what's your age?",
                "how much money do you make?",
                "may i be racist in the chat?",
                "omg"
                ]
            chat.users = ["dickster69"]

            self.events_enabled = True
            self.y_position_for_animation = -400

            chat.users_in_chat = 1
            chat.users_division = (1, 1)
            physics.create_static_wall(settings, maps.level_map_rect.x + 200)
            physics.create_static_wall(settings, maps.level_map_rect.topright[0] - 200)
            self.create_static_balls(40, maps, physics, radious = 10)
            self.create_falling_balls(400, physics, maps)
        
        chat.miliseconds_for_new_text = 4000
        physics.remove_unused_objects(settings.screen_size[1])
        physics.draw_ball(settings, maps.color_lose)
        physics.draw_static_ball(settings, (0, 0, 255), radius = 1)
        self.y_position_for_animation += self.speed_of_increasing_y

    def level_3(self, streamer, chat, maps):
        if not self.events_enabled:
            streamer.texts = [
                    "The best way to gain viewers is to have unique personality.",
                    "Okay, pretend to have Tourette's syndrome.",
                    "People with Tourette's subclass have n-word pass even as white.",
                    "Pick the best curse combo."
                    ]
            
            chat.texts = ["What's uppppppppppp",
                "My boyfriend gay can't think straight",
                "i have 99 problems but a beach ain't one",
                "Where there's a stream, there's watchers...",
                "I think i have hemorrhoids",
                "let's gooooooo",
                "lol",
                "Yeeeeeeees",
                "noo",
                "How did it go so wrong",
                "That's a hard lvl!",
                "xDD", "xD", "xd", "XDDDD",
                "where do you live?",
                "what's your age?",
                "how much money do you make?",
                "may i be racist in the chat?",
                "omg"
                ]
            chat.users = ["dickster69"]

            self.events_enabled = True
        
        chat.users_in_chat = 1
        chat.users_division = (1, 1)
        chat.miliseconds_for_new_text = 4000
        if streamer.index_of_text < len(streamer.texts) - 1:
            maps.map_speed = 0
        else:
            maps.map_speed = 3

    def level_4(self, streamer, chat, maps, settings):
        if not self.events_enabled:
            chat.users_in_chat = 1
            curse_string = "\"You are "
            if len(self.curse_words) == 3:
                curse_string += " ".join(self.curse_words)
                curse_string += "\""
                if self.curse_words[0] in ["fucking", "garbage"]:
                    chat.users_in_chat += 23
                if self.curse_words[1] in ["ugly", "humpbacked"]:
                    chat.users_in_chat += 11
                if self.curse_words[2] in ["bastard", "fucker"]:
                    chat.users_in_chat += 17
                if self.curse_words[1] == "handsome":
                    chat.users_in_chat = 1

            chat.users_division = (chat.users_in_chat, chat.users_in_chat + 5)

            if chat.users_in_chat >= 40:
                how_well_player_did = "Pretty good for the first time. You should consider taking Tourette's subclass."
            elif chat.users_in_chat < 40 and chat.users_in_chat > 12:
                how_well_player_did = "You should practice a little, but I can see the potential."
            else:
                how_well_player_did = "Okay, maybe that's not for you."
                self.ending_check_points[0] = True

            streamer.texts = [
                    curse_string,
                    how_well_player_did,
                    "About 68% of influencers lie to their viewers.",
                    "Source? I made it up."
                    ]
            
            chat.texts = ["What's uppppppppppp",
                "My boyfriend gay can't think straight",
                "i have 99 problems but a beach ain't one",
                "Where there's a stream, there's watchers...",
                "I think i have hemorrhoids",
                "let's gooooooo",
                "lol",
                "Yeeeeeeees",
                "noo",
                "How did it go so wrong",
                "That's a hard lvl!",
                "xDD", "xD", "xd", "XDDDD",
                "where do you live?",
                "what's your age?",
                "how much money do you make?",
                "may i be racist in the chat?",
                "omg"
                ]
            chat.users = ["dickster69", "ralph", "max", "tobby", "robert", "master21", "cornelius"]

            y = self.calculate_y_position_on_map(4054, maps, settings)
            x = maps.level_map_rect.x + 316
            angle = 0
            self.moving_points_circle_radius.append([x, y, 89, angle, 5])

            y = self.calculate_y_position_on_map(3740, maps, settings)
            x = maps.level_map_rect.x + 346

            for i in range(5):
                y -= 178
                angle += 10
                self.moving_points_circle_radius.append([x, y, 89, angle, 5])
                self.moving_points_circle_radius.append([x, y, 89, angle + 180, 5])
            y -= 100
            for i in range(5):
                y -= 89
                angle += 10
                self.moving_points_circle_radius.append([x, y, 89, angle, 5])
                self.moving_points_circle_radius.append([x, y, 89, angle + 180, 5])
            
            y -= 100
            x = maps.level_map_rect.x + 218
            for i in range(20):
                self.moving_points_rects.append([x + random.randint(0, 200), y, 40, 20, x + 40, maps.level_map_rect.x + 434, False])
                y -= 60

            self.events_enabled = True
            self.list_of_events = [False]
        
        chat.miliseconds_for_new_text = 4000
        if self.list_of_events[0]:
            self.draw_lines(settings.screen)
        
        self.draw_rotating_lines(settings.screen, speed = 3)
        self.draw_moving_sideways_rects(settings.screen, speed = 0)
        self.move_down_drawn_objects(maps)
    
    def level_5(self, streamer, chat, maps, settings, player):
        if not self.events_enabled:
            streamer.texts = [
                ""
            ]
            
            self.load_clothes_img(maps)
            self.list_of_events = [False]

            self.events_enabled = True
        
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            self.drag_clothes(player)
        else:
            self.list_of_events[0] = False
        x = maps.level_map_rect.x
        y = maps.level_map_rect.y
        buy_zone_rect = pygame.draw.rect(settings.screen, (0, 0, 0), (x, y, 400, 800), 1)
        budget = self.add_up_clothes_price_in_buy_zone(buy_zone_rect)

        if self.budget != budget:
            self.budget = budget
            if budget <= -100 and budget > -140:
                chat.change_number_of_users_in_chat(60)
            elif budget <= -140 and budget > -540:
                chat.change_number_of_users_in_chat(110)
            elif budget <= -600:
                chat.change_number_of_users_in_chat(180)
            else:
                chat.change_number_of_users_in_chat(30)

        self.ending_check_points[1] = True if budget > 0 else False
        
        if self.check_if_dressed(buy_zone_rect):
            pygame.draw.circle(settings.screen, maps.color_win, (x + 350, y + 30), 25)

        self.draw_clothes(settings.screen)
        self.draw_budget(budget, settings, x, y)

    def collision_handler(self, collision, maps, player):
        if maps.level == 3:
            self.collision_with_words(collision, maps, player)
        elif maps.level == 4:
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0] and not self.list_of_events[0]:
                self.moving_points_lines.append([player.x_pos, player.y_pos, player.x_pos, player.y_pos - 500, 40])
                self.list_of_events[0] = True

    def calculate_y_position_on_map(self, y, maps, settings):
        screen_height = maps.level_map_rect.y - settings.screen_size[1]
        y = y + screen_height

        return y + settings.screen_size[1]
    
    def load_clothes_img(self, maps):
        self.clothes_images = [
                (pygame.image.load("imgs/pants1.png").convert_alpha(), 45),
                (pygame.image.load("imgs/pants2.png").convert_alpha(), 10),
                (pygame.image.load("imgs/boots1.png").convert_alpha(), 48),
                (pygame.image.load("imgs/boots2.png").convert_alpha(), 10),
                (pygame.image.load("imgs/tshirt1.png").convert_alpha(), 69),
                (pygame.image.load("imgs/tshirt2.png").convert_alpha(), 10),
                (pygame.image.load("imgs/chain.png").convert_alpha(), 400),
                (pygame.image.load("imgs/sunglasses.png").convert_alpha(), 20),
                (pygame.image.load("imgs/watch.png").convert_alpha(), 399),
            ]

        x = maps.level_map_rect.x + 610
        y = maps.level_map_rect.y

        for image in self.clothes_images:
            self.clothes_image_rect.append(image[0].get_rect(topright = (x, y)))
            if x >= maps.level_map_rect.x + 800:
                x = maps.level_map_rect.x + 610
                y += 120
            else:
                x += 190
    
    def draw_clothes(self, screen):
        for index, img in enumerate(self.clothes_images):
            screen.blit(img[0], self.clothes_image_rect[index])
    
    def drag_clothes(self, player):
        if not self.list_of_events[0]:
            for index, rect in enumerate(self.clothes_image_rect):
                if player.check_for_collision_with_rect(rect):
                    rect.center = (player.x_pos, player.y_pos)
                    self.list_of_events[0] = True
                    self.index_of_drag_rect = index
                    break
        else:
            self.clothes_image_rect[self.index_of_drag_rect].center = (player.x_pos, player.y_pos)
    
    def draw_budget(self, budget, settings, x, y):
        settings.draw_text("Budget:", x + 200, y + 100, (0, 0, 0))
        if budget > 0:
            color = (31, 163, 70)
        else:
            color = (183, 32, 11)
        settings.draw_text(str(budget) + "$", x + 200, y + 150, color)
    
    def add_up_clothes_price_in_buy_zone(self, buy_zone_rect):
        budget = 40
        for index, rect in enumerate(self.clothes_image_rect):
            if buy_zone_rect.colliderect(rect):
                budget -= self.clothes_images[index][1]
        
        return budget
    
    def check_if_dressed(self, buy_zone_rect):
        cloth_indexes = []
        for index, rect in enumerate(self.clothes_image_rect):
            if buy_zone_rect.colliderect(rect):
                cloth_indexes.append(index)
        
        pants_ids = [0, 1]
        boots_ids = [2, 3]
        tshirt_ids = [4, 5]

        wears_pants = any(index in cloth_indexes for index in pants_ids)
        wears_boots = any(index in cloth_indexes for index in boots_ids)
        wears_tshirt = any(index in cloth_indexes for index in tshirt_ids)

        if wears_pants and wears_boots and wears_tshirt:
            return True

        return False

    def draw_moving_sideways_rects(self, screen, speed = 3, color = (214, 85, 37)):
        for points in self.moving_points_rects:
            if speed == 0:
                speed = random.randint(3, 6)
            x_start, y_start, width, height, x_left_border, x_right_border, move_left = points

            if x_start >= x_right_border:
                points[6] = True
            elif x_start + width <= x_left_border:
                points[6] = False
            if move_left:
                points[0] -= speed
            else:
                points[0] += speed
            
            pygame.draw.rect(screen, color, pygame.Rect(x_start, y_start, width, height))

    def draw_rotating_lines(self, screen, speed = 1, color = (214, 85, 37)):
        for points in self.moving_points_circle_radius:
            x_center, y_center, radius, angle, width = points
            x = int(radius * math.sin(math.pi * 2 * angle / 360))
            y = int(radius * math.cos(math.pi * 2 * angle / 360))
            points[3] += speed
            if angle >= 360:
                points[3] = 0
            pygame.draw.line(screen, color, (x_center, y_center), (x_center + x, y_center + y), width)

    def draw_lines(self, screen, color = (255, 255, 255)):
        for points in self.moving_points_lines:
            x_start, y_start, x_end, y_end, width = points
            pygame.draw.line(screen, color, (x_start, y_start), (x_end, y_end), width)
    
    def move_down_drawn_objects(self, maps):
        for points in self.moving_points_lines:
            points[1] += maps.map_speed
            points[3] += maps.map_speed
        
        for points in self.moving_points_circle_radius:
            points[1] += maps.map_speed
        
        for points in self.moving_points_rects:
            points[1] += maps.map_speed

    def create_falling_balls(self, how_many, physics, maps, radious = 5):
        for n in range(how_many):
            physics.create_ball(maps.level_map_rect.x + random.randint(200, 600), maps.level_map_rect.y + random.randint(100, 600), radious)
    
    def create_static_balls(self, how_many, maps, physics, radious = 10):
        x, y = maps.level_map_rect.x + random.randint(210, 240), 200
        for n in range(how_many):
            if x >= maps.level_map_rect.topright[0] - 220:
                x = maps.level_map_rect.x + random.randint(210, 240)
                y += 40
            physics.create_static_ball(x, y, radious)
            x += random.randint(30, 60)
    
    def collision_with_words(self, collision_color_index, maps, player):
        def add_word_to_curse_words(word, word_index):
            if len(self.curse_words) >= word_index + 1:
                self.curse_words[word_index] = word
            else:
                self.curse_words.append(word)

        first_sector = player.x_pos <= maps.level_map_rect.x + 274
        second_sector = player.x_pos > maps.level_map_rect.x + 274 and player.x_pos <= maps.level_map_rect.x + 476
        third_sector = player.x_pos > maps.level_map_rect.x + 476
        
        if collision_color_index == 3:
            if first_sector:
                add_word_to_curse_words("fucking", 0)
            elif second_sector:
                add_word_to_curse_words("nice", 0)
            elif third_sector:
                add_word_to_curse_words("garbage", 0)

        elif collision_color_index == 4:
            if first_sector:
                add_word_to_curse_words("handsome", 1)
            elif second_sector:
                add_word_to_curse_words("ugly", 1)
            elif third_sector:
                add_word_to_curse_words("humpbacked", 1)

        elif collision_color_index == 5:
            if first_sector:
                add_word_to_curse_words("bastard", 2)
            elif second_sector:
                add_word_to_curse_words("guy", 2)
            elif third_sector:
                add_word_to_curse_words("fucker", 2)
    
    def reset(self):
        self.events_enabled = False
        self.list_of_events.clear()
        self.moving_points_circle_radius.clear()
        self.moving_points_lines.clear()
        self.moving_points_rects.clear()
        self.clothes_images.clear()
        self.clothes_image_rect.clear()