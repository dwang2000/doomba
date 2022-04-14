import pygame as pg
import os

ASSET_DIR = 'assets'


class Loader:

    def __init__(self):
        """
        Constructs an asset loader for shared assets such as images and sounds.

        Attributes:
            - self.images: Dictionary of images loaded as pygame Surfaces.
        """
        self.images = dict()
        self.load_images()

    def load_images(self):
        """
        Loads images and stores them as optimized pygame Surfaces in image dictionary.
        """
        self.images['doomba'] = pg.image.load(os.path.join(ASSET_DIR, 'doomba.png')).convert_alpha()
        self.images['croomba'] = pg.image.load(os.path.join(ASSET_DIR, 'croomba.png')).convert_alpha()

        self.images['bullet_small_a'] = pg.image.load(os.path.join(ASSET_DIR, 'bullet_small_a.png')).convert_alpha()

        self.images['background_a1'] = pg.image.load(os.path.join(ASSET_DIR, 'background_a1.png')).convert()
