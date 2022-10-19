import pygame
import sys
import random
from words import *

pygame.init()

# Constants
info = pygame.display.Info()
# print(info.current_w, info.current_h)  ###### 1536 864 for laptop

WIDTH, HEIGHT = 890, 750 ####################################### changed from 1000 to 750

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.image.load("assets/Check Starting Tiles.png")
BACKGROUND = pygame.transform.smoothscale(BACKGROUND, (677/1.5, 580/1.5))  #### RESCALE EVERYTHING BY 1.5 TIMES
BACKGROUND_RECT = BACKGROUND.get_rect(center=(445, 265)) ##  356 to 265 i.e. difference of 91
ICON = pygame.image.load("assets/Icon.png")

pygame.display.set_caption("Wordle")
pygame.display.set_icon(ICON)

################
TOP = pygame.image.load('top.jpg')
TOP_RECT = TOP.get_rect(center=(445, 25))
RESTART = pygame.image.load('restart.jpg')
RESTART = pygame.transform.smoothscale(RESTART, (23, 23))
RESTART_RECT = RESTART.get_rect(center=(32, 25))
QUESTION = pygame.image.load('question.jpg')
QUESTION_RECT = QUESTION.get_rect(center=(WIDTH - 40, 25))

main_font = pygame.font.Font("assets/HelveticaLT63MediumExtendedOblique.ttf", 14)
# hint_text = main_font.render("Hint: that's what you have to say to me", True, "pink")
# hint_rect = hint_text.get_rect(center=(WIDTH-50, 980))

# pygame.draw.rect(SCREEN, "white", (10, 655, 1000, 600))
help_font = pygame.font.Font("assets/HelveticaLT63MediumExtendedOblique.ttf", 14)
# help_text = help_font.render('Help', True, "black")
# help_rect = help_text.get_rect(center=(WIDTH - 40, 20))
# pygame.draw.rect(SCREEN, "black", [WIDTH - 42, 22, 30, 20])
# pygame.display.update()
################

GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d8d4dc"
FILLED_OUTLINE = "#878a8c"

CORRECT_WORD = "iloveyou"

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 32)
AVAILABLE_LETTER_FONT = pygame.font.Font("assets/HelveticaLT63MediumExtended.ttf", 25)

SCREEN.fill("white")
SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
pygame.display.update()
SCREEN.blit(TOP, TOP_RECT)
pygame.display.update()
SCREEN.blit(RESTART, RESTART_RECT)
pygame.display.update()
# SCREEN.blit(hint_text, hint_rect)
# SCREEN.blit(help_text, help_rect)
SCREEN.blit(QUESTION, QUESTION_RECT)
pygame.display.update()

LETTER_X_SPACING = 56.7
LETTER_Y_SPACING = 72 + 26 ###############################
LETTER_SIZE = 50

# Global variables

guesses_count = 0

# guesses is a 2D list that will store guesses. A guess will be a list of letters.
# The list will be iterated through and each letter in each guess will be drawn on the screen.
guesses = [[]] * 6

current_guess = []
current_guess_string = ""
current_letter_bg_x = 222

# Indicators is a list storing all the Indicator object. An indicator is that button thing with all the letters you see.
indicators = []

game_result = ""

class Letter:
    def __init__(self, text, bg_position):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y - 26, LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x+24, self.bg_position[1]) ################
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(SCREEN, "black", self.bg_rect, 3)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(SCREEN, "white", self.bg_rect)
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 2)
        pygame.display.update()

class Indicator:
    def __init__(self, x, y, letter):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 50, 55)
        self.bg_color = OUTLINE

    def draw(self):
        # Puts the indicator and its text on the screen at the desired position.
        pygame.draw.rect(SCREEN, self.bg_color, self.rect, border_radius=8)
        pygame.draw.rect(SCREEN, "#BBBABC", self.rect, 3, border_radius=8)
        if self.bg_color == GREY:
            pygame.draw.rect(SCREEN, "#65696A", self.rect, 3, border_radius=8)
        if self.bg_color == YELLOW:
            pygame.draw.rect(SCREEN, "#AD9A4B", self.rect, 3, border_radius=8)
        if self.bg_color == GREEN:
            pygame.draw.rect(SCREEN, "#5C9756", self.rect, 3, border_radius=8)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "black")
        self.text_rect = self.text_surface.get_rect(center=(self.x+24, self.y+27))
        SCREEN.blit(self.text_surface, self.text_rect) ############## here
        pygame.display.update()

# Drawing the indicators on the screen.

indicator_x, indicator_y = 172, 500 #### 124 --> 172 = 48 of difference

for i in range(3):
    for letter in ALPHABET[i]:
        new_indicator = Indicator(indicator_x, indicator_y, letter)
        indicators.append(new_indicator)
        new_indicator.draw()
        indicator_x += 55
    indicator_y += 70
    if i == 0:
        indicator_x = 203
    elif i == 1:
        indicator_x = 258


