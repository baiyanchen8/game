import os
import pygame as pg
import sys
import threading
import win32api
import win32con
import win32gui
import ctypes

from method.draw_text import *
from method.img_path import *

def main_thread():
    pg.init()
    # 取得螢幕的寬度和高度
    screen_height = pg.display.Info().current_h

    # 設定顯示器位置為左下方
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (80, screen_height - 350)
    # 初始化手把
    pg.joystick.init()
    joystick_count = pg.joystick.get_count()
    
    if joystick_count > 0:
        # 選擇第一個手把
        joystick = pg.joystick.Joystick(0)
        joystick.init()

        print("手把名稱:", joystick.get_name())
        print("手把數量:", joystick_count)

        # 設定顯示器
        screen = pg.display.set_mode((320, 270), pg.NOFRAME)  # 使用 pg.NOFRAME 設置為無邊框窗口
        pg.display.set_caption("手把狀態顯示器")

        # 導入圖片
        controller_image_path = pic["controller"]  
        controller_image = pg.image.load(controller_image_path).convert_alpha()

        lt_frame_path = pic["lt_frame"]  
        lt_frame_image = pg.image.load(lt_frame_path).convert_alpha()
        
        rt_frame_path = pic["rt_frame"]  
        rt_frame_image = pg.image.load(rt_frame_path).convert_alpha()

        # 設定新的圖片大小
        new_width = 300
        new_height = 200

        # 調整圖片大小
        resized_controller_image = pg.transform.scale(controller_image, (new_width, new_height))
        resized_lt_frame_image = pg.transform.scale(lt_frame_image, (60, 65))
        resized_rt_frame_image = pg.transform.scale(rt_frame_image, (60, 65))

        lt_percentage = -1
        rt_percentage = -1
        fuchsia = (0, 0, 0)  # Transparency color

        hwnd = pg.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
        
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        # 設定該視窗不搶占焦點
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        buttonlist = ["a", "b", "x", 'y', "lb", "rb"]
        buttonstate = [0, 0, 0, 0, 0, 0]  

        clock = pg.time.Clock()  # 創建時間迴圈物件
        while True:
            pg.event.pump()  # 處理事件
            print(1)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.JOYBUTTONDOWN:
                    print("press:", event.button)
                    try:
                        buttonstate[event.button] = 1
                    except:
                        pass
                elif event.type == pg.JOYBUTTONUP:
                    print("up:", event.button)
                    try:
                        buttonstate[event.button] = 0
                    except:
                        pass
                elif event.type == pg.JOYAXISMOTION:
                    print("axis:", event.axis, "value:", event.value)
                    if event.axis == 5:
                        rt_percentage = event.value
                    elif event.axis == 4:
                        lt_percentage = event.value

            # 清除顯示器
            screen.fill(fuchsia) 
            # 顯示手把圖片
            screen.blit(resized_controller_image, (10, 70))
            h = 70  # 設定填充的起始高度
            ph = 5
            # 左搖桿背景
            joystick_bg_pos = (85, 130)
            joystick_bg_radius = 17
            pg.draw.circle(screen, (250, 250, 250), joystick_bg_pos, joystick_bg_radius)

            # 左搖桿實際位置
            joystick_x = int(joystick.get_axis(0) * 17)  
            joystick_y = int(joystick.get_axis(1) * 17)  
            joystick_pos = (joystick_bg_pos[0] + joystick_x, joystick_bg_pos[1] + joystick_y)

            # 顯示左搖桿實際位置
            pg.draw.circle(screen, (0, 0, 255), joystick_pos, 10)
            
            # 顯示 LT 外框和填充
            screen.blit(resized_lt_frame_image, (60, ph))
            lt_width = 65 - int(lt_percentage * 65)
            lt_height = min(65, max(0, lt_width)) 
            lt_fill_rect = pg.Rect(60, ph, 60, lt_height)
            screen.blit(resized_lt_frame_image, (60, ph), special_flags=pg.BLEND_RGBA_MULT)
            pg.draw.rect(screen, (0, 0, 0), lt_fill_rect)

            # 顯示 RT 外框和填充
            screen.blit(resized_rt_frame_image, (210, ph))
            rt_width = 65 - int(rt_percentage * 65)
            rt_height = min(65, max(0, rt_width)) 
            rt_fill_rect = pg.Rect(210, ph, 60, rt_height)
            screen.blit(resized_rt_frame_image, (210, ph), special_flags=pg.BLEND_RGBA_MULT)
            pg.draw.rect(screen, (0, 0, 0), rt_fill_rect)

            # 按鈕顯示
            button_position = [(239, 151), (), (), (239, 111), (), ()]
            buttonlist = ["a", "b", "x", 'y', "lb", "rb"]
            button_radius = 11
            if buttonstate[0] == 1:
                pg.draw.circle(screen, (250, 250, 250), button_position[0], button_radius)
            elif buttonstate[3] == 1:
                pg.draw.circle(screen, (250, 250, 250), button_position[3], button_radius)
            pg.display.flip()
            clock.tick(60)  # 控制每秒迴圈執行次數，保持遊戲順暢

    else:
        print("找不到手把")

# 創建後台執行緒
thread = threading.Thread(target=main_thread)
thread.start()


