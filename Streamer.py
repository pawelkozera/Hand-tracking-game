import pygame

class Streamer():
    def __init__(self, name):
        self.image_text_bubble = pygame.image.load("imgs/text_bubble.png").convert_alpha()
        self.image_rect_text_bubble = self.image_text_bubble.get_rect(midtop = (0, 50))
        self.image = pygame.image.load("avatars/" + name + ".jpg").convert()
        self.image_rect = self.image.get_rect(midtop = (0, 50))
        self.texts = ["Hey guys!"]
    
    def render_streamer(self, screen, settings):
        self.image_rect = self.image.get_rect(center = (150, settings.screen_size[1]/2))
        screen.blit(self.image, self.image_rect)
    
    def render_dialogue(self, screen, settings, maps):
        text_surface = settings.font.render(self.texts[0], False, (255, 255, 255))
        text_rect = text_surface.get_rect(midleft=(int(self.image_rect.midtop[0]) + 10, int(self.image_rect.midright[1]) - self.image_rect.height))

        new_strings = self.split_dialogue(settings, maps)
        text_surfaces, text_rects = self.get_surfaces_and_rects(new_strings, settings)

        bubble_x = text_rect.width + 60
        bubble_y = text_rect.height * 3

        self.image_text_bubble = pygame.transform.scale(self.image_text_bubble, (bubble_x, bubble_y))
        self.image_rect_text_bubble = self.image_text_bubble.get_rect(center=(text_rect.centerx, text_rect.centery))

        #screen.blit(self.image_text_bubble, self.image_rect_text_bubble)
        for text_s, text_r in zip(text_surfaces, text_rects):
            screen.blit(text_s, text_r)
    
    def split_dialogue(self, settings, maps):
        split_text = self.texts[0].split(" ")
        new_strings = []
        text = ""
        text_prev = text

        for string in split_text:
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
            text_surfaces.append(settings.font.render(string, False, (255, 255, 255)))
            text_rects.append(text_surfaces[index].get_rect(midleft=(self.image_rect.midtop[0] + 10, self.image_rect.midright[1] - self.image_rect.height - height)))
            height -= 30

        return text_surfaces, text_rects
