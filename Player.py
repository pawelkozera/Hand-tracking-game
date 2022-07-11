import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_size):
        super().__init__
        self.border = 4
        self.color = "Black"
        self.controler_hand = True
        self.x_pos = int(screen_size[0]/2)
        self.y_pos = int(screen_size[1] - 100)
    
    def get_mouse_position(self):
        if not self.controler_hand:
            self.x_pos, self.y_pos = pygame.mouse.get_pos()
    
    def draw_player(self, screen):
        pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.border)
    
    def draw_hand_not_detected(self, settings, screen, screen_size):
        text_surface = settings.font.render("Hand not detected", False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_size[0]/2, screen_size[1]/2))
        screen.blit(text_surface, text_rect)

    def in_borders(self, maps, height):
        return self.x_pos - self.border > maps.level_map_rect.left and self.y_pos - self.border > 0 and self.y_pos + self.border < height and self.x_pos + self.border < maps.level_map_rect.right

    def check_for_collision(self, maps, screen):
        collision_positions = {
            'right': [self.x_pos + self.border, self.y_pos],
            'left': [self.x_pos - self.border, self.y_pos],
            'up': [self.x_pos, self.y_pos + self.border],
            'down': [self.x_pos, self.y_pos - self.border]
        }

        for position in collision_positions.values():
            if screen.get_at((position[0], position[1]))[:3] == maps.color_win:
                print("win")
            if screen.get_at((position[0], position[1]))[:3] == maps.color_lose:
                print("lose")
        