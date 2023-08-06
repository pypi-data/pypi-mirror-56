from enum import Enum
import win32api
import win32con
import win32gui
import time

__version__ = '0.0.1'


class VK(Enum):
    """键盘虚拟码"""
    #定义键盘虚拟码 https://docs.microsoft.com/zh-cn/windows/win32/inputdev/virtual-key-codes
    VK_LBUTTON = 0x01  # Left mouse button
    VK_RBUTTON = 0x02  # Right mouse button
    VK_CANCEL = 0x03  # Control-break processing
    VK_MBUTTON = 0x04  # Middle mouse button (three-button mouse)
    VK_XBUTTON1 = 0x05  # X1 mouse button
    VK_XBUTTON2 = 0x06  # X2 mouse button
    VK_BACK = 0x08  # BACKSPACE key
    VK_TAB = 0x09  # TAB key
    VK_CLEAR = 0x0C  # CLEAR key
    VK_ENTER = 0x0D  # ENTER key
    VK_SHIFT = 0x10  # SHIFT key
    VK_CONTROL = 0x11  # CTRL key
    VK_MENU = 0x12  # ALT key
    VK_PAUSE = 0x13  # PAUSE key
    VK_CAPITAL = 0x14  # CAPS LOCK key
    VK_KANA = 0x15  # IME Kana mode
    VK_HANGUEL = 0x15
    VK_HANGUL = 0x15  # IME Hangul mode
    VK_JUNJA = 0x17  # IME Junja mode
    VK_FINAL = 0x18  # IME final mode
    VK_HANJA = 0x19  # IME Hanja mode
    VK_KANJI = 0x19  # IME Kanji mode
    VK_ESCAPE = 0x1B  # ESC key
    VK_CONVERT = 0x1C  # IME convert
    VK_NONCONVERT = 0x1D  # IME nonconvert
    VK_ACCEPT = 0x1E  # IME accept
    VK_MODECHANGE = 0x1F  # IME mode change request
    VK_SPACE = 0x20  # SPACEBAR
    VK_PRIOR = 0x21  # PAGE UP key
    VK_NEXT = 0x22  # PAGE DOWN key
    VK_END = 0x23  # END key
    VK_HOME = 0x24  # HOME key
    VK_LEFT = 0x25  # LEFT ARROW key
    VK_UP = 0x26  # UP ARROW key
    VK_RIGHT = 0x27  # RIGHT ARROW key
    VK_DOWN = 0x28  # DOWN ARROW key
    VK_SELECT = 0x29  # SELECT key
    VK_PRINT = 0x2A  # PRINT key
    VK_EXECUTE = 0x2B  # EXECUTE key
    VK_SNAPSHOT = 0x2C  # PRINT SCREEN key
    VK_INSERT = 0x2D  # INS key
    VK_DELETE = 0x2E  # DEL key
    VK_HELP = 0x2F  # HELP key
    VK_LWIN = 0x5B  # Left Windows key (Natural keyboard)
    VK_RWIN = 0x5C  # Right Windows key (Natural keyboard)
    VK_APPS = 0x5D  # Applications key (Natural keyboard)
    VK_SLEEP = 0x5F  # Computer Sleep key
    VK_NUMPAD0 = 0x60  # Numeric keypad 0 key
    VK_NUMPAD1 = 0x61  # Numeric keypad 1 key
    VK_NUMPAD2 = 0x62  # Numeric keypad 2 key
    VK_NUMPAD3 = 0x63  # Numeric keypad 3 key
    VK_NUMPAD4 = 0x64  # Numeric keypad 4 key
    VK_NUMPAD5 = 0x65  # Numeric keypad 5 key
    VK_NUMPAD6 = 0x66  # Numeric keypad 6 key
    VK_NUMPAD7 = 0x67  # Numeric keypad 7 key
    VK_NUMPAD8 = 0x68  # Numeric keypad 8 key
    VK_NUMPAD9 = 0x69  # Numeric keypad 9 key
    VK_MULTIPLY = 0x6A  # Multiply key
    VK_ADD = 0x6B  # Add key
    VK_SEPARATOR = 0x6C  # Separator key
    VK_SUBTRACT = 0x6D  # Subtract key
    VK_DECIMAL = 0x6E  # Decimal key
    VK_DIVIDE = 0x6F  # Divide key
    VK_F1 = 0x70  # F1 key
    VK_F2 = 0x71  # F2 key
    VK_F3 = 0x72  # F3 key
    VK_F4 = 0x73  # F4 key
    VK_F5 = 0x74  # F5 key
    VK_F6 = 0x75  # F6 key
    VK_F7 = 0x76  # F7 key
    VK_F8 = 0x77  # F8 key
    VK_F9 = 0x78  # F9 key
    VK_F10 = 0x79  # F10 key
    VK_F11 = 0x7A  # F11 key
    VK_F12 = 0x7B  # F12 key
    VK_F13 = 0x7C  # F13 key
    VK_F14 = 0x7D  # F14 key
    VK_F15 = 0x7E  # F15 key
    VK_F16 = 0x7F  # F16 key
    VK_F17 = 0x80  # F17 key
    VK_F18 = 0x81  # F18 key
    VK_F19 = 0x82  # F19 key
    VK_F20 = 0x83  # F20 key
    VK_F21 = 0x84  # F21 key
    VK_F22 = 0x85  # F22 key
    VK_F23 = 0x86  # F23 key
    VK_F24 = 0x87  # F24 key
    VK_NUMLOCK = 0x90  # NUM LOCK key
    VK_SCROLL = 0x91  # SCROLL LOCK key = 0x92-96
    VK_LSHIFT = 0xA0  # Left SHIFT key
    VK_RSHIFT = 0xA1  # Right SHIFT key
    VK_LCONTROL = 0xA2  # Left CONTROL key
    VK_RCONTROL = 0xA3  # Right CONTROL key
    VK_LMENU = 0xA4  # Left MENU key
    VK_RMENU = 0xA5  # Right MENU key
    VK_BROWSER_BACK = 0xA6  # Browser Back key
    VK_BROWSER_FORWARD = 0xA7  # Browser Forward key
    VK_BROWSER_REFRESH = 0xA8  # Browser Refresh key
    VK_BROWSER_STOP = 0xA9  # Browser Stop key
    VK_BROWSER_SEARCH = 0xAA  # Browser Search key
    VK_BROWSER_FAVORITES = 0xAB  # Browser Favorites key
    VK_BROWSER_HOME = 0xAC  # Browser Start and Home key
    VK_VOLUME_MUTE = 0xAD  # Volume Mute key
    VK_VOLUME_DOWN = 0xAE  # Volume Down key
    VK_VOLUME_UP = 0xAF  # Volume Up key
    VK_MEDIA_NEXT_TRACK = 0xB0  # Next Track key
    VK_MEDIA_PREV_TRACK = 0xB1  # Previous Track key
    VK_MEDIA_STOP = 0xB2  # Stop Media key
    VK_MEDIA_PLAY_PAUSE = 0xB3  # Play/Pause Media key
    VK_LAUNCH_MAIL = 0xB4  # Start Mail key
    VK_LAUNCH_MEDIA_SELECT = 0xB5  # Select Media key
    VK_LAUNCH_APP1 = 0xB6  # Start Application 1 key
    VK_LAUNCH_APP2 = 0xB7  # Start Application 2 key
    VK_OEM_1 = 0xBA
    VK_OEM_PLUS = 0xBB  # For any country/region, the '+' key
    VK_OEM_COMMA = 0xBC  # For any country/region, the ',' key
    VK_OEM_MINUS = 0xBD  # For any country/region, the '-' key
    VK_OEM_PERIOD = 0xBE  # For any country/region, the '.' key
    VK_OEM_2 = 0xBF  # Used for miscellaneous characters
    VK_OEM_3 = 0xC0  # Used for miscellaneous characters
    VK_OEM_4 = 0xDB  # Used for miscellaneous characters
    VK_OEM_5 = 0xDC  # Used for miscellaneous characters
    VK_OEM_6 = 0xDD  # Used for miscellaneous characters
    VK_OEM_7 = 0xDE  # Used for miscellaneous characters
    VK_OEM_8 = 0xDF  # Used for miscellaneous characters
    VK_OEM_102 = 0xE2
    VK_PROCESSKEY = 0xE5  # IME PROCESS key = 0xE6
    VK_PACKET = 0xE7
    VK_ATTN = 0xF6  # Attn key
    VK_CRSEL = 0xF7  # CrSel key
    VK_EXSEL = 0xF8  # ExSel key
    VK_EREOF = 0xF9  # Erase EOF key
    VK_PLAY = 0xFA  # Play key
    VK_ZOOM = 0xFB  # Zoom key
    VK_NONAME = 0xFC  # Reserved
    VK_PA1 = 0xFD  # PA1 key
    VK_OEM_CLEAR = 0xFE  # Clear key


