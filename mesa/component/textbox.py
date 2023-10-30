from mesa.container.container import _MesaContainer
from mesa.flag.core_flag import MesaCoreFlag
from mesa.flag.render_flag import MesaRenderFlag
from mesa.text_buffer.text_buffer import TextBuffer
import pygame as pg


class MesaTextBox(_MesaContainer):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.font_name = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.font = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.font_size = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.text = ""
        self.text_surface = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.bold = False
        self.italic = False
        self.text_background_color = None
        self.antialias = True
        self.text_color = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.buffer = TextBuffer()
        self.text_center_v_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.text_center_h_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT
        self.metrics = []
        self.pointer_position = self.get_pointer_position()
        self.blink = False
        self.tick = 0

    def get_input(self):
        return self.buffer

    def get_pointer_position(self):
        return (sum([x[4] for x in self.metrics[: self.buffer.pointer]]),)

    def handle_events(self):
        for event in self.scene.manager.get_events():
            if event.type == pg.TEXTINPUT:
                self.buffer.add(event.text)
                self.text = self.buffer.buffer
                self.make_text_surface()
                self.buffer.shift_right()
                self.metrics = pg.Font.metrics(self.font, self.text)
                self.pointer_position = self.get_pointer_position()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    self.buffer.delete()
                    self.text = self.buffer.buffer
                    self.make_text_surface()
                    self.metrics = pg.Font.metrics(self.font, self.text)
                    self.pointer_position = self.get_pointer_position()
                if event.key == 8:
                    self.buffer.pop()
                    self.text = self.buffer.buffer
                    self.make_text_surface()
                    self.metrics = pg.Font.metrics(self.font, self.text)
                    self.pointer_position = self.get_pointer_position()
                if event.key == pg.K_LEFT:
                    self.buffer.shift_left()
                    self.pointer_position = self.get_pointer_position()
                if event.key == pg.K_RIGHT:
                    self.buffer.shift_right()

                    self.pointer_position = self.get_pointer_position()
                if event.key == pg.K_RETURN:
                    self.text += "\n"
                    self.make_text_surface()
                    self.metrics = pg.Font.metrics(self.font, self.text)
                    self.pointer_position = self.get_pointer_position()

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

    def set_text(self, text):
        if self.text == MesaCoreFlag.NOT_DECLARED_ON_INIT:
            self.text = text
        if self.text_surface != MesaCoreFlag.NOT_DECLARED_ON_INIT:
            if text != self.text:
                self.text = text
                self.make_text_surface()

    def make_text_surface(self):
        "called"
        self.text_surface = self.font.render(
            self.text,
            self.antialias,
            self.text_color,
            self.text_background_color,
        )

    def late_init(self):
        self.font = pg.font.SysFont(
            self.font_name, self.font_size, self.bold, self.italic
        )
        self.make_text_surface()
        pg.key.set_text_input_rect(self.rect)
        return super().late_init()

    def inherit_update(self):
        self.tick += 1
        self.handle_events()
        return super().inherit_update()

    def render(self):
        self.text_position = pg.Vector2(0, 0)
        if self.text_center_v_flag == MesaRenderFlag.TEXT_CENTERED_V:
            self.text_position.y = (self.height - self.text_surface.get_height()) // 2

        if self.text_center_h_flag == MesaRenderFlag.TEXT_CENTERED_H:
            self.text_position.x = (self.width - self.text_surface.get_width()) // 2
        if self.tick % 5 == 0:
            self.blink = not self.blink
        if self.blink:
            pg.draw.rect(
                self.surface,
                "cyan",
                [self.pointer_position[0], 0, 2, 24],
                0,
            )
        else:
            pg.draw.rect(
                self.surface,
                "black",
                [self.pointer_position[0], 0, 2, 24],
                0,
            )
        self.surface.blit(self.text_surface, self.text_position)
