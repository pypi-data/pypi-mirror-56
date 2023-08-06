
class TerminalCode(object):

    PRINT_CLOSE_ATTRS = '\33[0m'                  # 关闭所有属性
    PRINT_LINE_HEIGHT = '\33[1m'                  # 设置高亮度
    PRINT_UNDERLINE = '\33[4m'                    # 下划线
    PRINT_FLICKER = '\33[5m'                      # 闪烁
    PRINT_REVERT = '\33[7m'                       # 反显
    PRINT_BLANKING = '\33[8m'                     # 消隐
    PRINT_CLEAR = '\33[2J'                        # 清屏
    PRINT_HIDE_CURSOR = '\33[?25l'                # 隐藏光标
    PRINT_SHOW_CURSOR = '\33[?25h'                # 显示光标
    PRINT_SAVE_CURSOR = '\33[s'                   # 保存光标位置
    PRINT_RECOVER_CURSOR = '\33[u'                # 恢复光标位置
    PRINT_DE = '\33[K'                            # 清除从光标到行尾的内容 VIM DE
    PRINT_F_COLOR_BLACK = '\33[30m'               # 设置前景色: 黑
    PRINT_F_COLOR_RED = '\33[31m'                 # 设置前景色: 红
    PRINT_F_COLOR_GREEN = '\33[32m'               # 设置前景色: 绿
    PRINT_F_COLOR_YELLOW = '\33[33m'              # 设置前景色: 黄
    PRINT_F_COLOR_DARK_BLUE = '\33[34m'           # 设置前景色: 蓝色
    PRINT_F_COLOR_DARK_PURPLE = '\33[35m'         # 设置前景色: 紫色
    PRINT_F_COLOR_DARK_GREEN = '\33[36m'          # 设置前景色: 深绿
    PRINT_F_COLOR_WHITE = '\33[37m'               # 设置前景色: 白色

    PRINT_B_COLOR_BLACK = '\33[40m'               # 设置背景色: 黑
    PRINT_B_COLOR_DARK_RED = '\33[41m'            # 设置背景色: 深红
    PRINT_B_COLOR_GREEN = '\33[42m'               # 设置背景色: 绿
    PRINT_B_COLOR_YELLOW = '\33[43m'              # 设置背景色: 黄色
    PRINT_B_COLOR_BLUE = '\33[44m'                # 设置背景色: 蓝色
    PRINT_B_COLOR_PURPLE = '\33[45m'              # 设置背景色: 紫色
    PRINT_B_COLOR_DARK_GREEN = '\33[46m'          # 设置背景色: 深绿
    PRINT_B_COLOR_WHITE = '\33[47m'               # 设置背景色: 白色

    PRINT_C_COLOR_BLACK = '\33[90m'               # 黑底彩色: 黑
    PRINT_C_COLOR_DARK_RED = '\33[91m'            # 黑底彩色: 深红
    PRINT_C_COLOR_GREEN = '\33[92m'               # 黑底彩色: 绿
    PRINT_C_COLOR_DARK_YELLOW = '\33[93m'         # 黑底彩色: 黄色
    PRINT_C_COLOR_DARK_BLUE = '\33[94m'           # 黑底彩色: 蓝色
    PRINT_C_COLOR_DARK_PURPLE = '\33[95m'         # 黑底彩色: 紫色
    PRINT_C_COLOR_DARK_GREEN = '\33[96m'          # 黑底彩色: 深绿
    PRINT_C_COLOR_WHITE = '\33[97m'               # 黑底彩色: 白色

    # 光标上移n行
    @staticmethod
    def cursor_up(n):
        print('\33[{}A'.format(n))

    # 光标下移n行
    @staticmethod
    def cursor_down(n):
        print('\33[{}B'.format(n))

    # 光标右移n行
    @staticmethod
    def cursor_right(n):
        print('\33[{}C'.format(n))

    # 光标左移n行
    @staticmethod
    def cursor_left(n):
        print('\33[{}D'.format(n))

    # 设置光标位置
    @staticmethod
    def cursor_set(x, y):
        print('\33[y;xH'.format(y, x))


tp = TerminalCode()
