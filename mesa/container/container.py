from mesa.flag.core_flag import MesaCoreFlag
from mesa.flag.render_flag import MesaRenderFlag
from mesa.scene.scene import MesaScene
from mesa.transform.transform import *
from mesa.style.styles import MesaDefaultGUI
import pygame as pg
import random


class _MesaContainer:
    def __init__(self, parent) -> None:
        if isinstance(parent, MesaScene) or isinstance(parent, _MesaContainer):
            self.type_flag = MesaRenderFlag.CORE_CONTAINER
            self.parent = parent
            self.parent.container = self
            self.elements = []
            self.width = MesaCoreFlag.NOT_DECLARED_ON_INIT
            self.height = MesaCoreFlag.NOT_DECLARED_ON_INIT
            self.width_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT
            self.height_flag = MesaCoreFlag.NOT_DECLARED_ON_INIT
            self.margin = 0
            self.surface = MesaCoreFlag.NOT_DECLARED_ON_INIT
            self.position = pg.Vector2(0, 0)
            if isinstance(parent, MesaScene):
                self.scene = parent
            if isinstance(parent, _MesaContainer):
                self.scene = parent.scene
                self.absolute_position = self.parent.absolute_position + self.position
            else:
                self.absolute_position = pg.Vector2(0, 0)
            self.rect = MesaCoreFlag.NOT_DECLARED_ON_INIT
            self.background_color = MesaDefaultGUI.DEFAULT_CONTAINER_BACKGROUND_COLOR
            self.original_color = self.background_color.copy()
            self.font = pg.font.SysFont(
                MesaDefaultGUI.DEFAULT_FONT_TYPE, MesaDefaultGUI.DEFAULT_FONT_SIZE
            )
            self.is_hovered = False
            self.borders = [
                [False, None, None],
                [False, None, None],
                [False, None, None],
                [False, None, None],
            ]
            self.should_late_init = True
            self.radius = MesaCoreFlag.NOT_DECLARED_ON_INIT
            self.debug_color = [
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ]
            self.display_size = pg.display.get_window_size()
            self.on_init = True
            self.surface_type = MesaCoreFlag.NOT_DECLARED_ON_INIT

    def display_resized(self):
        if self.on_init:
            print("omg")
            self.on_init = False
            return True
        if pg.display.get_window_size() == self.display_size:
            return False
        else:
            self.display_size = pg.display.get_window_size()
            return True

    def perform_on_resize(self):
        ...

    def _on_resize(self):
        self.perform_on_resize()
        for element in self.elements:
            element._on_resize()

    def set_rounded_borders(self, radius):
        self.radius = radius

    def late_init(self):
        ...

    def set_margin(self, margin):
        self.margin = margin

    def set_color_as_parent(self):
        self.background_color = self.parent.background_color
        self.original_color = self.background_color

    def set_background_color(self, color):
        self.background_color = color
        self.original_color = self.background_color

    def get_absolute_position(self):
        return self.parent.absolute_position + self.position

    def is_container_hovered(self):
        return self.rect.collidepoint(pg.mouse.get_pos())

    def populate_rects(self):
        ...

    def compute_elements_positions(self):
        for element in self.elements:
            element.compute_elements_positions()
            element.populate_rects()

    def _compute_elements_surfaces_handle_width_case(self, element):
        if element.parent.type_flag == MesaRenderFlag.SLIDABLE_CONTAINER_HORIZONTAL:
            return element.parent.width // 2
        if element.parent.type_flag == MesaRenderFlag.SLIDABLE_CONTAINER_VERTICAL:
            return element.parent.width

        if element.width_flag == MesaRenderFlag.DISPLAY_WIDTH_WINDOW:
            return pg.display.get_window_size()[0]
        if element.width_flag == MesaRenderFlag.DISPLAY_WIDTH_PARENT:
            return element.parent.width
        if element.width_flag == MesaRenderFlag.DISPLAY_WIDTH_REMAIN:
            accum_width = 0
            for other_element in self.elements:
                if other_element == element:
                    continue
                else:
                    if (
                        other_element.width == MesaCoreFlag.NOT_DECLARED_ON_INIT
                        or other_element.width_flag
                        == MesaRenderFlag.DISPLAY_WIDTH_REMAIN
                    ):
                        raise ValueError(
                            "Could not build surface. No enough information was given [TWO LAYOUTS WITH NO DEFINED WIDTH]"
                        )
                    accum_width += other_element.width
            return element.parent.width - accum_width
        return element.width

    def _compute_elements_surfaces_handle_height_case(self, element):
        if element.parent.type_flag == MesaRenderFlag.SLIDABLE_CONTAINER_HORIZONTAL:
            return element.parent.height
        if element.parent.type_flag == MesaRenderFlag.SLIDABLE_CONTAINER_VERTICAL:
            return element.parent.height // 2
        if element.height_flag == MesaRenderFlag.DISPLAY_HEIGHT_WINDOW:
            return pg.display.get_window_size()[1]
        if element.height_flag == MesaRenderFlag.DISPLAY_HEIGHT_PARENT:
            return element.parent.height
        if element.height_flag == MesaRenderFlag.DISPLAY_HEIGHT_REMAIN:
            accum_height = 0
            for other_element in self.elements:
                if other_element == element:
                    continue
                else:
                    if (
                        other_element.height == MesaCoreFlag.NOT_DECLARED_ON_INIT
                        or other_element.height_flag
                        == MesaRenderFlag.DISPLAY_HEIGHT_REMAIN
                    ):
                        raise ValueError(
                            "Could not build surface. No enough information was given [TWO LAYOUTS WITH NO DEFINED HEIGHT]"
                        )
                    accum_height += other_element.height
            return element.parent.height - accum_height
        return element.height

    def compute_elements_surfaces(self):
        if self.surface_type == MesaCoreFlag.CORESURFACE:
            self.rect = pg.Rect(self.absolute_position, pg.display.get_window_size())
        else:
            self.rect = pg.Rect(self.absolute_position, self.surface.get_size())
            print(
                f"[DEBUG] Surface of size {self.surface.get_size()} has been made. Component: {self.__class__.__name__}"
            )

        for element in self.elements:
            element.height = self._compute_elements_surfaces_handle_height_case(element)
            element.width = self._compute_elements_surfaces_handle_width_case(element)

            element.surface = pg.Surface(
                [
                    element.width - 2 * element.margin,
                    element.height - 2 * element.margin,
                ],
                flags=pg.SRCALPHA,
            )

            if isinstance(element, _MesaContainer):
                element.compute_elements_surfaces()

    def compute_extra_inherit(self):
        for element in self.elements:
            element.compute_extra_inherit()

    def round_corners(self):
        if self.radius != MesaCoreFlag.NOT_DECLARED_ON_INIT:
            self.surface = rounded_border(self.surface, self.radius)

    def build(self):
        self.compute_elements_surfaces()
        self.compute_elements_positions()
        self.compute_extra_inherit()

    def set_as_core(self):
        self.position = pg.Vector2(0, 0)
        self.absolute_position = pg.Vector2(0, 0)
        self.width = pg.display.get_window_size()[0]
        self.height = pg.display.get_window_size()[1]
        self.surface_type = MesaCoreFlag.CORESURFACE
        self.rect = pg.Rect(self.absolute_position, pg.display.get_window_size())

    def set_position_as_core(self):
        self.position = pg.Vector2(0, 0)
        self.absolute_position = pg.Vector2(0, 0)

    def borderless(self):
        self.borders = [
            [False, None, None],
            [False, None, None],
            [False, None, None],
            [False, None, None],
        ]

    def border(self, color, thick):
        self.border_left(color, thick)
        self.border_right(color, thick)
        self.border_up(color, thick)
        self.border_down(color, thick)

    def border_left(self, color, thick):
        self.borders[0][0] = True
        self.borders[0][1] = thick
        self.borders[0][2] = color

    def border_right(self, color, thick):
        self.borders[1][0] = True
        self.borders[1][1] = thick
        self.borders[1][2] = color

    def border_up(self, color, thick):
        self.borders[2][0] = True
        self.borders[2][1] = thick
        self.borders[2][2] = color

    def border_down(self, color, thick):
        self.borders[3][0] = True
        self.borders[3][1] = thick
        self.borders[3][2] = color

    def set_size_as_display(self):
        self.width = pg.display.get_window_size()[0]
        self.height = pg.display.get_window_size()[1]

        self.surface = self.scene.core.display

    def set_height_as_display(self):
        self.height_flag = MesaRenderFlag.DISPLAY_HEIGHT_WINDOW

    def set_width_as_display(self):
        self.width_flag = MesaRenderFlag.DISPLAY_WIDTH_WINDOW

    def set_height_as_remaining_area(self):
        self.height_flag = MesaRenderFlag.DISPLAY_HEIGHT_REMAIN

    def set_width_as_remaining_area(self):
        self.width_flag = MesaRenderFlag.DISPLAY_WIDTH_REMAIN

    def set_height_as_parent(self):
        self.height_flag = MesaRenderFlag.DISPLAY_HEIGHT_PARENT

    def set_width_as_parent(self):
        self.width_flag = MesaRenderFlag.DISPLAY_WIDTH_PARENT

    def cover_parent_surface(self):
        self.set_height_as_parent()
        self.set_width_as_parent()

    def set_fixed_width(self, value):
        self.width = value

    def set_fixed_height(self, value):
        self.height = value

    def add_element(self, element):
        if isinstance(element, (_MesaContainer)):
            self.elements.append(element)
        else:
            raise ValueError(
                "Classes that are not Component or Containers cannot be added to a Container parent"
            )

    def update(self):
        ...

    def inherit_update(self):
        ...

    def __coreupdate__(self):
        if self.should_late_init:
            self.late_init()
            self.should_late_init = False
        self.update()
        self.inherit_update()
        for element in self.elements:
            element.__coreupdate__()

    def render(self):
        ...

    def inherit_render(self):
        ...

    def __corerender__(self):
        if self.background_color != None:
            if self.surface_type != MesaCoreFlag.CORESURFACE:
                self.surface.fill(self.background_color)

        self.render_borders()
        self.render()

        for element in self.elements:
            element.__corerender__()
        self.inherit_render()

        if self.scene.core.on_debug == False:
            if self.surface_type != MesaCoreFlag.CORESURFACE:
                self.surface.set_alpha(255)
                if self.parent.surface_type == MesaCoreFlag.CORESURFACE:
                    self.scene.core.display.blit(self.surface, self.position)
                else:
                    self.parent.surface.blit(self.surface, self.position)
        else:
            thick = 2

            if self.surface_type != MesaCoreFlag.CORESURFACE:
                pg.draw.rect(
                    self.surface,
                    self.debug_color,
                    self.surface.get_rect(),
                    thick,
                )
                self.surface.set_alpha(255)
                if self.parent.surface_type == MesaCoreFlag.CORESURFACE:
                    self.scene.core.display.blit(self.surface, self.position)
                else:
                    self.parent.surface.blit(self.surface, self.position)

    def render_borders(self):
        for index, border in enumerate(self.borders):
            if border[0] == False:
                continue
            else:
                if index == 0:
                    pg.draw.rect(
                        self.surface,
                        border[2],
                        pg.Rect(0, 0, border[1], self.surface.get_height()),
                    )
                if index == 1:
                    pg.draw.rect(
                        self.surface,
                        border[2],
                        pg.Rect(
                            self.surface.get_width() - border[1],
                            0,
                            self.surface.get_width() - border[1],
                            self.surface.get_height(),
                        ),
                    )
                if index == 2:
                    pg.draw.rect(
                        self.surface,
                        border[2],
                        pg.Rect(0, 0, self.surface.get_width(), border[1]),
                    )
                if index == 3:
                    pg.draw.rect(
                        self.surface,
                        border[2],
                        pg.Rect(
                            0,
                            self.surface.get_height() - border[1],
                            self.surface.get_width(),
                            border[1],
                        ),
                    )
