import numpy as np
import pygame as pg
import asset_loader as ld
from random import choice
import player
import enemy
import gun


class Model:

    CENTER = (683, 384)
    PLAYER_SPAWN = (227, 384)
    ENEMY_SPAWNS = [(1138, 384)]

    enemies = []
    defeated = []

    background = pg.sprite.Group()
    entities = pg.sprite.Group()

    collision_layers = {
        0: [],              # Background
        1: [],              # Player
        2: [],              # Enemies
        3: [],              # None
    }

    score = 0
    time = 0

    def __init__(self, config):
        """
        Creates and returns model representing the game.

        Attributes:
            -config (dict): Game configuration.
            -assets (asset_loader.Loader): Loaded assets such as images or sounds.
            -player (entity.Entity): Player entity.
            -spawn_time_decay_rate (int): Time to decrease spawn time by for each enemy spawned.
            -spawn_time (int): Time between enemy spawns.
            -min_spawn_time (int): Minimum spawn time.
            -min_enemies (int): Minimum number of enemies.

        Args:
            **settings (dict): Game settings selected by user.
        """
        self.config = config
        self.assets = ld.Loader()

        self.background_image = pg.sprite.Sprite()
        self.background_walls = [
            pg.Rect(80, 34, 20, 700),
            pg.Rect(1250, 34, 20, 700),
            pg.Rect(90, 80, 1200, 20),
            pg.Rect(90, 725, 1200, 20),
        ]
        self.collision_layers[0].extend(self.background_walls)

        self.player = player.Player(self)
        default_player_gun = gun.GunFlieger
        self.player.set_gun(default_player_gun)
        self.generate_level()

        self.timer_spawn = 0

        if config['difficulty'] == 'easy':
            self.spawn_time_decay_rate = 40
            self.spawn_time = 5000
            self.min_spawn_time = 3000
            self.min_enemies = 0
        elif config['difficulty'] == 'normal':
            self.spawn_time_decay_rate = 120
            self.spawn_time = 3000
            self.min_spawn_time = 1250
            self.min_enemies = 1
        elif config['difficulty'] == 'hard':
            self.spawn_time_decay_rate = 350
            self.spawn_time = 1000
            self.min_spawn_time = 750
            self.min_enemies = 3

    def generate_level(self):
        """
        Generates level.
        """
        self.background.empty()
        self.background_image.image = self.assets.images['background_a1']
        self.background_image.rect = self.background_image.image.get_rect()
        self.background_image.rect.center = self.CENTER
        self.background.add(self.background_image)

        self.player.set_position(self.PLAYER_SPAWN)
        self.add_entity(self.player)

    def draw(self, window):
        """
        Renders game world and entities.

        Args:
            window (pygame.Surface): Window to render game on.
        """
        self.background.draw(window)
        self.entities.draw(window)

    def update(self, delta, controller, recorded_input_events):
        """
        Update the game model.

        Args:
            delta (float): Time since last tick of the main game loop.
            controller (controller.Controller): Controller representing user input.
            recorded_input_events (list): List of types of user input that have changed.
        """
        if self.timer_spawn <= 0:
            self.timer_spawn = self.spawn_time
            self.spawn_time = max(self.min_spawn_time, self.spawn_time - self.spawn_time_decay_rate)
            self.spawn_enemy()
        self.timer_spawn -= delta

        self.update_player(delta, controller, recorded_input_events)
        self.entities.update(delta, self)

        self.time += delta

    def update_player(self, delta, controller, recorded_input_events):
        """
        Updates the player.

        Args:
            delta (float): Time since last tick of the main game loop.
            controller (controller.Controller): Controller representing user input.
            recorded_input_events (list): List of types of user input that have changed.
        """
        if recorded_input_events[0]:

            speed = self.player.speed

            if controller["MOVEMENT"] == "RIGHT":
                self.player.move(np.radians(0), speed)
            elif controller["MOVEMENT"] == "UP_RIGHT":
                self.player.move(np.radians(-45), speed)
            elif controller["MOVEMENT"] == "UP":
                self.player.move(np.radians(-90), speed)
            elif controller["MOVEMENT"] == "UP_LEFT":
                self.player.move(np.radians(-135), speed)
            elif controller["MOVEMENT"] == "LEFT":
                self.player.move(np.radians(180), speed)
            elif controller["MOVEMENT"] == "DOWN_LEFT":
                self.player.move(np.radians(135), speed)
            elif controller["MOVEMENT"] == "DOWN":
                self.player.move(np.radians(90), speed)
            elif controller["MOVEMENT"] == "DOWN_RIGHT":
                self.player.move(np.radians(45), speed)
            else:
                self.player.stop()

        if recorded_input_events[1]:
            self.player.aim(controller["AIM"])

        if recorded_input_events[2]:
            self.player.fire(controller["FIRE"])

    def spawn_enemy(self):
        """
        Selects an enemy to spawn based on time and difficulty.
        """
        self.add_enemy(enemy.EnemyCroomba, choice(self.ENEMY_SPAWNS))

    def add_enemy(self, enemy_template, spawn_pos):
        """
        Instantiates an enemy and adds it to the model.

        Args:
            enemy_template (class): Class of enemy to instantiate.
            spawn_pos (tuple): Position to spawn new enemy at.
        """
        new_enemy = enemy_template(self)
        new_enemy.set_position(spawn_pos)
        self.enemies.append(new_enemy)
        self.add_entity(new_enemy)

    def add_entity(self, entity):
        """
        Adds entity to game model.

        Args:
            entity (entity.Entity): Entity to add.
        """
        self.entities.add(entity)
        self.collision_layers[entity.collision_layer].append(entity)

    def remove_entity(self, entity):
        """
        Removes entity from game model. Records enemies killed for end of the game. Ends the
        game when the player is killed.

        Args:
            entity (entity.Entity): Entity to remove.
        """
        if entity == self.player:
            print("YOU DIED!")
            print("Your score was {score}. Yay!".format(score=self.score))
            print("Your rampage lasted for {time:.2f} seconds. Wowzers.".format(time=self.time/1000))
            print("Here's a list of all your victims!")
            for defeated_enemy in self.defeated:
                print(defeated_enemy)
            pg.event.post(pg.event.Event(pg.QUIT))
        self.entities.remove(entity)
        try:
            self.collision_layers[entity.collision_layer].remove(entity)
            self.enemies.remove(entity)
        except ValueError:
            pass
        if isinstance(entity, enemy.Enemy):
            self.score += entity.points
            self.defeated.append(entity)
            if len(self.enemies) < self.min_enemies:
                self.spawn_enemy()
