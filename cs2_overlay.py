"""
CS2 Anti-Flashbang — оверлей через mss + pywin32
Установка: python -m pip install mss numpy pywin32
Запуск:    python3 cs2_overlay.py  (от имени администратора)
"""
import sys, time, ctypes, threading
import numpy as np

try:
    import mss
    import win32api, win32con, win32gui
except ImportError as e:
    print(f"Установи: python -m pip install mss numpy pywin32")
    print(f"Ошибка: {e}"); input(); sys.exit(1)

if sys.platform != "win32": sys.exit(1)

WHITE_THRESHOLD = 255
HOLD_DURATION   = 1
CAPTURE_SIZE    = 300   # захватываем 50x50 в центре

_running  = True
_is_black = False
_hwnd     = None
_sw       = 0
_sh       = 0

def create_overlay():
    global _hwnd, _sw, _sh
    _sw = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    _sh = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    wc = win32gui.WNDCLASS()
    wc.hInstance     = win32api.GetModuleHandle(None)
    wc.lpszClassName = "CS2AF"
    wc.lpfnWndProc   = {win32con.WM_DESTROY: lambda h,m,w,l: win32gui.PostQuitMessage(0)}
    try:
        win32gui.RegisterClass(wc)
    except Exception:
        pass

    _hwnd = win32gui.CreateWindowEx(
        win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT |
        win32con.WS_EX_TOPMOST | win32con.WS_EX_TOOLWINDOW,
        "CS2AF", "CS2AF", win32con.WS_POPUP,
        0, 0, _sw, _sh, 0, 0, wc.hInstance, None
    )
    win32gui.SetLayeredWindowAttributes(_hwnd, 0, 0, win32con.LWA_ALPHA)
    win32gui.ShowWindow(_hwnd, win32con.SW_SHOW)
    win32gui.UpdateWindow(_hwnd)
    return _hwnd

def set_black(black: bool):
    global _is_black
    if _is_black == black:
        return
    _is_black = black
    if black:
        hdc   = win32gui.GetDC(_hwnd)
        brush = win32gui.CreateSolidBrush(0x00000000)
        win32gui.FillRect(hdc, (0, 0, _sw, _sh), brush)
        win32gui.DeleteObject(brush)
        win32gui.ReleaseDC(_hwnd, hdc)
        win32gui.SetLayeredWindowAttributes(_hwnd, 0, 255, win32con.LWA_ALPHA)
    else:
        win32gui.SetLayeredWindowAttributes(_hwnd, 0, 0, win32con.LWA_ALPHA)
    win32gui.UpdateWindow(_hwnd)

def capture_loop():
    global _running
    cx   = _sw // 2
    cy   = _sh // 2
    h    = CAPTURE_SIZE // 2
    region = {"left": cx-h, "top": cy-h, "width": CAPTURE_SIZE, "height": CAPTURE_SIZE}

    hold_until = 0.0
    is_black   = False

    with mss.mss() as sct:
        while _running:
            img    = sct.grab(region)
            frame  = np.frombuffer(img.raw, dtype=np.uint8).reshape((CAPTURE_SIZE, CAPTURE_SIZE, 4))
            white  = np.all(frame[:,:,:3] >= WHITE_THRESHOLD, axis=2)
            ratio  = white.mean()
            now    = time.monotonic()

            if not is_black:
                if ratio >= 0.90:
                    set_black(True)
                    is_black   = True
                    hold_until = now + HOLD_DURATION
                    print(f"[{time.strftime('%H:%M:%S')}] ВКЛ ⚡")
            else:
                if now >= hold_until and ratio < 0.30:
                    set_black(False)
                    is_black = False
                    print(f"[{time.strftime('%H:%M:%S')}] ВЫКЛ ✓")

def main():
    global _running
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Запусти от имени администратора!"); input(); sys.exit(1)

    print("=" * 55)
    print("  CS2 Anti-Flashbang  |  оверлей")
    print("=" * 55)
    print(f"  Порог  : >= {WHITE_THRESHOLD}/255")
    print(f"  Захват : {CAPTURE_SIZE}x{CAPTURE_SIZE} px в центре")
    print("  Ctrl+C для выхода")
    print("-" * 55)

    create_overlay()
    print(f"  Оверлей создан: {_sw}x{_sh}")

    t = threading.Thread(target=capture_loop, daemon=True)
    t.start()
    print("  Готов! Запускай CS2 в Fullscreen Windowed.\n")

    try:
        while _running:
            win32gui.PumpWaitingMessages()
            time.sleep(0.001)
    except KeyboardInterrupt:
        pass

    _running = False
    set_black(False)
    try:
        win32gui.DestroyWindow(_hwnd)
    except Exception:
        pass
    print("\n  Готово!")

if __name__ == "__main__":
    main()
