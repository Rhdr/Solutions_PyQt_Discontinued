def __getCapsLockStateHex():
        import ctypes
        __hllDll = ctypes.WinDLL("User32.dll")
        __VK_CAPITAL = 0x14
        return __hllDll.GetKeyState(__VK_CAPITAL)

def get_CapsLockEnabled():
    __state = __getCapsLockStateHex()
    print(__state)
    if (__state == 0) or (__state == 65408):
        #capsLock is disabled
        return False
    else:
        # capsLock is enabled
        return True

if __name__ == "__main__":
    from PyQt5 import QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)
    print("CapsLock State:" + str(get_CapsLockEnabled()))
    sys.exit(app.exec())
