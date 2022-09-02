import pygame
from random import randint

class Keyboard():
    def __init__(self, screen_size, map_x_beginning):
        self.letters = (
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M'
        )
        self.letters_rects = []
        self.__add_letters_rects(screen_size, map_x_beginning)
        self.colors_for_pressed_letters = {12: (72, 187, 98), 8: (72, 187, 98)}

        self.current_displayed_question = 0
        self.questions = (
                "Human best friend?",
                "A person who is not strong, brave, or confident?", 
                "Should we get a license for this ______?",
                "An ______ stream helps keep your viewers active and engaged.",
                "Encouraging people to like, buy, use, do or support something?",
                "Acting or done in the same way over time, means that someone is being?",
                "The situation of two or more people working together to create or achieve the same thing?"
            )
        self.correct_answers = ("DOG", "WIMP", "DIGGER", "INTERACTIVE", "PROMOTE", "CONSISTENT", "COLLABORATION")
        self.user_chosen_letters = "DO"
    
    def __add_letters_rects(self, screen_size, map_x_beginning):
        self.letters_rects.clear()
        start_x_padding = 25
        x_start = map_x_beginning + start_x_padding
        y_start = screen_size[1] - 300

        for index, _ in enumerate(self.letters):
            letter_rect = pygame.Rect(0, 0, 50, 50)
            letter_rect.midleft = (x_start, y_start)
            self.letters_rects.append(letter_rect)
            
            x_start += 75
            if index == 9 or index == 18:
                start_x_padding += 25
                x_start = map_x_beginning + start_x_padding
                y_start += 75
    
    def draw_keyboard(self, settings):
        for index, letter in enumerate(self.letters):
            if index in self.colors_for_pressed_letters.keys():
                color = self.colors_for_pressed_letters[index]
                self.draw_letter(settings, index, letter, letter_rect_color = color)
            else:
                self.draw_letter(settings, index, letter)
    
    def draw_letter(self, settings, index, letter, letter_rect_color = (189, 164, 109), letter_color = (255, 255, 255)):
        letter_rect = self.letters_rects[index]
        x, y = letter_rect.center
        pygame.draw.rect(settings.screen, letter_rect_color, letter_rect)
        settings.draw_text(letter, x, y, letter_color)
    
    def collision_with_letter(self, settings, x_pos, y_pos):
        for index, rect in enumerate(self.letters_rects):
            if pygame.Rect.collidepoint(rect, (x_pos, y_pos)):
                if index not in self.colors_for_pressed_letters.keys():
                    self.letter_hovered(index, settings)
                if self.check_if_letter_pressed_using_mouse(settings):
                    self.add_letter_to_user_chosen_letters(index)
    
    def letter_hovered(self, index, settings):
        letter = self.letters[index]
        self.draw_letter(settings, index, letter, letter_rect_color=(173, 142, 78))
    
    def check_if_letter_pressed_using_mouse(self, settings):
        for event in settings.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        return False
    
    def check_if_letter_pressed_using_keyboard(self, settings):
        for event in settings.events:
            if event.type == pygame.KEYDOWN:
                ascii_code_for_a = ord('a')
                ascii_code_for_z = ord('z')
                if event.key >= ascii_code_for_a and event.key <= ascii_code_for_z:
                    letter = event.unicode
                    letter_index = self.letters.index(letter.upper())
                    self.add_letter_to_user_chosen_letters(letter_index)
    
    def add_letter_to_user_chosen_letters(self, index):
        letter = self.letters[index]
        if letter not in self.user_chosen_letters:
            self.user_chosen_letters += letter
            answer = self.correct_answers[self.current_displayed_question]
            if letter in answer:
                self.colors_for_pressed_letters[index] = (72, 187, 98)
            else:
                self.colors_for_pressed_letters[index] = (221, 51, 51)
    
    def draw_current_question(self, settings, maps, chat):
        x = maps.level_map_rect.x + 400
        y = 125
        current_question = self.questions[self.current_displayed_question]
        current_question_splited = chat.split_text(current_question, settings.font, 760)
        for question in current_question_splited: 
            settings.draw_text(question, x, y)
            y += 40
    
    def draw_answer_space(self, settings, maps):
        x = maps.level_map_rect.x + 400
        y = 270
        correct_answer = self.correct_answers[self.current_displayed_question]
        current_answer = ""

        for char in correct_answer:
            if char in self.user_chosen_letters:
                current_answer += " " + char + " "
            else:
                current_answer += " __ "
        
        settings.draw_text(current_answer, x, y)

    def check_if_answer_is_complete(self):
        index_of_current_correct_answer = self.current_displayed_question
        for letter in self.correct_answers[index_of_current_correct_answer]:
            if letter not in self.user_chosen_letters:
                return False
        return True
    
    def next_question(self):
        self.current_displayed_question += 1
        self.user_chosen_letters = ""
        self.colors_for_pressed_letters.clear()
        self.reveal_random_letter()
    
    def check_if_its_last_question(self):
        last_question_index = len(self.questions) - 1
        if self.current_displayed_question < last_question_index:
            return False
        return True
    
    def reveal_random_letter(self):
        if self.current_displayed_question == 1:
            self.user_chosen_letters += "IMP"
            self.color_revealed_random_letters("IMP")
        elif self.current_displayed_question == 2:
            self.user_chosen_letters += "IGGER"
            self.color_revealed_random_letters("IGGER")
        else:
            current_answer_index = self.current_displayed_question
            correct_answer = self.correct_answers[current_answer_index]
            last_index_of_char = len(correct_answer) - 1
            random_char_index = randint(0, last_index_of_char)
            random_letter = correct_answer[random_char_index]
            self.user_chosen_letters += random_letter
            index_of_random_letter = self.letters.index(random_letter)
            self.colors_for_pressed_letters[index_of_random_letter] = (72, 187, 98)
    
    def color_revealed_random_letters(self, letters):
        for letter in letters:
            index = self.letters.index(letter)
            self.colors_for_pressed_letters[index] = (72, 187, 98)
