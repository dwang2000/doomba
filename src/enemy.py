import random
import numpy as np
from . import mob
from . import gun


class Enemy(mob.Mob):

    def __init__(self, model):
        """
        Constructs an instance of an enemy.

        Args:
             model (model.Model): Model of the game to which to instantiate the mob into.
        """
        super().__init__(model)

        self.collision_layer = 2
        self.collision_mask = [0]
        self.bullet_collision_mask = [0, 1]
        self.time_of_death = 0

        self.name = "NULL"

    def update(self, delta, model):
        """
        Updates this enemy. Performs enemy behavior.

        Args:
            delta (float): Time since last tick of the main game loop.
            model (model.Model): Model of the game.
        """
        super().update(delta, model)
        self.fire("PRIMARY")
        self.aim(model.player.position)

    def get_direction_to_player(self):
        """
        Gets direction to player.

        Returns:
            float: Direction to player in radians.
        """
        vector = self.model.player.position - self.position
        return np.arctan2(vector[1], vector[0])

    def take_damage(self, bullet):
        """
        Perform operations when this mob is hit by a bullet. Records time of death when dying.

        Args:
            bullet (bullet.Bullet): Bullet this mob was hit by.
        """
        super().take_damage(bullet)
        if self.health <= 0:
            self.time_of_death = self.model.time

    def __str__(self):
        """
        Creates string for display in after action report.

        Args:
            str: String representation.
        """
        obiturary = self.name + "\n"
        obiturary += random.choice([
            "'volunteered at the orphanage'\n",
            "'just one day from retiring'\n",
            "'member of an endangered species'\n",
            "'drafted by local warlord'\n",
            "'paying for parents' medical debt'\n",
            "",
        ])
        obiturary += "Murdered at {time:.2f} seconds.\n".format(time=self.time_of_death/1000)
        obiturary += "Died carrying a {gun}.\n".format(gun=str(self.gun))
        return obiturary


class EnemyCroomba(Enemy):

    def __init__(self, model):
        self.base_image = model.assets.images['croomba']
        super().__init__(model)
        self.gun = gun.GunCroombaPistol(self, model)

        self.health = 50
        self.speed = .15

        self.timer_move = 0
        self.move_time = 1000

        self.points = 10

        self.name = "CROOMBA UNIT #{number:04}".format(number=random.randint(1, 9999))

    def update(self, delta, model):
        super().update(delta, model)
        self.timer_move -= delta
        if self.timer_move <= 0:
            self.timer_move = self.move_time
            new_direction = self.get_direction_to_player()
            offset = random.choice([-1, 0, 0, 1])
            new_direction = np.radians(np.round(((np.degrees(new_direction) / 360) * 8) + offset) * 45)
            self.move(new_direction, self.speed)
