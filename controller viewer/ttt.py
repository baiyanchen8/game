import pygetwindow as gw
import pyautogui
import time

def get_xbox_controller_window():
    windows = gw.getWindowsWithTitle("Asus")
    if windows:
        return windows[0]
    return None

def read_xbox_controller_window(window):
    if window:
        print("Xbox 手柄視窗已找到！開始讀取資訊...")
        while True:
            window.activate()
            keys = pyautogui.keyInfo()
            print(f"按鈕狀態: {keys}")
            
            # 這裡你可以根據需要處理其他按鈕和軸值的資訊
            time.sleep(0.1)

if __name__ == "__main__":
    print("等待 Xbox 手柄視窗...")
    xbox_window = get_xbox_controller_window()
    while not xbox_window:
        xbox_window = get_xbox_controller_window()
        time.sleep(1)

    print("Xbox 手柄視窗已找到！開始讀取資訊...")
    read_xbox_controller_window(xbox_window)
