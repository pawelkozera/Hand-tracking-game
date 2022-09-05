import pygame

class Clothes():
    def __init__(self, maps):
        self.budget = 0
        self.clothes_images = []
        self.clothes_image_rect = []

        self.__load_clothes_img()
        self.__add_clothes_rects(maps)
    
    def __load_clothes_img(self):
        self.clothes_images = [
                (pygame.image.load("imgs/clothes/pants1.png").convert_alpha(), 45),
                (pygame.image.load("imgs/clothes/pants2.png").convert_alpha(), 10),
                (pygame.image.load("imgs/clothes/boots1.png").convert_alpha(), 48),
                (pygame.image.load("imgs/clothes/boots2.png").convert_alpha(), 10),
                (pygame.image.load("imgs/clothes/tshirt1.png").convert_alpha(), 69),
                (pygame.image.load("imgs/clothes/tshirt2.png").convert_alpha(), 10),
                (pygame.image.load("imgs/clothes/chain.png").convert_alpha(), 400),
                (pygame.image.load("imgs/clothes/sunglasses.png").convert_alpha(), 20),
                (pygame.image.load("imgs/clothes/watch.png").convert_alpha(), 399),
            ]

    def __add_clothes_rects(self, maps):
        x = maps.level_map_rect.x + 610
        y = maps.level_map_rect.y

        for image in self.clothes_images:
            self.clothes_image_rect.append(image[0].get_rect(topright = (x, y)))
            if x >= maps.level_map_rect.x + 800:
                x = maps.level_map_rect.x + 610
                y += 120
            else:
                x += 190
    
    def reset_clothes_position(self, maps):
        x = maps.level_map_rect.x + 610
        y = maps.level_map_rect.y

        for clothes_rect in self.clothes_image_rect:
            clothes_rect.topright = (x, y)
            if x >= maps.level_map_rect.x + 800:
                x = maps.level_map_rect.x + 610
                y += 120
            else:
                x += 190
    
    def draw_clothes(self, screen):
        for index, img in enumerate(self.clothes_images):
            screen.blit(img[0], self.clothes_image_rect[index])
    
    def drag_clothes(self, player, level_events):
        level_events.drag_rects(player, self.clothes_image_rect)
    
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
    
    def check_for_adding_viewers(self, chat, budget):
        if self.budget != budget:
            self.budget = budget
            if budget <= -100 and budget > -140:
                chat.change_number_of_users_in_chat(60)
                chat.load_chat_users_from_file(60)
            elif budget <= -140 and budget > -600:
                chat.change_number_of_users_in_chat(110)
                chat.load_chat_users_from_file(60)
            elif budget <= -600:
                chat.change_number_of_users_in_chat(180)
                chat.load_chat_users_from_file(60)
            else:
                chat.change_number_of_users_in_chat(30)
                chat.load_chat_users_from_file(15)
    
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