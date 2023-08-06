# -*- coding: utf-8 -*-
from src.core import pycurses
from src.themes.theme_github import GithubTheme
from src.constant import colors


class Window(object):
    def __init__(self, height='100%', width='100%', begin_top=0, begin_left=0):
        self.window = pycurses.newwin(height, width, begin_top, begin_left)

    def refresh(self):
        self.window.refresh()
