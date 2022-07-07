import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__
        self.border = 4
        self.color = "Black"
        self.controler_hand = True
        self.x_pos = 300
        self.y_pos = 300
    
    def draw_player(self, screen):
        if not self.controler_hand:
            self.x_pos, self.y_pos = pygame.mouse.get_pos()

        pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.border)
    
    def check_for_collision(self, maps, width, height, screen):
        in_borders = self.x_pos - self.border > maps.level_map_rect.left and self.y_pos - self.border > 0 and self.y_pos + self.border < height and self.x_pos + self.border < maps.level_map_rect.right

        if in_borders:
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
        else:
            print("Poza")