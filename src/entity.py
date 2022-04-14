import pygame as pg
import numpy as np


class Entity(pg.sprite.Sprite):

    def __init__(self, model):
        """
        Constructs an instance of an entity. An entity is something that can move, can be
        drawn, and can be collided with.

        Attributes:
            - model (model.Model): Reference to the model of the game.
            - image (pygame.Surface): Rendered image of this entity.
            - rect (pygame.Rect): Collision box of this entity.
            - position (numpy.ndarray): Position of this entity.
            - velocity (numpy.ndarray): Velocity of this entity.
            - speed (float): Speed at which this entity will accelerate when moving.
            - collision_layer (int): Collision layer that this entity belongs to.
            - collision_mask (list): List of indices of collision layers that this entity collides with.

        Args:
             model (model.Model): Model of the game to which to instantiate the entity into.
        """
        pg.sprite.Sprite.__init__(self)
        self.model = model

        self.image = self.base_image
        self.rect = self.image.get_rect()

        self.position = np.array([0, 0])
        self.velocity = np.array([0, 0])
        self.speed = 0

        self.collision_layer = 3
        self.collision_mask = []

    def move(self, direction, speed):
        """
        Accelerates this entity in a given direction at a given speed.

        Args:
            direction (float): Direction to move towards in radians.
            speed (float): Speed at which to accelerate at.
        """
        self.velocity = np.array([np.cos(direction), np.sin(direction)]) * speed

    def stop(self):
        """
        Sets this entity's velocity to zero.
        """
        self.velocity *= 0

    def rotate(self, direction):
        """
        Rotates this entity in given direction.

        Args:
            direction (float): Direction to rotate towards.
        """
        self.image = pg.transform.rotate(self.base_image, -np.degrees(direction))
        self.rect = self.image.get_rect(center=self.rect.center)

    def collidepoint(self, point):
        """
        Checks if point is within this entity's collision box.

        Args:
             point (tuple): The point to check.

        Returns:
            bool: True if point is within this entity's collision box, otherwise False.
        """
        return self.rect.collidepoint(point)

    def update(self, delta, model):
        """
        Updates this entity. Should only be called by the main game loop.

        Args:
            delta (float): Time since last tick of the main game loop.
            model (model.Model): Reference to model of the game.
        """
        self.update_position(delta)
        self.rect.center = self.position

    def update_position(self, delta):
        """
        Updates the position of this entity.

        Args:
            delta (float): Time since last tick of the main game loop.
        """
        if not np.allclose(self.velocity, 0):
            self.update_collide(delta)
            self.position += self.velocity * delta

    def update_collide(self, delta):
        """
        Checks for collisions and updates the velocity of this entity accordingly.

        Args:
            delta (float): Time since last tick of the main game loop.
        """
        new_position_x = (self.position[0] + self.velocity[0] * delta, self.position[1])
        new_position_y = (self.position[0], self.position[1] + self.velocity[1] * delta)
        for layer in self.collision_mask:
            for collision_object in self.model.collision_layers[layer]:
                if collision_object == self:
                    continue
                if collision_object.collidepoint(new_position_x):
                    self.velocity[0] = 0.0
                    self.collide_with(collision_object)
                    break

            for collision_object in self.model.collision_layers[layer]:
                if collision_object == self:
                    continue
                if collision_object.collidepoint(new_position_y):
                    self.velocity[1] = 0.0
                    self.collide_with(collision_object)
                    break

    def collide_with(self, other):
        """
        Perform operation when colliding with other object.

        Args:
            other (entity.Entity): The entity to collide with.
        """
        pass

    def set_position(self, new_position):
        """
        Sets position of this entity.

        Args:
            new_position (tuple): The position to move this entity to.
        """
        self.position = np.array(new_position, dtype=np.float64)
        self.rect.center = self.position
