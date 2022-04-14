import pygame as pg


class Controller:

    KEY_MAP = {
        "UP": pg.K_w,
        "DOWN": pg.K_s,
        "LEFT": pg.K_a,
        "RIGHT": pg.K_d,
        "PRIMARY_FIRE": 0,
        "SECONDARY_FIRE": 2,
    }

    def __init__(self, res_ratio):
        self.res_ratio = res_ratio

        self.movement = "NONE"
        self.aim = (0, 0)
        self.fire = "NONE"

    def update(self, input_events):
        key_event = False
        mouse_motion_event = False
        mouse_button_event = False

        for event in input_events:
            if event.type == pg.KEYUP or event.type == pg.KEYDOWN:
                key_event = True
            elif event.type == pg.MOUSEMOTION:
                mouse_motion_event = True
            elif event.type == pg.MOUSEBUTTONUP or event.type == pg.MOUSEBUTTONDOWN:
                mouse_button_event = True

        if key_event:
            keys_pressed = pg.key.get_pressed()
            if keys_pressed[self.KEY_MAP["UP"]]:
                if keys_pressed[self.KEY_MAP["LEFT"]]:
                    self.movement = "UP_LEFT"
                elif keys_pressed[self.KEY_MAP["RIGHT"]]:
                    self.movement = "UP_RIGHT"
                else:
                    self.movement = "UP"
            elif keys_pressed[self.KEY_MAP["DOWN"]]:
                if keys_pressed[self.KEY_MAP["LEFT"]]:
                    self.movement = "DOWN_LEFT"
                elif keys_pressed[self.KEY_MAP["RIGHT"]]:
                    self.movement = "DOWN_RIGHT"
                else:
                    self.movement = "DOWN"
            elif keys_pressed[self.KEY_MAP["LEFT"]]:
                self.movement = "LEFT"
            elif keys_pressed[self.KEY_MAP["RIGHT"]]:
                self.movement = "RIGHT"
            else:
                self.movement = "NONE"

        if mouse_motion_event:
            self.aim = pg.mouse.get_pos()
            self.aim = self.aim[0] * self.res_ratio, self.aim[1] * self.res_ratio

        if mouse_button_event:
            mouse_buttons_pressed = pg.mouse.get_pressed(num_buttons=3)

            if mouse_buttons_pressed[self.KEY_MAP["PRIMARY_FIRE"]]:
                self.fire = "PRIMARY"
            elif mouse_buttons_pressed[self.KEY_MAP["SECONDARY_FIRE"]]:
                self.fire = "SECONDARY"
            else:
                self.fire = "NONE"

        return key_event, mouse_motion_event, mouse_button_event

    def __getitem__(self, name):
        if name == "MOVEMENT":
            return self.movement
        elif name == "AIM":
            return self.aim
        elif name == "FIRE":
            return self.fire
