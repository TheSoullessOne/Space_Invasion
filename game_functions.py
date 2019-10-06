import pygame
from bullet import Bullet
from diff_aliens import *
import sys
from text_box import TextBox
import random
from pygame.sprite import Group
from timer import Timer


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break
    random_alien = Alien4(ai_settings, screen)
    rand_collision = pygame.sprite.collide_rect(ship, random_alien)
    if rand_collision:
        ai_settings.rand_alien_alive = False
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_back_button(stats, back_button, mouse_x, mouse_y):
    button_clicked = back_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.high_score_active:
        stats.high_score_active = False


def check_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if ai_settings.rand_alien_alive:
        rand = Group()
        random_alien = Alien4(ai_settings, screen)
        rand.add(random_alien)
        rand_collision = pygame.sprite.groupcollide(bullets, rand, True, True)
        if rand_collision:
            stats.score += ai_settings.alien4_points
            sb.prep_score()
            check_high_score(stats, sb)
            ai_settings.rand_alien_alive = False
            score_text = TextBox(ai_settings, screen, stats)
            score_text.update_text(str(ai_settings.alien4_points))
            score_text.text_rect = random_alien.rect
            score_text.draw(screen)
            frames = [score_text, score_text, score_text, score_text, score_text]
            timer = Timer(frames)
    if collisions:
        for aliens in collisions.values():
            if "Alien1" in aliens.__str__():
                stats.score += ai_settings.alien1_points * len(aliens)
            elif "Alien2" in aliens.__str__():
                stats.score += ai_settings.alien2_points * len(aliens)
            elif "Alien3" in aliens.__str__():
                stats.score += ai_settings.alien3_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        #  Destroy existing bullets and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()

        #  Increase level
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def check_events(ai_settings, screen, stats, sb, play_button, high_score_button, quit_button, back_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb)
        elif event.type == pygame.KEYUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_keyup_events(event, ai_settings, screen, stats, sb,  play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            check_high_scores_button(ai_settings, screen, stats, high_score_button, mouse_x, mouse_y)
            check_quit_button(stats, quit_button, mouse_x, mouse_y)
            check_back_button(stats, back_button, mouse_x, mouse_y)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif pygame.key == pygame.K_ESCAPE or pygame.key == pygame.K_q:
        stats.set_high_score()
        sys.exit()


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_keyup_events(event, ai_settings, screen, stats, sb,  play_button, ship, aliens, bullets, mouse_x, mouse_y):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_ESCAPE:
        stats.set_high_score()
        sys.exit()
    elif (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN) and not stats.game_active:
        check_play_button(ai_settings, screen, stats, sb,  play_button, ship, aliens, bullets, mouse_x, mouse_y, True)
    elif event.key == pygame.K_BACKSPACE:
        text = stats.initials
        text = text[:-1]  # removes last letter
        stats.set_initials(text)
    elif stats.set_initials and event.key != pygame.K_SPACE and event.key != pygame.K_RSHIFT and event.key != \
            pygame.K_LSHIFT:
        text = stats.initials
        if len(text) < 3:
            text += str(chr(event.key)).upper()  # adds letter
            stats.set_initials(text)


def check_play_button(ai_settings, screen, stats, sb,  play_button, ship, aliens, bullets, mouse_x, mouse_y, enter=False):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if (button_clicked and not stats.game_active and stats.get_initials) or enter:
        #  Reset the game settings
        ai_settings.initialize_dynamic_settings()

        #  Hide the mouse cursor
        pygame.mouse.set_visible(False)

        #  Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        #   Reset the scorebaord images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #  Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #  Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    elif button_clicked and not stats.game_active and not stats.get_initials:
        stats.get_initials = True


def check_high_scores_button(ai_settings, screen, stats, high_score_button, mouse_x, mouse_y):
    button_clicked = high_score_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.high_score_active:
        stats.high_score_active = True
        show_high_scores()


def check_quit_button(stats, quit_button, mouse_x, mouse_y):
    button_clicked = quit_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.high_score_active:
        sys.exit()


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien1(ai_settings, screen)
    if row_number == 0:
        alien = Alien3(ai_settings, screen)
    elif row_number == 1:
        alien = Alien2(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    #  Create an alien and find the number of aliens in a row
    #  alien = Alien1(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, 60)  # alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, 58)  # alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached"""
    #  Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_user_input(text):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                text = text[:-1]  # removes last letter
            elif len(text) < 4:
                text += e.unicode  # adds letter


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    #  Need to pass in Timer class in here for 8 frames of animation of the crash

    #  Decrement ships_left
    if stats.ships_left > 0:
        stats.ships_left -= 1

        #  Update scoreboard
        sb.prep_ships()

        #  Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #  Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #  Pause
        sleep(0.5)
    else:
        stats.game_active = False
        # stats.set_high_score_active = True
        pygame.mouse.set_visible(True)

        #  Save new high score in a txt file
        stats.set_high_score()


def show_high_scores():

    print('test')


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Update the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets"""
    #  Update bullet positions.
    bullets.update()

    #  Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, high_score_button, quit_button,
                  back_button, start_button):
    """Update images on the screen and flip to the new screen"""
    if stats.game_active and not stats.high_score_active:
        screen.fill(ai_settings.bg_color)

        #  Redraw all bullets behind the ship and aliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blit_me()
        aliens.draw(screen)

        rand_num = random.randint(0, 7500)
        random_alien = Alien4(ai_settings, screen)
        if rand_num == 1 and not ai_settings.rand_alien_alive:
            print('Created Alien at ' + str(random_alien.rect))
            ai_settings.rand_alien_alive = True
        if ai_settings.rand_alien_alive:
            random_alien.move()
            random_alien.blit_me()

        #  Draw the score information
        sb.show_score(screen)

        #  Draw the play button if the game is inactive.
    elif stats.get_initials and not stats.game_active:
        screen.fill(ai_settings.bg_color)
        # grats_box = TextBox(ai_settings, screen, stats)
        # grats_box.update_text("Unfortunately, the aliens got you ")

        prompt_box = TextBox(ai_settings, screen, stats)
        prompt_box.update_text('Please Enter Your 3 Initials:')
        prompt_box.draw(screen)

        input_box = TextBox(ai_settings, screen, stats)
        string_for_input = str(stats.initials)
        input_box.update_text(string_for_input)

        input_box.text_rect.y += 50
        input_box.draw(screen)

        enter_box = TextBox(ai_settings, screen, stats)
        enter_box.update_text('Please Press enter to begin!')
        enter_box.text_rect.y += 100
        enter_box.draw(screen)

    elif not stats.game_active and not stats.high_score_active and not stats.get_initials:
        screen.fill(ai_settings.bg_color)

        game_title1 = TextBox(ai_settings, screen, stats)
        game_title1.update_text("Welcome to Space Invasion!")
        # game_title1.text_rect.y -= 50
        game_title1.update_font('arial', 100)
        game_title1.draw(screen)

        game_title2 = TextBox(ai_settings, screen, stats)
        game_title2.update_text("Can you fend off the aliens?!")
        game_title2.text_rect.y += 50
        game_title2.update_font('Times New Roman', 150)
        game_title2.draw(screen)

        play_button.draw_button()
        high_score_button.draw_button()
        quit_button.draw_button()

        #  Draw the high_score screen if button was clicked
    elif not stats.game_active and stats.high_score_active:
        screen.fill(ai_settings.bg_color)
        stats.show_high_scores(ai_settings, screen, stats)
        back_button.draw_button()

    #  Make the most recently drawn screen visible.
    pygame.display.flip()
