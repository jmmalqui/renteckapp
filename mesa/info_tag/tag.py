import pygame as pg
from mesa.core import *
from mesa.animation import *
from mesa.style import *


class TagProperty:
    def __init__(self, fill, border, ttl) -> None:
        self.fill = fill
        self.border = border
        self.ttl = ttl


class InfoTagLevels:
    NOTIFY = TagProperty([0, 70, 0], [0, 170, 0], 100)
    ALERT = TagProperty([70, 70, 0], [170, 170, 0], 250)
    CRITICAL = TagProperty([70, 0, 0], [170, 0, 0], 400)
    SPECIAL = TagProperty([70, 0, 70], [170, 0, 170], 300)


class InfoTagHandler:
    def __init__(self, core) -> None:
        self.core: MesaCore = core
        self.tags: list[InfoTag] = []
        self.tag_font = pg.font.SysFont("meiryoui", 15, False, True)

    def inform(self, information, level=InfoTagLevels.NOTIFY):
        self.tags.append(InfoTag(self, information, level))
        self.update_tag_ids()

    def update_tag_ids(self):
        tag_num = len(self.tags)
        for tag_id, tag in enumerate(self.tags):
            tag.set_id(tag_num - tag_id - 1)

    def update(self):
        for tag in self.tags:
            tag.update()

    def render(self):
        for tag in self.tags:
            tag.render()


class InfoTag:
    def __init__(self, handler, information, level: TagProperty) -> None:
        self.id = 0
        self.information = information
        self.level = level
        self.handler: InfoTagHandler = handler
        self.animation = Animation()
        self.tick = 0
        self.x = AnimVal(self.animation, 0)
        self.y = AnimVal(self.animation, 0)
        self.alpha = AnimVal(self.animation, 255)
        self.text = self.handler.tag_font.render(
            self.information, True, MesaDefaultGUI.DEFAULT_TEXT_COLOR, wraplength=450
        )
        self.surface = pg.Surface(
            [self.text.get_width() + 50, self.text.get_height() + 20]
        ).convert_alpha()
        self.rect = pg.Rect([0, 0], self.surface.get_size())
        self.x.move_to(60, 60, MesaAnimationCurves.EASE_OUT_CUBIC)
        self.gap = 20
        self.vanishing_time = 100

    def set_id(self, id):
        self.id = id
        y_difference = 0
        for tag in self.handler.tags:
            if tag.id < self.id:
                y_difference += self.gap
                y_difference += tag.surface.get_height()
        self.y.move_to(-1 * y_difference, 30, MesaAnimationCurves.EASE_OUT_SINE)

    def update(self):
        self.tick += 1
        self.animation.update()
        self.rect = pg.Rect([0, 0], self.surface.get_size())
        if self.tick == self.level.ttl:
            self.alpha.move_to(0, self.vanishing_time, MesaAnimationCurves.EASE_IN_SINE)
        if self.tick >= self.level.ttl + self.vanishing_time:
            self.handler.tags.remove(self)
            self.handler.update_tag_ids()

    def render(self):
        self.surface.fill("black")
        pg.draw.rect(self.surface, self.level.fill, self.rect, 0)
        pg.draw.rect(self.surface, self.level.border, self.rect, 2)
        self.surface.blit(self.text, [25, 10])
        self.surface.set_alpha(self.alpha.value)
        self.handler.core.display.blit(
            self.surface,
            [
                self.x.value,
                self.handler.core.display.get_height()
                - self.gap
                - self.surface.get_height()
                + self.y.value,
            ],
        )
