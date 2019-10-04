import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    #  Initialize game, screen settings and screen project.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #  Make the buttons.
    play_button = Button(ai_settings, screen, "Play")
    high_score_button = Button(ai_settings, screen, "High Scores")
    quit_button = Button(ai_settings, screen, "Quit")
    back_button = Button(ai_settings, screen, "Back")
    high_score_button.rect.bottom = play_button.rect.bottom + 100
    high_score_button.msg_image_rect.center = high_score_button.rect.center
    quit_button.rect.bottom = screen.get_rect().bottom
    quit_button.rect.right = screen.get_rect().right
    quit_button.msg_image_rect.center = quit_button.rect.center
    back_button.rect.center = quit_button.rect.center
    back_button.msg_image_rect.center = back_button.rect.center

    #  Create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #  Make a ship.
    ship = Ship(ai_settings, screen)
    #  Make a group to store bullets in.
    bullets = Group()
    aliens = Group()

    #  Create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #  Start the main loop for the game
    while True:
        #  Watch for keyboard and mouse events.
        gf.check_events(ai_settings, screen, stats, sb, play_button, high_score_button, quit_button, back_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
        #  elif stats.high_score_active:
            #  gf.show_high_scores(ai_settings, screen, stats, quit_button)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, high_score_button,
                         quit_button, back_button)


run_game()
