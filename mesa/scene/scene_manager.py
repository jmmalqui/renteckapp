from mesa.core import *
from typing import Dict, Union
from mesa.flag import *
import pygame as pg


class MesaSceneManager:
    def __init__(self, core) -> None:
        from mesa.scene.scene import MesaScene

        self.core: MesaCore = core
        self.scenes: Dict["str", MesaScene] = {}
        self.current_scene_name = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.current_scene: Union[
            MesaScene, MesaCoreFlag
        ] = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.events = []

    def set_init_scene(self, scene_name):
        self.current_scene_name = scene_name
        print(self.current_scene_name)

    def get_events(self):
        return self.events

    def pump_event(self, event):
        if event:
            self.events.append(event)
        else:
            self.events.clear()

    def add_scene(self, scene):
        self.scenes[scene.name] = scene

    def update_scene_sizes(self):
        for scene in self.scenes.values():
            scene.resize()

    def update_scene_ids(self):
        self.current_scene = self.scenes[self.current_scene_name]

    def go_to(self, scene_name):
        self.current_scene_name = scene_name

    def resize_current_surface(self):
        if self.current_scene != MesaCoreFlag.NOT_DECLARED_ON_INIT:
            self.current_scene.surface = pg.Surface(pg.display.get_window_size())
            self.current_scene.container.set_size_as_display()
            self.current_scene.container.set_position_as_core()
            self.current_scene.container.build()
            self.current_scene.container._on_resize()

    def update(self):
        self.update_scene_ids()
        self.current_scene.__coreupdate__()

    def render(self):
        self.current_scene.__corerender__()
