import pygame

class Player():
    def __init__(self, screen_size):
        self.border = 5
        self.color = "Black"
        self.controler_hand = False
        self.x_pos = int(screen_size[0]/2)
        self.y_pos = int(screen_size[1] - 100)
    
    def get_mouse_position(self):
        if not self.controler_hand:
            self.x_pos, self.y_pos = pygame.mouse.get_pos()
    
    def draw_player(self, screen):
        pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.border)
    
    def draw_hand_not_detected(self, settings):
        text_surface = settings.font.render("Hand not detected", False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(settings.screen_size[0]/2, settings.screen_size[1]/2))
        settings.screen.blit(text_surface, text_rect)

    def in_borders(self, maps, height):
        return self.x_pos - self.border > maps.level_map_rect.left and self.y_pos - self.border > 0 and self.y_pos + self.border < height and self.x_pos + self.border < maps.level_map_rect.right

    def check_for_collision(self, maps, settings):
        collision_positions = {
            'right': [self.x_pos + self.border, self.y_pos],
            'left': [self.x_pos - self.border, self.y_pos],
            'up': [self.x_pos, self.y_pos + self.border],
            'down': [self.x_pos, self.y_pos - self.border]
        }

        for position in collision_positions.values():
            color = settings.screen.get_at((position[0], position[1]))[:3]
            
            if color == maps.color_win:
                return 1
            elif color == maps.color_lose:
                return 2
            elif color == (0, 162, 232):
                return 3
            elif color == (255, 174, 201):
                return 4
            elif color == (239, 228, 176):
                return 5
        
        return 0
    
    def check_for_collision_with_rect(self, rect):
        if rect.collidepoint(self.x_pos, self.y_pos):
            return True
        return False