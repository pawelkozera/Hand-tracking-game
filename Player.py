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
    
    def draw_hand_not_detected(self, settings, screen):
        text_surface = settings.font.render("Hand not detected", False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(settings.screen_size[0]/2, settings.screen_size[1]/2))
        screen.blit(text_surface, text_rect)

    def in_borders(self, maps, height):
        return self.x_pos - self.border > maps.level_map_rect.left and self.y_pos - self.border > 0 and self.y_pos + self.border < height and self.x_pos + self.border < maps.level_map_rect.right

    def check_for_collision(self, maps, screen, screen_size):
        collision_positions = {
            'right': [self.x_pos + self.border, self.y_pos],
            'left': [self.x_pos - self.border, self.y_pos],
            'up': [self.x_pos, self.y_pos + self.border],
            'down': [self.x_pos, self.y_pos - self.border]
        }

        collided = False
        for position in collision_positions.values():
            color = screen.get_at((position[0], position[1]))[:3]
            
            if color == maps.color_win and not collided:
                collided = True
                maps.next_map_after_win(screen_size)
            if color == maps.color_lose:
                maps.same_map_after_lose(screen_size)
        