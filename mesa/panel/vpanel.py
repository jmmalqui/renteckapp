from mesa.stack.vstack import MesaStackVertical
from mesa.flag.core_flag import MesaCoreFlag
from mesa.flag.render_flag import MesaRenderFlag
import pygame as pg


class MesaSlidablePanelVertical(MesaStackVertical):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.type_flag = MesaRenderFlag.SLIDABLE_CONTAINER_VERTICAL
        self.perform_late_init = True
        self.slider_height = 5
        self.slider_color = "black"
        self.handle_get = False
        self.mouse_handle = pg.Vector2(pg.mouse.get_pos())
        self.separator = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.middle_x = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.middle_y = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.slider = MesaCoreFlag.NOT_DECLARED_ON_INIT

    def set_slider_color(self, color):
        self.slider_color = color

    def compute_extra_inherit(self):
        self.remake_slider()
        for element in self.elements:
            element.compute_extra_inherit()

    def late_init(self):
        self.remake_slider()
        return super().late_init()

    def remake_slider(self):
        print("im redone :)", self)
        self.middle_x = 0
        self.middle_y = self.height // 2
        self.slider = pg.Rect(
            self.middle_x,
            self.middle_y - self.slider_height,
            self.width,
            self.slider_height,
        )

    def inherit_update(self):
        if len(self.elements) == 0:
            raise ValueError("A Slidable Panel must have children elements")
        if len(self.elements) != 2:
            raise ValueError(f"Panel must have two children elements")
        return super().inherit_update()

    def inherit_render(self):
        pg.draw.rect(self.surface, self.slider_color, self.slider, 0)
