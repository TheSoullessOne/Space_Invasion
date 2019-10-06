import pygame


class TextBox:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #  Font for scoring information
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.text_size = 20
        self.text_limit = 3
        self.text = ''

        self.prep_text()

    def prep_text(self):
        self.text_image = self.font.render(self.text, True, self.text_color, self.ai_settings.bg_color)

        #  Display the score at the top right of the screen
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.screen_rect.center
        self.text_rect.top = self.screen_rect.top + 100

    def draw(self, screen):
        screen.blit(self.text_image, self.text_rect)

    def update_text(self, text):
        # if len(self.text) < self.text_limit:
        # print('Less than')
        self.text = text
        self.prep_text()

    def update_font(self, font_name, font_size):
        self.font = pygame.font.SysFont(font_name, font_size)
