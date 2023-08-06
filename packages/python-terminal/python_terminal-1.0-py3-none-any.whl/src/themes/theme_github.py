# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from src.themes.theme import Theme
from src.constant import colors


class GithubTheme(Theme):

    def __init__(self, cur):
        super().__init__(
            cur=cur,
            theme_bg=colors.SYSTEM_WHITE_FFFFFF,
            theme_font=colors.GREY_4E4E4E
        )
