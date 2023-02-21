import pygame

class Stamp():
    def __init__(self, map_x_beginning, screen_height):
        self.stamp_left_img = pygame.image.load("imgs/stamps/stamp.png").convert_alpha()
        self.stamp_left_rect = self.stamp_left_img.get_rect(midleft = (map_x_beginning + 50, 200))
        self.stamp_right_img = pygame.image.load("imgs/stamps/stamp.png").convert_alpha()
        self.stamp_right_rect = self.stamp_left_img.get_rect(midleft = (map_x_beginning + 500, 200))
        self.stamp_rect_padding = 24
        self.__scale_down_stamps()

        self.stamp_approved = pygame.image.load("imgs/stamps/approved.png").convert_alpha()
        self.stamp_scam = pygame.image.load("imgs/stamps/scam.png").convert_alpha()
        self.stamped_on_contract = [] #[index_of_contract, is_stamp_approved, x_draw_start, y_draw_start, x_crop_stample, y_crop_stample, width_crop_stample, height_crop_stample]

        self.contract_imgs = [ #maybe use 2d array to check if it's scam or not [[img, false], [img, true], [img, false]...]
            pygame.image.load("imgs/stamps/contract1.png").convert_alpha(),
            pygame.image.load("imgs/stamps/contract2.png").convert_alpha()
        ]
        self.contract_rects = []
        self.__add_contract_rects(map_x_beginning, screen_height)

        self.user_choice_contracts = [None] * len(self.contract_rects) # True = scam, False = approved

        self.sound_stamp = pygame.mixer.Sound("music/stamp.wav")
    
    def __add_contract_rects(self, map_x_beginning, screen_height):
        x = map_x_beginning + 20
        for contract_img in self.contract_imgs:
            contract_rect = contract_img.get_rect(bottomleft = (x, screen_height - 20))
            self.contract_rects.append(contract_rect)
    
    def __scale_down_stamps(self):
        stamp_left_position = self.stamp_left_rect.center
        self.stamp_left_rect.width -= self.stamp_rect_padding
        self.stamp_left_rect.height -= self.stamp_rect_padding
        self.stamp_left_rect.center = stamp_left_position

        stamp_right_position = self.stamp_right_rect.center
        self.stamp_right_rect.width -= self.stamp_rect_padding
        self.stamp_right_rect.height -= self.stamp_rect_padding
        self.stamp_right_rect.center = stamp_right_position

    def draw_stamps(self, screen):
        stamp_left_center = (int(self.stamp_left_rect.x - self.stamp_rect_padding/2), int(self.stamp_left_rect.y - self.stamp_rect_padding/2))
        screen.blit(self.stamp_left_img, stamp_left_center)
        stamp_right_center = (int(self.stamp_right_rect.x - self.stamp_rect_padding/2), int(self.stamp_right_rect.y - self.stamp_rect_padding/2))
        screen.blit(self.stamp_right_img, stamp_right_center)
    
    def draw_contracts(self, screen):
        contract_imgs_len = len(self.contract_imgs) - 1
        for index, contract_img in enumerate(reversed(self.contract_imgs)):
            contract_index = contract_imgs_len - index
            contract_rect = self.contract_rects[contract_index]
            screen.blit(contract_img, contract_rect)
    
    def draw_stamps_on_contract(self, index_of_current_dragged_contract):
        contract_img = self.contract_imgs[index_of_current_dragged_contract]
        
        for stamped in self.stamped_on_contract:
            index_of_contract, stamp_approved, x_draw_start, y_draw_start, x_crop_stample, y_crop_stample, width_crop_stample, height_crop_stample = stamped
            if index_of_contract == index_of_current_dragged_contract:
                if stamp_approved:
                    contract_img.blit(self.stamp_approved, (x_draw_start, y_draw_start), (x_crop_stample, y_crop_stample, width_crop_stample, height_crop_stample))
                else:
                    contract_img.blit(self.stamp_scam, (x_draw_start, y_draw_start), (x_crop_stample, y_crop_stample, width_crop_stample, height_crop_stample))
    
    def draw_signs_for_stamps(self, settings):
        move_up = 40
        aprroved_sign_position_x, sign_position_y = self.stamp_left_rect.midtop
        settings.draw_text("Accept", aprroved_sign_position_x, sign_position_y - move_up, (72, 187, 98))
        rejected_sign_position_x = self.stamp_right_rect.midtop[0]
        settings.draw_text("Reject", rejected_sign_position_x, sign_position_y - move_up, (221, 51, 51))
    
    def drag_contract(self, player, level_events):
        level_events.drag_rects(player, self.contract_rects, "midbottom")
    
    def draw_passage_to_next_level(self, color_win, screen):
        x = int((self.stamp_left_rect.x + self.stamp_left_rect.width + self.stamp_right_rect.x)/2)
        y = self.stamp_left_rect.y - 50
        pygame.draw.circle(screen, color_win, (x, y), 20)
    
    def contract_collision_with_stamples(self, player, events, index_of_current_dragged_contract):
        if self.contract_collision_with_left_stample():
            if self.stample_left_clicked(player, events):
                self.change_user_choice_on_contracts(False, index_of_current_dragged_contract)
                self.add_stample_on_contract(True, index_of_current_dragged_contract)
        if self.contract_collision_with_right_stample():
            if self.stample_right_clicked(player, events):
                self.change_user_choice_on_contracts(True, index_of_current_dragged_contract)
                self.add_stample_on_contract(False, index_of_current_dragged_contract)
    
    def contract_collision_with_left_stample(self):
        for contract_rect in self.contract_rects:
            if pygame.Rect.colliderect(self.stamp_left_rect, contract_rect):
                return True
        return False
    
    def contract_collision_with_right_stample(self):
        for contract_rect in self.contract_rects:
            if pygame.Rect.colliderect(self.stamp_right_rect, contract_rect):
                return True
        return False
    
    def stample_left_clicked(self, player, events):
        LEFT_BUTTON = 1
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_BUTTON or keys[pygame.K_SPACE]:
                collision_left_stamp_with_player = pygame.Rect.collidepoint(self.stamp_left_rect, (player.x_pos, player.y_pos))
                if collision_left_stamp_with_player:
                    return True
        return False
    
    def stample_right_clicked(self, player, events):
        LEFT_BUTTON = 1
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_BUTTON or keys[pygame.K_SPACE]:
                collision_right_stamp_with_player = pygame.Rect.collidepoint(self.stamp_right_rect, (player.x_pos, player.y_pos))
                if collision_right_stamp_with_player:
                    return True
        return False
    
    def change_user_choice_on_contracts(self, is_scam, index_of_current_dragged_contract):
        if is_scam:
            self.user_choice_contracts[index_of_current_dragged_contract] = True
        else:
            self.user_choice_contracts[index_of_current_dragged_contract] = False
    
    def add_stample_on_contract(self, is_it_left_stample, index_of_current_dragged_contract):
        pygame.mixer.Sound.play(self.sound_stamp)

        if is_it_left_stample:
            x_stample = self.stamp_left_rect.x
            y_stample = self.stamp_left_rect.y
            is_stamp_approved = True
        else:
            x_stample = self.stamp_right_rect.x
            y_stample = self.stamp_right_rect.y
            is_stamp_approved = False

        width_stample = self.stamp_left_rect.width
        height_stample = self.stamp_left_rect.height
        x_contract = self.contract_rects[index_of_current_dragged_contract].x
        y_contract = self.contract_rects[index_of_current_dragged_contract].y

        x_draw_start = self.calculate_pos_draw_start(x_stample, x_contract)
        y_draw_start = self.calculate_pos_draw_start(y_stample, y_contract)
        x_crop_stample = self.calculate_pos_crop(x_stample, x_contract)
        y_crop_stample = self.calculate_pos_crop(y_stample, y_contract)

        self.stamped_on_contract.append([index_of_current_dragged_contract, is_stamp_approved, x_draw_start, y_draw_start, x_crop_stample, y_crop_stample, width_stample, height_stample])
    
    def calculate_pos_draw_start(self, pos_stample, pos_contract):
        if pos_stample <= pos_contract:
            return 0
        return pos_stample - pos_contract
    
    def calculate_pos_crop(self, pos_stample, pos_contract):
        if pos_stample <= pos_contract:
            return pos_contract - pos_stample
        return 0

    def player_collision_with_stample(self, player):
        collision_with_left_stamp = pygame.Rect.collidepoint(self.stamp_left_rect, (player.x_pos, player.y_pos))
        collision_with_right_stamp = pygame.Rect.collidepoint(self.stamp_right_rect, (player.x_pos, player.y_pos)) 
        if collision_with_left_stamp or collision_with_right_stamp:
            return True
        return False
    
    def check_if_player_stamped_all_contracts(self):
        for choice in self.user_choice_contracts:
            if choice == None:
                return False
        return True