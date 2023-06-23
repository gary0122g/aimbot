import win32api,win32con

def lock(current_x, current_y, target_x, target_y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -(current_x-target_x) , (target_y - current_y) , 0, 0)