# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from src import Window
from src.core import pycurses
from src.constant import doms, pairs
from .dom import Dom


class WindowDom(Dom):

    def __init__(self,
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
        context = list() if context is None else context
        super().__init__(
            kind=doms.DOM_KIND_WINDOW,
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
        window = Window(height=10, width=20, begin_top=20, begin_left=40)
        # window = pycurses.newwin(10, 20, 20, 20)
        for x in self.context:
            if not isinstance(x, Dom):
                raise pycurses.error('dom\'s context must be dom.')
            x.show(target=window, parent=self)
        window.refresh()

