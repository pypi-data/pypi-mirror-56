# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from src.core import pycurses
from src.constant import doms, pairs, colors


class Dom(object):

    def __init__(self,
                 kind,
                 name='',
                 context=None,
                 position=doms.POSITION_STATIC,
                 begin_top=None,
                 begin_left=None,
                 display=doms.DISPLAY_INLINE,
                 width='100%',
                 height='100%',
                 padding=(0, 0, 0, 0),
                 margin=(0, 0, 0, 0),
                 text_blink=doms.CSS_UNSET,
                 text_decoration=doms.CSS_UNSET,
                 text_align=doms.TEXT_ALIGN_LEFT,
                 font_weight=doms.FONT_WEIGHT_NORMAL,
                 color=pairs.PAIR_THEME_FONT
                 ):
        self.kind = kind
        self.name = name
        self.context = context
        # 定位
        self._position = position
        self._begin_top = begin_top
        self._begin_left = begin_left
        # 显示
        self._display = display
        self._width = width
        self._height = height
        self._margin = margin
        self._padding = padding
        # 文本
        self._text_blink = text_blink
        self._text_decoration = text_decoration
        self._text_align = text_align
        self._font_weight = font_weight
        self._color = color

    def show(self, target=None, parent=None):
        for x in self.context:
            if not isinstance(x, Dom):
                raise pycurses.error('dom\'s context must be dom.')
            x.show(target=target, parent=self)

    def add_child(self, child, start_num=None):
        if not isinstance(child, Dom):
            raise pycurses.error('child must be dom.')
        if start_num is None:
            self.context.append(child)
        else:
            if not isinstance(start_num, int):
                raise pycurses.error('child_num must be int.')
            self.context.insert(start_num, child)

    def del_child(self, child_num):
        if not isinstance(child_num, int):
            raise pycurses.error('child_num must be int.')
        self.context.pop(child_num)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, display):
        self._display = display

    @property
    def font_weight(self):
        return self._font_weight

    @font_weight.setter
    def font_weight(self, font_weight):
        self._font_weight = font_weight

    @property
    def text_blink(self):
        return self._text_blink

    @text_blink.setter
    def text_blink(self, text_blink):
        self._text_blink = text_blink

    @property
    def text_decoration(self):
        return self._text_decoration

    @text_decoration.setter
    def text_decoration(self, text_decoration):
        self._text_decoration = text_decoration

    @property
    def text_align(self):
        return self._text_align

    @text_align.setter
    def text_align(self, text_align):
        self._display = text_align

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, margin):
        self._margin = margin

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, padding):
        self._padding = padding

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def begin_top(self):
        return self._begin_top

    @begin_top.setter
    def begin_top(self, begin_top):
        self._begin_top = begin_top

    @property
    def begin_left(self):
        return self._begin_left

    @begin_left.setter
    def begin_left(self, begin_left):
        self._begin_left = begin_left
