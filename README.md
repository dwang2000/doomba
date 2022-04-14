
# Doomba Dungeon

## Project Summary

**Doomba Dungeon** is a game about a weaponized autonomous vacuum cleaner traversing a hostile environment, defeating enemies, and becoming increasingly powerful. Specifically, it is a top down shooter with randomly generated rooms filled with enemies and loot.

This project will use the argparse module to initialize settings, such as difficulty, before launching the game itself. If necessary, the json module will also be used to store game data. External modules that Doomba will use are Pygame, for graphics, sound, and user interface, and Numpy to handle calculations, such as entity movement and object collision.

Procedural loot and level generation, sound, and user interface are not yet implemented.

## Installation and Running Instructions

Dependencies:
```
pip install numpy
pip install pygame
```
Launching the game:
```
python doomba.py
```
Display game launch options:
```
python doomba.py -h
```

## Code Structure
```
DoombaDungeon
|---assets
|   |   background_a1.png
|   |   bullet_small_a.png
|   |   croomba.png
|   |   doomba.png
|
|   README.md
|   asset_loader.py
|   bullet.py
|   controller.py
|   doomba.py
|   enemy.py
|   entity.py
|   gun.py
|	interface.py
|   item.py
|   mob.py
|   model.py
|   player.py
```
