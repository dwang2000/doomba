import argparse
import pygame as pg

from src import model as md
from src import controller as control


COLOR_BACKGROUND = (42, 42, 42)


def build_parser():
    """
    Builds an ArgumentParser with the specified parameters from the CLI.

    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description="Configure your game of DoombaDungeon!")
    parser.add_argument('-r', default='1366x768', choices=['854x480', '1280x720', '1366x768', '1600x900'],
                        help='Resolution (default: 1366x768)')
    parser.add_argument('-f', default=75, choices=[30, 60, 75, 90, 120], type=int,
                        help='Maximum Frame Rate (default: 75)')
    parser.add_argument('-d', default='normal', choices=['easy', 'normal', 'hard'],
                        help='Difficulty (default: normal)')

    return parser


def config_model(parser):
    """
    Create and configure new game from settings.

    Args:
        parser (argparse.ArgumentParser): Arguments to configure game settings.

    Returns:
        model.Model: Model representing the game.
    """
    args = parser.parse_args()
    config = dict()

    config['resolution'] = (int(args.r.split('x')[0]), int(args.r.split('x')[1]))
    config['frame_rate'] = args.f
    config['difficulty'] = args.d

    screen = pg.display.set_mode(config['resolution'])

    model = md.Model(config)
    return model, config, screen


def game_loop(model, config, screen):
    """
    Main game loop, draws game and handles player input.

    Args:
        model (model.Model): Model representing the game.
        config (dict): Desired game settings.
        screen (pg.surface.Surface): Primary screen to render game within.
    """
    window = pg.surface.Surface(size=(1366, 768))

    pg.display.set_caption("DoombaDungeon")

    res_ratio = 1366 / config['resolution'][0]
    controller = control.Controller(res_ratio)

    frame_rate = config['frame_rate']
    clock = pg.time.Clock()
    print("Starting game...")
    running = True

    while running:
        delta = clock.tick(frame_rate)
        input_events = pg.event.get()
        for event in input_events:
            if event.type == pg.QUIT:
                running = False
        recorded_input_events = controller.update(input_events)
        model.update(delta, controller, recorded_input_events)
        render(model, window, screen)


def render(model, window, screen):
    """
    Renders the game.

    Args:
        model (model.Model): Model representing the game.
        window (pg.surface.Surface): Surface with onto which the game model is rendered.
        screen (pg.surface.Surface): Primary screen to render game within.
    """
    window.fill(COLOR_BACKGROUND)

    model.draw(window)
    resized = pg.transform.scale(window, screen.get_rect().size)
    screen.blit(resized, (0, 0))

    pg.display.update()


def cleanup():
    """
    Stops the game, performs cleanup, and exits the program.
    """
    print("Exiting...")
    pg.quit()


def main():
    """
    Parses arguments, launches game loop, closes game, clean up on exit.
    """
    print("Setting up...")
    parser = build_parser()
    pg.init()
    model, config, screen = config_model(parser)
    game_loop(model, config, screen)
    cleanup()


if __name__ == "__main__":
    main()