def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result
    game_decided = False
    for i in range(8): #############################
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                guess_to_check[i].bg_color = GREEN
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = GREEN
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = YELLOW
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = YELLOW
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = GREY
            for indicator in indicators:
                if indicator.text == lowercase_letter.upper():
                    indicator.bg_color = GREY
                    indicator.draw()
            guess_to_check[i].text_color = "white"
            game_result = ""
            game_decided = True
        guess_to_check[i].draw()
        pygame.display.update()
    
    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = 222

    if guesses_count == 6 and game_result == "":
        game_result = "L"

def play_again():
    # Puts the play again text on the screen.
    pygame.draw.rect(SCREEN, "white", (10, 460, 1000, 600)) ## 655 --> 460 = 195 of difference
    play_again_font = pygame.font.Font("assets/HelveticaLT63MediumExtended.ttf", 36)

    if CORRECT_WORD == 'iloveyou':
        emoji_font = pygame.font.Font("assets/FreeSansBold.otf", 36)
        emoji_text = emoji_font.render('♥', True, "#CD79EA")
        emoji_rect = emoji_text.get_rect(center=(WIDTH - 180, 610))
        play_again_text = play_again_font.render("Happy Anniversary, bby", True, "black")
        play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 610))
        word_was_text = play_again_font.render(f"The correct answer was:", True, "black")
        word_was_rect = word_was_text.get_rect(center=(WIDTH / 2, 510))
        word_was_text_2 = play_again_font.render("i love you", True, "pink")
        word_was_rect_2 = word_was_text.get_rect(center=(WIDTH - 250, 560))
        SCREEN.blit(word_was_text, word_was_rect)
        SCREEN.blit(word_was_text_2, word_was_rect_2)
        SCREEN.blit(play_again_text, play_again_rect)
        SCREEN.blit(emoji_text, emoji_rect)
        pygame.display.update()
    else:
        word_was_text = play_again_font.render(f"The correct answer was:", True, "black")
        word_was_rect = word_was_text.get_rect(center=(WIDTH / 2, 510))
        word_was_text_2 = play_again_font.render(f"{CORRECT_WORD}", True, "black")
        word_was_rect_2 = word_was_text.get_rect(center=(WIDTH - 250, 560))
        SCREEN.blit(word_was_text, word_was_rect)
        SCREEN.blit(word_was_text_2, word_was_rect_2)
        pygame.display.update()

def reset():
    # Resets all global variables to their default states.
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result, current_letter_bg_x
    SCREEN.fill("white")
    SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
    SCREEN.blit(TOP, TOP_RECT)
    SCREEN.blit(RESTART, RESTART_RECT)
    SCREEN.blit(QUESTION, QUESTION_RECT)
    pygame.display.update()
    guesses_count = 0
    current_letter_bg_x = 222
    CORRECT_WORD = random.choice(WORDS)
    guesses = [[]] * 6
    current_guess = []
    current_guess_string = ""
    game_result = ""
    pygame.display.update()
    for indicator in indicators:
        indicator.bg_color = OUTLINE
        indicator.draw()

def create_new_letter():
    # Creates a new letter and adds it to the guess.
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count*67+LETTER_Y_SPACING)) ########################## here rect appear
    current_letter_bg_x += LETTER_X_SPACING
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()
            pygame.draw.rect(SCREEN, "white", (619, 1, 200, 50))
            pygame.display.update()

def delete_letter():
    # Deletes the last letter from the guess.
    global current_guess_string, current_letter_bg_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_bg_x -= LETTER_X_SPACING

while True:
    if game_result != "":
        play_again()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            rect = pygame.Rect(750, 20, 250, 50)
            if rect.collidepoint(mouse):
                pygame.draw.rect(SCREEN, "white", (619, 1, 200, 50))
                pygame.draw.rect(SCREEN, "black", (619, 1, 200, 50), 3)
                help_text = help_font.render("Hint: That's what you", True, "black")
                help_rect = help_text.get_rect(center=(717, 18))
                help_text_2 = help_font.render("have to say to me", True, "black")
                help_rect_2 = help_text.get_rect(center=(727, 32))
                SCREEN.blit(help_text, help_rect)
                SCREEN.blit(help_text_2, help_rect_2)
                pygame.display.update()

            else:
                pygame.draw.rect(SCREEN, "white", (619, 1, 200, 50))
                pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            rect_restart = pygame.Rect(10, 20, 250, 50)
            if rect_restart.collidepoint(mouse):
                reset()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    pygame.time.delay(300)
                    reset()
                else:
                    if len(current_guess_string) == 8 and current_guess_string.lower() in WORDS:
                        pygame.time.delay(200)
                        check_guess(current_guess)
            elif event.key == pygame.K_BACKSPACE:
                if len(current_guess_string) > 0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    if len(current_guess_string) < 8: #############################
                        create_new_letter()


