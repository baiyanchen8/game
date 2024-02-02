import pygame as pg
import win32gui
import win32con
import sys

pg.init()

# 設定顯示器
screen = pg.display.set_mode((400, 300), flags=pg.NOFRAME)  # 使用 pg.NOFRAME 設置為無邊框窗口
pg.display.set_caption("始終置頂示例")

# 取得視窗的 HWND
hwnd = pg.display.get_wm_info()["window"]

# 設定視窗始終置頂
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()
