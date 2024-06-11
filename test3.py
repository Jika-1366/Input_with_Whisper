import ctypes
from ctypes import wintypes
import time

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
HC_ACTION = 0

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG),
    ]

def low_level_keyboard_proc(nCode, wParam, lParam):
    if nCode == HC_ACTION and wParam == WM_KEYDOWN:
        kbDllHookStruct = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        vk_code = kbDllHookStruct.vkCode
        if vk_code == 32:  # Space key
            if kbDllHookStruct.flags & 0x20:  # Check if Shift key is pressed
                print("全角スペースが入力されました")
            else:
                print("半角スペースが入力されました")
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

hook = user32.SetWindowsHookExW(
    WH_KEYBOARD_LL,
    low_level_keyboard_proc,
    kernel32.GetModuleHandleW(None),
    0 
)

if hook == 0:
    print("フックの設置に失敗しました。")
else:
    msg = wintypes.MSG()
    while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageA(ctypes.byref(msg))

    user32.UnhookWindowsHookEx(hook)