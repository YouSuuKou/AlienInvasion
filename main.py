import pygame
import sys
import random
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import time
import threading

def check_shooting(ai):
    """Check if the spacebar is being held down and fire bullets at a consistent rate."""
    while True:
        ai.is_in_shooting_interval = False
        time.sleep(0.5 / ai.settings.shots_per_second)  # Wait for the shooting interval
        ai.is_in_shooting_interval = True
        time.sleep(0.5 / ai.settings.shots_per_second)  # Wait for the shooting interval
class AlienInvasion:
    """Overall class to mage game assets and behavior."""
    def __init__(self):
        """
        Initialize the game and create game resources.
        """
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height


        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.fireing_bullets = False
        self.is_in_shooting_interval = False
        # Start the game in an active state.
        self.game_active = False

        # Create the Play button.
        self.play_button = Button(self, "Play")
    def run_game(self):
        while True:
            self._check_events()  # Check for events
            if self.stats.game_active:
                self.ship.update()  # Update the ship's position
                if self.fireing_bullets:
                    self._fire_bullet()  # Fire bullets if the spacebar is pressed
                self._update_bullets()  # Update the bullets' positions
                self._update_aliens()  # Update the aliens' positions
            self._update_screen()  # Update the screen
            self.clock.tick(60)  # Limit to 60 frames per second
    def _check_events(self):
            """Respond to keypresses and mouse events."""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d: # If the 'D' key is pressed, set the moving_right flag to True
                        self.ship.moving_right = True
                    elif event.key == pygame.K_a: # If the 'A' key is pressed, set the moving_left flag to True
                        self.ship.moving_left = True
                    elif event.key == pygame.K_LSHIFT: # If the left shift key is pressed, set the fast_moving flag to True     
                        self.ship.fast_moving = True
                    elif event.key == pygame.K_ESCAPE: # If the 'Escape' key is pressed, exit the game
                        sys.exit(0)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_d: # If the 'D' key is released, set the moving_right flag to False
                        self.ship.moving_right = False
                    elif event.key == pygame.K_a: # If the 'A' key is released, set the moving_left flag to False
                        self.ship.moving_left = False
                    elif event.key == pygame.K_LSHIFT: # If the left shift key is released, set the fast_moving flag to False   
                        self.ship.fast_moving = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.fireing_bullets = True
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.fireing_bullets = False
    def _check_play_button(self, mouse_pos):
            """Start a new game when the player clicks Play."""
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            if button_clicked and not self.stats.game_active:
                # Reset the game settings.
                # self.settings.initialize_dynamic_settings()
                # Reset the game statistics.
                self.stats.reset_stats()
                self.stats.game_active = True
                self.settings.initialize_dynamic_settings()
                # Get rid of any remaining aliens and bullets.
                self.aliens.empty()
                self.bullets.empty()
                # Create a new fleet and center the ship.
                self._create_fleet()
                self.ship.center_ship()
                pygame.mouse.set_visible(False)
                self.sb.prep_score()
                self.sb.prep_high_score()
                self.sb.prep_level()
                self.sb.prep_ships()
    def _fire_bullet(self):
            """Create a new bullet and add it to the bullets group."""
            if len(self.bullets) < self.settings.bullets_allowed and not self.is_in_shooting_interval:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
                self.is_in_shooting_interval = True
    def _update_bullets(self):
            """Update position of bullets and get rid of old bullets."""
            self.bullets.update()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
            """Respond to bullet-alien collisions."""
            # Remove any bullets and aliens that have collided.
            collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
            if collisions:
                for aliens in collisions.values():
                    self.stats.score += self.settings.alien_points * len(aliens)
                    self.sb.prep_score()
                    self.sb.check_high_score()
            if not self.aliens:
                # Destroy existing bullets and create new fleet.
                self.bullets.empty()
                self._create_fleet()
                self.settings.increase_speed()
                self.stats.level += 1
                self.sb.prep_level()
    def _check_aliens_bottom(self):
            """Check if any aliens have reached the bottom of the screen."""
            screen_rect = self.screen.get_rect()
            for alien in self.aliens.sprites():
                if alien.rect.bottom >= screen_rect.bottom:
                    # Treat this the same as if the ship got hit.
                    self._ship_hit()
                    break
    def _update_aliens(self):
            """Update the positions of all aliens in the fleet."""
            self.aliens.update()
            self._check_fleet_edges()

            # Look for alien-ship collisions.
            if pygame.sprite.spritecollideany(self.ship, self.aliens):
                self._ship_hit()

            # Look for aliens hitting the bottom of the screen.
            self._check_aliens_bottom()
    def _create_fleet(self):
            """Create the fleet of aliens."""
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            available_space_x = self.settings.screen_width - (2 * alien_width)
            number_aliens_x = available_space_x // (2 * alien_width)
            ship_height = self.ship.rect.height
            available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
            number_rows = available_space_y // (2 * alien_height)
            for row_number in range(number_rows):
                for alien_number in range(number_aliens_x):
                    if random.randint(1, 100) < self.settings.alien_density:
                        self._create_alien(alien_number, row_number)
    def _create_alien(self, alien_number, row_number):
            """Create an alien and place it in the row."""
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien_height + 2 * alien_height * row_number
            self.aliens.add(alien)
    def _check_fleet_edges(self):
            """Respond appropriately if any aliens have reached an edge."""
            for alien in self.aliens.sprites():
                if alien.check_edges():
                    self._change_fleet_direction()
                    break
    def _change_fleet_direction(self):
            """Drop the entire fleet and change the fleet's direction."""
            for alien in self.aliens.sprites():
                alien.rect.y += self.settings.drop_speed
            self.settings.fleet_direction *= -1
    def _ship_hit(self):
            """Respond to the ship being hit by an alien."""
            if self.stats.ships_left > 0:
                # Decrement ships_left, and update scoreboard.
                self.stats.ships_left -= 1
                self.sb.prep_ships()
                # Get rid of any remaining aliens and bullets.
                self.aliens.empty()
                self.bullets.empty()
                # Create a new fleet and center the ship.
                self._create_fleet()
                self.ship.rect.midbottom = self.screen.get_rect().midbottom
                # Pause.
                time.sleep(0.5)
            else:
                self.stats.game_active = False
                pygame.mouse.set_visible(True)
    def _update_screen(self):
            """Update images on the screen and flip to the new screen."""
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            # Draw the play button if the game is inactive.
            if not self.stats.game_active:
                self.play_button.draw_button()
            # Draw the score information.
            self.sb.show_score()
            pygame.display.flip()
if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    shooting_thread = threading.Thread(target=check_shooting, args=(ai,))
    shooting_thread.daemon = True
    shooting_thread.start()
    ai.run_game()