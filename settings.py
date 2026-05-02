"""A class to store all settings for Alien Invasion."""
class Settings:
    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_limit = 3
        # Bullet settings
        self.bullet_width = 7
        self.bullet_height = 7
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 100
        self.shots_per_second = 5
        # Alien settings
        self.drop_speed = 10
        self.fleet_direction = 1  # 1 represents right; -1 represents left
        self.alien_density = 10 # 90% Aliens will be randomly removed from the fleet.
        # How quickly the game speeds up.
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 5
        self.bullet_speed = 12.0
        self.alien_speed = 5.0
        self.alien_points = 50
        self.shots_per_second = 5
        self.alien_density = 10
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.speedup_scale)
        self.shots_per_second *= self.speedup_scale
        self.alien_density *= self.speedup_scale