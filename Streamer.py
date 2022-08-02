import pygame

class Streamer():
    def __init__(self, name):
        self.image_text_bubble = pygame.image.load("imgs/text_bubble.png").convert_alpha()
        self.image_rect_text_bubble = self.image_text_bubble.get_rect(midtop = (0, 50))
        self.image = pygame.image.load("avatars/" + name + ".jpg").convert()
        self.image_rect = self.image.get_rect(midtop = (0, 50))
        self.tip_of_bubble_triangle = (0, 0)
        self.texts = ["Lorem ipsum dolor sit, onsequat Lorem ipsum dolor sit amet, it erat ac tellus consequat"]
    
    def render_streamer(self, screen):
        x, y = self.tip_of_bubble_triangle
        padding = 10
        self.image_rect = self.image.get_rect(midtop = (x, y + padding))
        screen.blit(self.image, self.image_rect)
    
    def render_dialogue(self, screen, settings, maps):
        new_strings = self.split_dialogue(settings, maps)
        text_surfaces, text_rects = self.get_surfaces_and_rects(new_strings, settings)

        bubble_width, bubble_height = self.calculate_size_of_bubble(text_rects)
        index_of_widest_text_rect = self.calculate_width_and_index_of_widest_rect(text_rects)[1]

        half_of_text = int(len(text_rects)/2)
        self.image_text_bubble = pygame.transform.scale(self.image_text_bubble, (bubble_width, bubble_height))
        self.image_rect_text_bubble = self.image_text_bubble.get_rect(center=(text_rects[index_of_widest_text_rect].centerx, text_rects[half_of_text].centery))

        self.draw_triangle_under_bubble(self.image_rect_text_bubble.midbottom[0], self.image_rect_text_bubble.midbottom[1], screen)
        screen.blit(self.image_text_bubble, self.image_rect_text_bubble)
        for text_s, text_r in zip(text_surfaces, text_rects):
            screen.blit(text_s, text_r)

    def split_dialogue(self, settings, maps):
        split_text = self.texts[0].split(" ")
        new_strings = []
        text = split_text[0]
        text_prev = text

        for string in split_text[1:]:
            text = text + " " + string
            text_surface = settings.font.render(text, False, (255, 255, 255))
            text_rect = text_surface.get_rect(midleft=(0, 0))

            if text_rect.topright[0] >= maps.level_map_rect.x:
                new_strings.append(text_prev)
                text = string
                text_prev = text
            else:
                text_prev = text
        
        new_strings.append(text)

        return new_strings
    
    def get_surfaces_and_rects(self, new_strings, settings):
        text_surfaces = []
        text_rects = []
        height = 30 * len(new_strings)
        for index, string in enumerate(new_strings):
            text_surfaces.append(settings.font.render(string, False, (0, 0, 0)))
            text_rects.append(text_surfaces[index].get_rect(midleft = (100, settings.screen_size[1]/2 - height)))
            height -= 30

        return text_surfaces, text_rects
    
    def calculate_size_of_bubble(self, text_rects):
        padding = 30
        ascept_ratio = self.image_rect_text_bubble.height / self.image_rect_text_bubble.width
        width = self.calculate_width_and_index_of_widest_rect(text_rects)[0] + padding * len(text_rects)
        height = width * ascept_ratio

        return (width, height)

    def calculate_width_and_index_of_widest_rect(self, text_rects):
        max_width = 0
        index = 0
        for number, rect in enumerate(text_rects):
            if rect.width > max_width:
                max_width = rect.width
                index = number
        
        return (max_width, index)

    def draw_triangle_under_bubble(self, bubble_width, bubble_height, screen):
        bubble_height = bubble_height - 50
        padding = 100
        first_point_x = bubble_width + padding
        first_point_y = bubble_height
        second_point_x = bubble_width - padding
        second_point_y = bubble_height
        third_point_x = bubble_width
        third_point_y = bubble_height + padding

        pygame.draw.polygon(screen, (255, 255, 255), ((first_point_x, first_point_y), (second_point_x, second_point_y), (third_point_x, third_point_y)))
        self.tip_of_bubble_triangle = (third_point_x, third_point_y)