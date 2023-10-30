from mesa.container.container import _MesaContainer
from mesa.flag.core_flag import MesaCoreFlag
from mesa.flag.render_flag import MesaRenderFlag
from mesa.transform.transform import circle_chop
import pygame as pg


class MesaImage(_MesaContainer):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.image = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.original_image = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.image_pos = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.element_center_v_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.element_center_h_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT

    def border_image(self):
        self.image = circle_chop(self.image)
        self.original_image = self.image.copy()

    def center_element_vertical(self):
        self.element_center_v_flag = MesaRenderFlag.ELEMENT_CENTERED_V

    def center_element_horizontal(self):
        self.element_center_h_flag = MesaRenderFlag.ELEMENT_CENTERED_H

    def center_element(self):
        self.center_element_vertical()
        self.center_element_horizontal()

    def set_image(self, path):
        if path == None:
            self.image = None
            self.original_image = None
        else:
            self.image = pg.image.load(path).convert_alpha()
            self.original_image = self.image.copy()

    def resize_image(self, size):
        self.image = pg.transform.smoothscale(self.original_image, size)

    def resize_match_parent_height(self):
        height = self.height
        print(height)
        width = (
            self.original_image.get_width() * height / self.original_image.get_height()
        )
        print(width, height)
        print(self.image.get_size(), self.original_image.copy())
        self.image = pg.transform.smoothscale(self.original_image, [width, height])

    def resize_match_parent_width(self):
        width = self.width
        height = (
            self.original_image.get_height() * width / self.original_image.get_width()
        )
        self.image = pg.transform.smoothscale(self.original_image, [width, height])

    def render(self):
        self.image_pos = pg.Vector2(0, 0)
        if self.element_center_v_flag == MesaRenderFlag.ELEMENT_CENTERED_V:
            self.image_pos.y = (self.height - self.image.get_height()) // 2

        if self.element_center_h_flag == MesaRenderFlag.ELEMENT_CENTERED_H:
            self.image_pos.x = (self.width - self.image.get_width()) // 2
        if self.image != None:
            self.surface.blit(self.image, self.image_pos)
        else:
            self.surface.fill("black")
