import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, ai_settings, screen, alien):
        """Create a bullet object at the ship's current position"""
        super(AlienBullet, self).__init__()
        self.screen = screen

        #  Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.alien_bullet_width, ai_settings.alien_bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top

        #  Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.alien_bullets_color
        self.speed_factor = ai_settings.alien_bullet_speed_factor

    def update(self):
        """Move the bullet up the screen"""
        #  Update the decimal position of the bullet
        self.y += self.speed_factor
        #  Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
