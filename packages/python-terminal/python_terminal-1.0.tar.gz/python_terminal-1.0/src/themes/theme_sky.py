# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from src.themes.theme import Theme
from src.constant import colors


class SkyTheme(Theme):

    def __init__(self, cur):
        super().__init__(
            cur=cur,
            theme_bg=colors.SKY_BLUE_5FAFD7,
            theme_font=colors.SYSTEM_WHITE_FFFFFF
        )
