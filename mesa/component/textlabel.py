from mesa.container.container import _MesaContainer
from mesa.flag.core_flag import MesaCoreFlag
from mesa.flag.render_flag import MesaRenderFlag
import pygame as pg


class MesaTextLabel(_MesaContainer):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.font_name = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.font = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.font_size = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.text = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.text_surface = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.bold = False
        self.italic = False
        self.text_background_color = None
        self.antialias = True
        self.text_color = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.text_center_v_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.text_center_h_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.text_offset = pg.Vector2(0, 0)

    def center_text_vertical(self):
        self.text_center_v_flag = MesaRenderFlag.TEXT_CENTERED_V

    def center_text_horizontal(self):
        self.text_center_h_flag = MesaRenderFlag.TEXT_CENTERED_H

    def center_text(self):
        self.center_text_horizontal()
        self.center_text_vertical()

    def set_text_color(self, text_color):
        if self.text_color == MesaCoreFlag.NOT_DECLARED_ON_INIT:
            self.text_color = text_color
        if self.text_surface != MesaCoreFlag.NOT_DECLARED_ON_INIT:
            if text_color != self.text_color:
                self.text_color = text_color
                self.make_text_surface()

    def set_text_background_color(self, color):
        self.text_background_color = color

    def unset_antialiasing(self):
        self.antialias = False

    def set_bold(self):
        self.bold = True

    def set_italic(self):
        self.italic = True

    def set_font_name(self, font_name):
        self.font_name = font_name

    def set_font_size(self, font_size):
        if self.font_size == MesaCoreFlag.NOT_DECLARED_ON_INIT:
            self.font_size = font_size
        if self.font_size != MesaCoreFlag.NOT_DECLARED_ON_INIT:
            if font_size != self.font_size:
                self.font_size = font_size
                self.font = pg.font.SysFont(
                    self.font_name, self.font_size, self.bold, self.italic
                )
                self.make_text_surface()

    def set_offset(self, x, y):
        self.text_offset = pg.Vector2(x, y)

    def set_text(self, text):
        if self.text == MesaCoreFlag.NOT_DECLARED_ON_INIT:
            self.text = text
        if self.text_surface != MesaCoreFlag.NOT_DECLARED_ON_INIT:
            if text != self.text:
                self.text = text
                self.make_text_surface()

    def make_text_surface(self):
        self.text_surface = self.font.render(
            self.text, self.antialias, self.text_color, self.text_background_color
        )

    def late_init(self):
        print("name: ", self.__class__.__name__)
        self.font = pg.font.SysFont(
            self.font_name, self.font_size, self.bold, self.italic
        )
        self.make_text_surface()
        return super().late_init()

    def render(self):
        self.text_position = pg.Vector2(0, 0)
        if self.text_center_v_flag == MesaRenderFlag.TEXT_CENTERED_V:
            self.text_position.y = (self.height - self.text_surface.get_height()) // 2

        if self.text_center_h_flag == MesaRenderFlag.TEXT_CENTERED_H:
            self.text_position.x = (self.width - self.text_surface.get_width()) // 2
        self.text_position += self.text_offset
        self.surface.blit(self.text_surface, self.text_position)
