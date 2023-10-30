import os
import pygame as pg
from mesa.flag.core_flag import *

from mesa.info_tag.tag import InfoTagHandler

os.environ["SDL_IME_SHOW_UI"] = "1"


class MesaCore:
    def __init__(self) -> None:
        from mesa.scene.scene_manager import MesaSceneManager

        pg.init()
        self.perform_late_init = True
        self.display = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.clock = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.clock_type = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.clock_fps = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.rendering_flags = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.bacgkround_color = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.delta_time = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.caption = MesaCoreFlag.NOT_DECLARED_ON_INIT

        self.info_tag = InfoTagHandler(self)
        self.scene_manager = MesaSceneManager(self)
        self.on_debug = False

    def set_application_name(self, title):
        self.caption = title
        pg.display.set_caption(self.caption)

    def set_rendering_flags(self, *flags):
        self.rendering_flags = flags

    def set_clock(self, fps):
        self.clock = pg.Clock()
        self.clock_type = MesaCoreFlag.NON_TICK_BUSY_CLOCK
        self.clock_fps = fps

    def set_busy_clock(self, fps):
        self.clock = pg.Clock()
        self.clock_type = MesaCoreFlag.TICK_BUSY_CLOCK
        self.clock_fps = fps

    def set_display_size(self, height, width):
        if self.rendering_flags == MesaCoreFlag.NOT_DECLARED_ON_INIT:
            self.rendering_flags = 0
            self.display = pg.display.set_mode(
                [height, width], flags=self.rendering_flags
            )
        else:
            flag = self.rendering_flags[0]
            for f in self.rendering_flags[0:]:
                flag |= f
            self.display = pg.display.set_mode([height, width], flag)

    def late_init(self):
        if self.display == MesaCoreFlag.NOT_DECLARED_ON_INIT:
            raise ValueError(
                "Display was not initialized, perhaps you forgot set_display_size() ?"
            )

        if self.clock == MesaCoreFlag.NOT_DECLARED_ON_INIT:
            self.set_clock(60)
        if self.bacgkround_color == MesaCoreFlag.NOT_DECLARED_ON_INIT:
            self.bacgkround_color = "black"

    def check_events(self):
        self.scene_manager.pump_event(None)
        for event in pg.event.get():
            self.scene_manager.pump_event(event)
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    self.on_debug = not self.on_debug
            if event.type == pg.MOUSEBUTTONDOWN:
                ...
                # self.info_tag.inform("Info System", InfoTagLevels.NOTIFY)

            if event.type == pg.VIDEORESIZE:
                # self.scene_manager.resize_current_surface()
                self.scene_manager.update_scene_sizes()

    def check_events(self):
        self.scene_manager.pump_event(None)
        for event in pg.event.get():
            self.scene_manager.pump_event(event)
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.VIDEORESIZE:
                self.scene_manager.update_scene_sizes()

    def set_background_color(self, color):
        self.bacgkround_color = color

    def update(self):
        ...

    def __coreupdate__(self):
        self.mouse_rel = pg.mouse.get_rel()

        if self.perform_late_init:
            self.late_init()
            self.perform_late_init = not self.perform_late_init

        self.scene_manager.update()
        self.info_tag.update()

    def render(self):
        ...

    def __corerender__(self):
        self.display.fill(self.bacgkround_color)
        self.scene_manager.render()
        self.info_tag.render()
        self.render()
        pg.display.flip()

    def update_dt(self):
        if self.clock_type == MesaCoreFlag.NON_TICK_BUSY_CLOCK:
            self.delta_time = self.clock.tick(self.clock_fps)
        elif self.clock_type == MesaCoreFlag.TICK_BUSY_CLOCK:
            self.delta_time = self.clock.tick_busy_loop(self.clock_fps)

    def run(self):
        while self.run:
            self.update_dt()
            self.check_events()
            self.__coreupdate__()
            self.__corerender__()
