# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from src.themes.theme import Theme
from src.constant import colors
from src.core import pycurses


class SolarizedDarkTheme(Theme):

    def __init__(self, cur):
        self.init_color()
        super().__init__(
            cur=cur,
            theme_bg=colors.BLUE_005F5F,
            theme_font=colors.CORNSILK_FFFFD7,
            theme_primary=colors.BLUE_005F5F,
            theme_success=colors.GREEN_00875F,
            theme_info=colors.CORNSILK_FFFFD7,
            theme_warning=colors.DARK_ORANGE_AF5F00,
            theme_error=colors.RED_AF0000
        )

    @staticmethod
    def init_color():
        if pycurses.can_change_color():
            pycurses.init_rgb_color_255(colors.BLUE_005F5F, 0, 43, 54)
            pycurses.init_rgb_color_255(colors.CORNSILK_FFFFD7, 253, 246, 227)
            pycurses.init_rgb_color_255(colors.GREEN_00875F, 133, 153, 0)
            pycurses.init_rgb_color_255(colors.DARK_ORANGE_AF5F00, 203, 75, 22)
            pycurses.init_rgb_color_255(colors.RED_AF0000, 211, 1, 2)
