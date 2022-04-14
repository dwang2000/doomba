import pygame as pg
from . import entity


class Bullet(entity.Entity):

    def __init__(self, model):
        """
        Constructs an instance of a bullet.

        Attributes:
            -damage (int): Damage this bullet does to entities.

        Args:
             model (model.Model): Model of the game to which to instantiate the bullet into.
        """
        self.base_image = model.assets.images['bullet_small_a']
        super().__init__(model)
        self.model = model

        self.damage = 10
        self.speed = 0
        self.timer_despawn = 3000
        self.fired = False

    def move(self, direction, speed):
        """
        Accelerates this bullet in a given direction at a given speed.

        Args:
            direction (float): Direction to move towards in radians.
            speed (float): Speed at which to accelerate at.
        """
        super().move(direction, speed)
        self.fired = True

    def update(self, delta, model):
        """
        Updates this bullet.

        Args:
            delta (float): Time since last tick of the main game loop.
            model (model.Model): Reference to model of the game.
        """
        super().update(delta, model)
        if self.fired:
            if self.timer_despawn > 0:
                self.timer_despawn -= delta
            else:
                self.model.remove_entity(self)

    def collide_with(self, other):
        """
        Destroys this bullet and deals damage to entity when colliding.

        Args:
            other (entity.Entity): The entity to collide with.
        """
        if isinstance(other, pg.Rect):
            pass
        else:
            other.take_damage(self)
        self.model.remove_entity(self)

    def __copy__(self):
        """
        Makes a copy of this bullet.

        Returns:
            new_bullet (bullet.Bullet): Copy of this bullet.
        """
        new_bullet = Bullet(self.model)

        new_bullet.position = self.position

        new_bullet.damage = self.damage
        new_bullet.speed = self.speed

        new_bullet.image = self.image

        new_bullet.collision_mask = self.collision_mask

        return new_bullet