class KM(object):
    """键盘鼠标操作"""

    # 定义键盘虚拟码 https://docs.microsoft.com/zh-cn/windows/win32/inputdev/virtual-key-codes
    _vk = {
        # 26个字母
        "a": 0x41, "b": 0x42, "c": 0x43, "d": 0x44, "e": 0x45, "f": 0x46, "g": 0x47, "h": 0x48, "i": 0x49, "j": 0x4A, "k": 0x4B, "l": 0x4C, "m": 0x4D,
        "n": 0x4E, "o": 0x4F, "p": 0x50, "q": 0x51, "r": 0x52, "s": 0x53, "t": 0x54, "u": 0x55, "v": 0x56, "w": 0x57, "x": 0x58, "y": 0x59, "z": 0x5A,
        # 数字键
        "0": 0x60, "1": 0x61, "2": 0x62, "3": 0x63, "4": 0x64, "5": 0x65, "6": 0x66, "7": 0x67, "8": 0x68, "9": 0x69,
        # oem
        ',': 0xBC, '.': 0xBE, '-': 0xBD, '[': 0xDB, ']': 0xDD, ';': 0xBA, "'": 0xDE, '\\': 0xDC, ',': 0xbc, '`': 0xC0, '=': 0xBB, '/': 0xBF
    }

    _vk_2 = {
        '~': 0xC0, '!': 0x31, '@': 0x32, '#': 0x33, '$': 0x34, '%': 0x35, '^': 0x36, '&': 0x37, '*': 0x38, '(': 0x39, ')': 0x30,
        '+': 0xBB, '_': 0xBD, '{': 0xDB, '}': 0xDD,  ':': 0xBA, '"': 0xDE, '|': 0xDC, '<': 0xbc, '>': 0xbe, '?': 0xBF,
    }

    def keyboard(self, text, delayed=0.0):
        if type(text) == VK:
            self.keyDown(text.value)
            time.sleep(delayed)
            self.keyUp(text.value)
            return None
        for t in str(text):
            if t in self._vk_2.keys():
                vk_code = self._vk_2.get(t)
                self.keyDown(0x10)
                self.keyDown(vk_code)
                self.keyUp(vk_code)
                self.keyUp(0x10)
            elif t in self._vk.keys():
                vk_code = self._vk.get(t)
                self.keyDown(vk_code)
                self.keyUp(vk_code)
            elif t.lower() in self._vk.keys():
                vk_code = self._vk.get(t.lower())
                self.keyDown(0x10)
                self.keyDown(vk_code)
                self.keyUp(vk_code)
                self.keyUp(0x10)
            time.sleep(delayed)

    def keyDown(self, vk_code, delayed=0.0):
        """键盘按键按下"""
        win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), 0, 0)
        time.sleep(delayed)

    def keyUp(self, vk_code, delayed=0.0):
        """键盘按键释放"""
        vk = win32api.MapVirtualKey(vk_code, 0)
        win32api.keybd_event(vk_code, vk, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(delayed)

    def mouseMove(self, x, y):
        """鼠标移动到坐标"""
        win32api.SetCursorPos([x, y])

    def mouseLeftClick(self, delayed=0.0):
        """鼠标左键单击"""
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(delayed)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def mouseLeftMoveClick(self, x, y, delayed=0.0):
        """鼠标左键移动到坐标单击"""
        win32api.SetCursorPos([x, y])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(delayed)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def mouseRightClick(self, delayed=0.0):
        """鼠标右键单击"""
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        time.sleep(delayed)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    def mouseRightMoveClick(self, x, y, delayed=0.0):
        """鼠标右键移动到坐标单击"""
        win32api.SetCursorPos([x, y])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(delayed)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def mouseRoll(self, rate):
        """鼠标滚轮"""
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, rate, 1)
