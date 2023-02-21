import pygame

class Mukbang():
    def __init__(self, screen_size, map_x_beginning):
        self.calories = 0
        self.donated_boxes = 0

        self.table_img = pygame.image.load("imgs/food/table.png").convert_alpha()
        self.table_rect = self.table_img.get_rect(midtop = (map_x_beginning + 400, int(screen_size[1]/2)))

        self.donation_box_img = pygame.image.load("imgs/food/donation_box.png").convert_alpha()
        left_mid_table_position = self.table_rect.midleft
        self.donation_box_rect = self.donation_box_img.get_rect(midright = left_mid_table_position)
        self.donation_box_rect.x -= 10

        self.current_face_index = 0
        self.animation_time_since_eaten = 0
        self.animation_time = 1000
        self.face_imgs = [
            pygame.image.load("imgs/food/face_closed.png").convert_alpha(),
            pygame.image.load("imgs/food/face_open.png").convert_alpha(),
        ]
        self.face_rects = []
        self.__add_face_rects()

        self.food_imgs = [
            pygame.image.load("imgs/food/burger.png").convert_alpha(),
            pygame.image.load("imgs/food/cupcake1.png").convert_alpha(),
            pygame.image.load("imgs/food/cupcake2.png").convert_alpha(),
            pygame.image.load("imgs/food/cake.png").convert_alpha(),
            pygame.image.load("imgs/food/icecream.png").convert_alpha(),
            pygame.image.load("imgs/food/taco.png").convert_alpha(),
            pygame.image.load("imgs/food/pizza.png").convert_alpha(),
        ]
        self.food_rects = []
        self.__add_food_rects()
        self.food_removed_indexes = []

        self.sound_eating = pygame.mixer.Sound("music/eating.wav")
    
    def __add_food_rects(self):
        move_closer_to_table_top = 20
        move_close_to_the_right_side = 30
        y = self.table_rect.y + move_closer_to_table_top
        x = self.table_rect.x + move_close_to_the_right_side

        for food_img in self.food_imgs:
            food_rect = food_img.get_rect(midbottom = (x, y))
            self.food_rects.append(food_rect)
            x += 50
    
    def __add_face_rects(self):
        x, y = self.table_rect.midright
        move_to_the_right = 30
        for face_img in self.face_imgs:
            face_rect = face_img.get_rect(midleft = (x + move_to_the_right, y))
            self.face_rects.append(face_rect)

    def draw_table(self, screen):
        screen.blit(self.table_img, self.table_rect)
    
    def draw_dontation_box(self, screen):
        screen.blit(self.donation_box_img, self.donation_box_rect)
    
    def draw_food(self, screen):
        for index, food_img in enumerate(self.food_imgs):
            if index not in self.food_removed_indexes:
                food_rect = self.food_rects[index]
                screen.blit(food_img, food_rect)
    
    def draw_face(self, screen):
        face_img = self.face_imgs[self.current_face_index]
        face_rect = self.face_rects[self.current_face_index]
        screen.blit(face_img, face_rect)

    def draw_calories(self, settings):
        x, y = settings.screen_size
        color = (0, 0, 0)
        calories = "Calories: " + str(self.calories)
        settings.draw_text(calories, x/2, y - 100, color)
    
    def draw_donated_boxes(self, settings):
        x, y = settings.screen_size
        color = (0, 0, 0)
        calories = "Donated food: " + str(self.donated_boxes)
        settings.draw_text(calories, x/2, y - 50, color)
    
    def draw_passage_to_next_level(self, color_win, screen):
        x, y = self.table_rect.midtop
        y -= 200
        pygame.draw.circle(screen, color_win, (x, y), 20)

    def drag_food(self, player, level_events):
        level_events.drag_rects(player, self.food_rects)
    
    def food_collision(self, index_of_the_last_dragged_rect_food):
        food_rect = self.food_rects[index_of_the_last_dragged_rect_food]
        dragged_food_collision_with_face = pygame.Rect.collidepoint(self.face_rects[0], food_rect.center)
        dragged_food_collision_with_donation_box = pygame.Rect.collidepoint(self.donation_box_rect, food_rect.center)

        if dragged_food_collision_with_face:
            self.calories += 500
            self.food_collision_hide_food_rect(index_of_the_last_dragged_rect_food, food_rect)
            self.animation_time_since_eaten = pygame.time.get_ticks()
            pygame.mixer.Sound.play(self.sound_eating)
        if dragged_food_collision_with_donation_box:
            self.donated_boxes += 1
            self.food_collision_hide_food_rect(index_of_the_last_dragged_rect_food, food_rect)
    
    def food_collision_hide_food_rect(self, index_of_the_food_to_hide, food_rect_to_hide):
        self.food_removed_indexes.append(index_of_the_food_to_hide)
        food_rect_to_hide.center = (0, 0)
    
    def calories_goal_is_completed(self):
        if self.calories >= 10000:
            return True
        return False
    
    def donated_boxes_goal_is_completed(self):
        if self.donated_boxes >= 21:
            return True
        return False
    
    def check_if_every_food_is_eaten_or_donated(self):
        removed_food_length = len(self.food_removed_indexes)
        food_length = len(self.food_rects)
        if removed_food_length >= food_length:
            return True
        return False
    
    def reset_food_position(self):
        move_closer_to_table_top = 20
        move_close_to_the_right_side = 30
        y = self.table_rect.y + move_closer_to_table_top
        x = self.table_rect.x + move_close_to_the_right_side
        
        for food_rect in self.food_rects:
            food_rect.midbottom = (x, y)
            x += 50
    
    def clear_removed_rects(self):
        self.food_removed_indexes.clear()
    
    def eating_face_animation(self):
        current_time = pygame.time.get_ticks()
        time_difference_eat_animation = current_time - self.animation_time_since_eaten

        if time_difference_eat_animation >= self.animation_time:
            self.current_face_index = 0
        else:
            self.current_face_index = 1
