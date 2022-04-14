from copy import copy
from random import uniform
import numpy as np
from . import bullet


class Gun:

    def __init__(self, owner, model):
        """
        Constructs an instance of a gun.

        Args:
            owner (entity.Mob): Entity that has a gun.
            model (model.Model): Model of the game to which to instantiate the bullet into.
        """
        self.owner = owner
        self.model = model

        self.position = np.array([1, 1], dtype=np.float64)
        self.aim_direction = 0.0

        self.fire_input = "NONE"
        self.aim_input = np.array([1, 1], dtype=np.float64)
        self.state = "IDLE"

        self.bullet = None

        self.timer_reload = 0.0
        self.timer_fire = 0.0

        self.primary_bullet = bullet.Bullet(model)
        self.primary_bullet.collision_mask = owner.bullet_collision_mask
        self.secondary_bullet = None

    def set_fire(self, mode):
        """
        Sets the firing input of this gun.

        Args:
            mode (str): Mode to set this gun to.
        """
        self.fire_input = mode

    def set_aim(self, pos):
        """
        Sets the aim input of this gun.

        Args:
            pos (tuple): Position to aim this gun at.
        """
        self.aim_input = np.array(pos, dtype=np.float64)

    def update(self, delta):
        """
        Updates this gun. Moves it to its owner's position, firing logic.

        Args:
            delta (float): Time since last tick of the main game loop.
        """
        self.position = self.owner.position
        vector = self.aim_input - self.position

        self.aim_direction = np.arctan2(vector[1], vector[0])

        if self.state == "RELOAD":
            if self.timer_reload > 0:
                self.timer_reload -= delta
            else:
                self.timer_reload = self.reload_time
                self.state = "IDLE"
        elif self.fire_input == "PRIMARY":
            if self.timer_fire > 0:
                self.timer_fire -= delta
            else:
                self.timer_fire = self.fire_time
                self.fire_primary(self.aim_direction)

    def fire_primary(self, direction):
        """
        Invokes this gun's primary fire.

        Args:
            direction (float): Direction to fire at.
        """
        new_bullet = copy(self.primary_bullet)
        offset = np.array([np.cos(direction), np.sin(direction)]) * 48
        new_bullet.set_position(self.position + offset)
        dispersion = uniform(-.5, .5) * self.primary_bullet_dispersion
        new_bullet.move(direction + dispersion, new_bullet.speed)
        new_bullet.rotate(direction)
        self.model.add_entity(new_bullet)

    def cool_down(self):
        """
        Called when this gun is idle.
        """
        pass


class GunFlieger(Gun):

    def __init__(self, owner, model):
        super().__init__(owner, model)

        self.primary_bullet.damage = 7
        self.primary_bullet.speed = .55

        self.primary_bullet.image = model.assets.images['bullet_small_a']

        self.primary_bullet_count = 1
        self.primary_spread_pattern = None
        self.primary_bullet_dispersion = 0.07

        self.reload_time = 2000
        self.fire_time = 120

    def __str__(self):
        return "XM17 Flieger"


class GunCroombaPistol(Gun):

    def __init__(self, owner, model):
        super().__init__(owner, model)

        self.primary_bullet.damage = 10
        self.primary_bullet.speed = .25

        self.primary_bullet.image = model.assets.images['bullet_small_a']

        self.primary_bullet_count = 1
        self.primary_spread_pattern = None
        self.primary_bullet_dispersion = 0.07

        self.reload_time = 2000
        self.fire_time = 800

    def __str__(self):
        return "Croomba Pistol"
