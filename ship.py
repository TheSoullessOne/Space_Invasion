import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #  Load the image and get its rect.
        self.image = pygame.image.load('Images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #  Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #  Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        #  Movement flag
        self.moving_right = False
        self.moving_left = False

        self.alive = True
        self.frame_index = 0

        self.prep_ship_frames()

    def prep_ship_frames(self):
        self.explosion_frames = ['Images/Ship_Explosion_1.png', 'Images/Ship_Explosion_2.png',
                                 'Images/Ship_Explosion_3.png', 'Images/Ship_Explosion_4.png',
                                 'Images/Ship_Explosion_5.png', 'Images/Ship_Explosion_6.png',
                                 'Images/Ship_Explosion_7.png', 'Images/Ship_Explosion_8.png']

    def get_image_frames(self):
        self.img_frames = []
        self.img_frames_rect = []
        for i in self.explosion_frames:
            img = pygame.image.load(i)
            self.img_frames.append(img)
        # print(self.img_frames)
        return self.img_frames

    def update(self):
        """Update the ship's position based on movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        #  Update rect object from self.center
        self.rect.centerx = self.center

    def blit_me(self):
        """Draw the shop at its current location"""
        if self.alive:
            self.screen.blit(self.image, self.rect)
        elif self.frame_index < 8:
            self.image = pygame.image.load(self.explosion_frames[self.frame_index])
            self.screen.blit(self.image, self.rect)
            self.frame_index += 1
            print(self.frame_index)
            # pygame.time.delay(100)
        else:
            self.alive = True
            self.frame_index = 0
            self.image = pygame.image.load('Images/ship.bmp')

    def center_ship(self):
        self.center = self.screen_rect.centerx
