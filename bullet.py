import pygame
from pygame.sprite import Sprite
import numpy as np # for physics calculations

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    def __init__(self, ai_game, target):
        """
        Create a bullet object at the ship's current position.
        :param ai_game: The instance of the main game class, used to access game resources.
        :param target: The target position (x, y) that the bullet should move towards.
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
        self.target = target
        self.velocity =  (0, -self.settings.bullet_speed)
    def get_velocity(self):
        """Calculate the velocity of the bullet based on its speed."""
        if self.target:
            direction = np.array(self.target.rect.center) - np.array(self.rect.center)
            delta_v = self.settings.bullet_speed * direction / np.linalg.norm(direction)
            temp = self.velocity + delta_v
            if np.linalg.norm(temp) < np.linalg.norm(self.velocity): # If the angle of the velocity is more than 120 degrees, lose the target.
                self.target = None
            else: # Otherwise, update the velocity to move towards the target.
                self.velocity = temp  / np.linalg.norm(temp) * self.settings.bullet_speed
    def update(self):
        """Move the bullet up the screen."""
        self.get_velocity()
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)