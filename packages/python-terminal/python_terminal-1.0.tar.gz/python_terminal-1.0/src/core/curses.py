# -*- coding: utf-8 -*-
from src.core import pycurses
from src.themes.theme_github import GithubTheme
from src.constant import colors


class Curses(object):
    def __init__(self, noecho=True, cbreak=True):
        # 初始化实例
        self.stdscr = pycurses.initscr()
        self.stdscr_max_height, self.stdscr_max_width = self.stdscr.getmaxyx()
        pycurses.curs_set(0)
        pycurses.start_color()
        pycurses.use_default_colors()
        # 模板
        self._theme = GithubTheme(cur=self)
        # 通常 curses 会关闭屏幕回显，保证只在特定条件下才会读取键盘输入并显示。这需要调用 noecho()方法
        if noecho:
            pycurses.noecho()
        # 应用程序通常需要对键盘输入立即做出响应，而不需要特意的按下回车键；这叫做 cbreak 模式，与之对应的是常用的缓冲输入模式。
        if cbreak:
            pycurses.cbreak()
        # 终端通常返回特殊键作为多字节转义序列，比如光标键、Home键、Page Up等， curses 可以让你的程序根据转义序列执行相应的代码。让 curses 可以响应这些特殊值，需要开启 keypad 模式。
        self.stdscr.keypad(True)

    def __del__(self):
        # 结束一个 curses 应用
        pycurses.nocbreak()
        pycurses.echo()
        # 为了恢复 curses 的终端设置。调用 endwin() 方法重置为原来的操作模式
        pycurses.endwin()

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, theme):
        self._theme = theme(cur=self)

    def refresh(self):
        self.stdscr.refresh()

    def init_color(self):
        if pycurses.can_change_color():
            self.stdscr.addstr('can change')
            pycurses.init_color(colors.GREY_808080, 255, 0, 0)
            pycurses.init_color(colors.CORNSILK_FFFFD7, 253, 246, 227)
        else:
            self.stdscr.addstr('can not change')
