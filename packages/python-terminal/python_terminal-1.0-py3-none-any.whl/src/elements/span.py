# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from src.core import pycurses
from src.constant import doms, pairs
from src.elements import Dom
from src import Curses, Window


class SpanDom(Dom):

    def __init__(self,
                 name='',
                 context='',
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
        context = str(context) if isinstance(context, int) else context
        if not isinstance(context, str):
            raise pycurses.error('span\'s context must be str.')
        super().__init__(
            kind=doms.DOM_KIND_SPAN,
            name=name,
            context=context,
            position=position,
            begin_top=begin_top,
            begin_left=begin_left,
            display=display,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            text_blink=text_blink,
            text_decoration=text_decoration,
            text_align=text_align,
            font_weight=font_weight,
            color=color
        )

    def show(self, target=None, parent=None):
        attrs = 0
        context = self.context
        if self.display == doms.DISPLAY_BLOCK:
            context = context + '\n'
        if self.font_weight == doms.FONT_WEIGHT_BOLD:
            attrs += pycurses.A_BOLD
        if self.text_blink == doms.TEXT_DECORATION_BLINK:
            attrs += pycurses.A_BLINK
        if self.text_decoration == doms.TEXT_DECORATION_UNDERLINE:
            attrs += pycurses.A_UNDERLINE
        attrs += pycurses.color_pair(self.color)
        if isinstance(target, Curses):
            target.stdscr.addstr('{}'.format(context), attrs)
        if isinstance(target, Window):
            target.window.addstr('{}'.format(context), attrs)

    def add_child(self, child, start_num=None):
        child = str(child) if isinstance(child, int) else child
        if not isinstance(child, str):
            raise pycurses.error('span\'s child must be str.')
        if start_num is None:
            self.context = self.context + child
        else:
            if not isinstance(start_num, int):
                raise pycurses.error('child_num must be int.')
            self.context = self.context[: start_num] + child + self.context[start_num:]

    def del_child(self, child_num):
        if not isinstance(child_num, int):
            raise pycurses.error('child_num must be int.')
        self.context = self.context.replace(child_num, "", 1)

    def __str__(self):
        return self.context
