# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from curses import *
import re


# 终端允许的颜色数量
COLORS = 256


# redefine init_pair
# init_pair的pair_number被拆分段:
# 0             固定值
# 1-50          模板
# 51-100        ui库
# 101-254       其他
# 255           固定值
def init_theme_pair(number, fg, bg):
    if not 1 <= number < 51:
        raise error('theme pair must be in 1-50.')
    init_pair(number, fg, bg)


def init_ui_pair(number, fg, bg):
    if not 51 <= number < 101:
        raise error('ui pair must be in 51-100.')
    init_pair(number, fg, bg)


# redefine init_color， curses的参数范围是0-1000， 需要转成rgb的0-255
def init_rgb_color_255(color_number, r, g, b):
    init_color(color_number, int(r*1000 / 255), int(g*1000 / 255), int(b*1000 / 255))


# change 100% to int
def int_from_100(value, max_value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        value.strip()
        if value.isdigit():
            return int(value)
        reg = re.compile(r'^([0-9.]+)[ ]*%$')
        if reg.match(value):
            return int(int(value[:-1]) / 100) * max_value
    raise error('error value')
