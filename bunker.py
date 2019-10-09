import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position"""
        super(Bunker, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #  Load the image and get its rect.
        self.image = pygame.image.load('Images/Bunker_1.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #  Start each new ship at the bottom center of the screen
        self.rect.centerx = ai_settings.screen_width / 2
        self.rect.bottom = self.screen_rect.bottom - 75

        self.life = 0
        self.max_life = 4
        self.exists = False

        #  Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        self.prep_bunker_frames()

    def prep_bunker_frames(self):
        self.frames = ['Images/Bunker_1.png', 'Images/Bunker_2.png', 'Images/Bunker_3.png', 'Images/Bunker_4.png']

    def get_frame(self):
        return self.frames[self.life]

    def blit_me(self):
        """Draw the shop at its current location"""
        if self.life < self.max_life:
            self.image = pygame.image.load(self.get_frame())
            self.screen.blit(self.image, self.rect)
        print(self.rect.top)
