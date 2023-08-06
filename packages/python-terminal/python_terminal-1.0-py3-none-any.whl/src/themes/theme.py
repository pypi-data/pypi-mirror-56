# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from src.core import pycurses
from src.constant import pairs, colors


class Theme(object):

    def __init__(
            self,
            cur,
            theme_bg=colors.SYSTEM_WHITE_FFFFFF,
            theme_font=colors.SYSTEM_BLACK_000000,
            theme_primary=colors.SYSTEM_BLACK_000000,
            theme_success=colors.SYSTEM_GREEN_008000,
            theme_info=colors.SYSTEM_SILVER_C0C0C0,
            theme_warning=colors.SYSTEM_YELLOW_FFFF00,
            theme_error=colors.SYSTEM_RED_FF0000
    ):
        self.cur = cur
        self.theme_bg = theme_bg
        self.theme_font = theme_font
        self.theme_primary = theme_primary
        self.theme_success = theme_success
        self.theme_info = theme_info
        self.theme_warning = theme_warning
        self.theme_error = theme_error
        self.set_color()

    # set terminal background color
    def set_color(self):
        pycurses.init_theme_pair(pairs.PAIR_THEME_BG, self.theme_font, self.theme_bg)
        self.cur.stdscr.bkgd(' ', pycurses.color_pair(pairs.PAIR_THEME_BG))
        pycurses.init_theme_pair(pairs.PAIR_THEME_FONT, self.theme_font, self.theme_bg)
        pycurses.init_theme_pair(pairs.PAIR_THEME_PRIMARY, self.theme_primary, self.theme_bg)
        pycurses.init_theme_pair(pairs.PAIR_THEME_SUCCESS, self.theme_success, self.theme_bg)
        pycurses.init_theme_pair(pairs.PAIR_THEME_WARNING, self.theme_warning, self.theme_bg)
        pycurses.init_theme_pair(pairs.PAIR_THEME_ERROR, self.theme_error, self.theme_bg)


    @staticmethod
    def init_color():
        # curses provide 256 colors, if you want to replace it
        # 1. assess can_change_color
        # 2. select nearest color from constant.colors, replace it to the color you want
        # 3. and use this func when initialize
        # if pycurses.can_change_color():
        #     pycurses.init_rgb_color_255(colors.GREY_808080, 0, 43, 54)
        raise pycurses.error('rewrite it.')
