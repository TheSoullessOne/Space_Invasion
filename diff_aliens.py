from alien import Alien
from timer import Timer
import random
from time import sleep


class Alien1(Alien):
    def __init__(self, ai_settings, screen):
        super(Alien1, self).__init__(ai_settings, screen)

    def explode(self):
        pass

    def load_image(self):
        return 'Images/UFO.png'


class Alien2(Alien):
    def __init__(self, ai_settings, screen):
        super(Alien2, self).__init__(ai_settings, screen)

    def explode(self):
        pass

    def load_image(self):
        return 'Images/UFO_Big.png'


class Alien3(Alien):
    def __init__(self, ai_settings, screen):
        super(Alien3, self).__init__(ai_settings, screen)

    def explode(self):
        pass

    def load_image(self):
        return 'Images/UFO_Boss.png'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Alien4(Alien, metaclass=Singleton):
    def __init__(self, ai_settings, screen):
        super(Alien4, self).__init__(ai_settings, screen)
        print('made it here')
        self.get_starting_location()
        self.get_random_direction()
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def explode(self):
        pass

    def load_image(self):
        return 'Images/Random_Alien.png'

    def blit_me(self):
        self.screen.blit(self.image, self.rect)
        # print(self.rect)

    def get_starting_location(self):
        # if not self.ai_settings.rand_alien_alive:
        self.x = self.ai_settings.screen_width / 2
        self.y = self.ai_settings.screen_height / 2
        self.rect.x, self.rect.y = self.x, self.y

    def get_random_direction(self):
        dir_x = random.randint(0, 2)
        while dir_x == 0:
            dir_x = random.randint(0, 2)
        self.dir_x = dir_x

        dir_y = random.randint(0, 2)
        while dir_y == 0:
            dir_y = random.randint(0, 2)
        self.dir_y = dir_y

    def move(self):
        sw = self.ai_settings.screen_width
        sh = self.ai_settings.screen_height
        if self.rect.left < 0 or self.rect.right > sw:
            self.dir_x *= -1
        if self.rect.top < 0 or self.rect.bottom > sh:
            self.dir_y *= -1
        self.x += (self.dir_x * self.ai_settings.rand_alien_speed)
        self.y += (self.dir_y * self.ai_settings.rand_alien_speed)
        self.rect.x = self.x
        self.rect.y = self.y
