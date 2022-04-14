import pygame as pg
import entity
import numpy as np


class Mob(entity.Entity):

    def __init__(self, model):
        """
        Constructs an instance of a mob. A mob is an entity that can have a gun and can die.

        Args:
             model (model.Model): Model of the game to which to instantiate the mob into.
        """
        super().__init__(model)

        self.gun = None
        self.aim_pos = np.array([0, 0])

        self.bullet_collision_mask = []

        self.health = 0

    def set_gun(self, gun_template):
        """
       Instantiates and sets the gun of this mob.

       Args:
            gun_template (class): Class of gun to instantiate for this mob.
       """
        self.gun = gun_template(self, self.model)

    def aim(self, pos):
        """
        Sets this mob's aim input to position.

        Args:
            pos (tuple): Position to aim at.
        """
        self.gun.set_aim(pos)

    def fire(self, mode):
        """
        Sets this mob's firing input.

        Args:
            mode (str): Mode to set firing input to.
        """
        self.gun.set_fire(mode)

    def take_damage(self, bullet):
        """
        Perform operations when this mob is hit by a bullet.

        Args:
            bullet (bullet.Bullet): Bullet this mob was hit by.
        """
        base_damage = bullet.damage
        self.health -= base_damage
        if self.health <= 0:
            self.model.remove_entity(self)

    def update_position(self, delta):
        """
        Updates the position of this mob.

        Args:
            delta (float): Time since last tick of the main game loop.
        """
        super().update_position(delta)
        if self.gun:
            self.gun.update(delta)
