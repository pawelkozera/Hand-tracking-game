import random

class Level_events():
    def __init__(self):
        self.events_enabled = False
        self.y_position_for_animation = 0
        self.speed_of_increasing_y = 5
        self.curse_words = []
    
    def select_events_for_level(self, maps, physics, settings, streamer, chat):
        if maps.level == 0:
            self.level_0(streamer, chat)
        elif maps.level == 1:
            self.level_1(physics, maps, settings, streamer, chat)
        elif maps.level == 2:
            self.level_2(physics, maps, settings, streamer, chat)
        elif maps.level == 3:
            self.level_3(streamer, chat, maps)
    
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
            
            chat.texts = [""
                ]
            chat.users = ["dickster69"]

            self.events_enabled = True
        
        chat.miliseconds_for_new_text = 4000
        print(self.curse_words)
        if streamer.index_of_text < len(streamer.texts) - 1:
            maps.map_speed = 0
        else:
            maps.map_speed = 3

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