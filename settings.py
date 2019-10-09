class Settings:
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        """Initialize the game's settings."""
        #  Screen Settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        #  Ship settings
        self.ship_limit = 3

        #  Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255
        self.bullets_allowed = 3

        #  Alien bullet settings
        self.alien_bullet_width = self.bullet_width
        self.alien_bullet_height = self.bullet_height
        self.alien_bullets_allowed = 2
        self.alien_bullets_color = self.bullet_color

        #  Alien Settings
        self.fleet_drop_speed = 10
        self.alien2_total_aliens = 0
        self.alien3_total_aliens = 0
        self.alien2_max_aliens = 10
        self.alien3_max_aliens = 5
        self.rand_alien_alive = False
        self.rand_alien_speed = 0.5

        #  How quickly the game speeds uo
        self.speedup_scale = 1.1

        #  how quickly the alien point value increase
        self.score_scale = 1.5

        #  Bunker settings
        self.number_of_bunkers = 5
        self.bunker_max_life = 5
        self.bunker_life = 0
        self.bullet_increase = False

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_bullet_speed_factor = 1
        self.alien_speed_factor = 5

        #  fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        #  Scoring
        self.alien1_points = 50
        self.alien2_points = 100
        self.alien3_points = 150
        self.alien4_points = 1000

        self.bunker_life = 0

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien1_points = int(self.alien1_points * self.score_scale)
        self.alien2_points = int(self.alien3_points * self.score_scale)
        self.alien3_points = int(self.alien3_points * self.score_scale)
        self.alien4_points = int(self.alien4_points * self.score_scale)
        if not self.bullet_increase:
            self.bullet_increase = not self.bullet_increase
            self.alien_bullets_allowed += 1

    def can_create_alien2(self):
        self.alien2_total_aliens += 1
        return self.alien2_total_aliens < self.alien2_max_aliens

    def can_create_alien3(self):
        self.alien3_total_aliens += 1
        return self.alien3_total_aliens < self.alien3_max_aliens
