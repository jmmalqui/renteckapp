from mesa.container.container import _MesaContainer
from mesa.flag.core_flag import MesaCoreFlag
from mesa.flag.render_flag import MesaRenderFlag
import pygame as pg


class MesaSingleContainer(_MesaContainer):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.element_center_v_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.element_center_h_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.image = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.original_image = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.image_pos = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.image_center_v_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.image_center_h_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT

    def set_background_image(self, path):
        if path == None:
            self.image = None
            self.original_image = None
        else:
            self.image = pg.image.load(path).convert_alpha()
            self.image = pg.transform.box_blur(self.image, 10)
            self.original_image = self.image.copy()

    def center_image_vertical(self):
        self.image_center_v_flag = MesaRenderFlag.IMAGE_CENTERED_V

    def center_image_horizontal(self):
        self.image_center_h_flag = MesaRenderFlag.IMAGE_CENTERED_H

    def center_image(self):
        self.center_image_vertical()
        self.center_image_horizontal()

    def resize_match_parent_height(self):
        height = self.height
        print(height)
        width = (
            self.original_image.get_width() * height / self.original_image.get_height()
        )

        self.image = pg.transform.smoothscale(self.original_image, [width, height])

    def resize_match_parent_width(self):
        width = self.width
        height = (
            self.original_image.get_height() * width / self.original_image.get_width()
        )
        self.image = pg.transform.smoothscale(self.original_image, [width, height])

    def center_element_vertical(self):
        self.element_center_v_flag = MesaRenderFlag.ELEMENT_CENTERED_V

    def center_element_horizontal(self):
        self.element_center_h_flag = MesaRenderFlag.ELEMENT_CENTERED_H

    def center_element(self):
        self.center_element_vertical()
        self.center_element_horizontal()

    def compute_elements_positions(self):
        if len(self.elements) != 1:
            raise ValueError(
                f"MayaSingleContainer can only handle one children container, you may have added more than two or not added any.  Num of Children: {len(self.elements)}"
            )
        element: _MesaContainer = self.elements[0]
        if self.element_center_v_flag == MesaRenderFlag.ELEMENT_CENTERED_V:
            element.position.y = (self.height - element.surface.get_height()) // 2

            element.absolute_position.y = self.absolute_position.y + element.position.y
            element.rect = pg.Rect(
                element.absolute_position, element.surface.get_size()
            )
        if self.element_center_h_flag == MesaRenderFlag.ELEMENT_CENTERED_H:
            element.position.x = (self.width - element.surface.get_width()) // 2
            element.absolute_position.x = self.absolute_position.x + element.position.x

            element.rect = pg.Rect(
                element.absolute_position, element.surface.get_size()
            )
        return super().compute_elements_positions()

    def late_init(self):
        if len(self.elements) != 1:
            raise ValueError(
                "MayaSingleContainer can only handle one children container"
            )
        return super().late_init()

    def render(self):
        self.image_pos = pg.Vector2(0, 0)
        if self.image_center_v_flag == MesaRenderFlag.IMAGE_CENTERED_V:
            self.image_pos.y = (self.height - self.image.get_height()) // 2
        if self.image_center_h_flag == MesaRenderFlag.IMAGE_CENTERED_H:
            self.image_pos.x = (self.width - self.image.get_width()) // 2
        if self.image != MesaCoreFlag.NOT_DECLARED_ON_INIT:
            self.surface.blit(self.image, self.image_pos)
