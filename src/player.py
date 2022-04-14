import numpy as np
from . import mob


class Player(mob.Mob):

    def __init__(self, model):
        """
        Constructs an instance of the player.

        Args:
             model (model.Model): Model of the game to which to instantiate the mob into.
        """
        self.base_image = model.assets.images['doomba']
        super().__init__(model)

        self.collision_layer = 1
        self.collision_mask = [0]
        self.bullet_collision_mask = [0, 2]

        self.health = 100
        self.speed = .28
