import ctypes
import time

def drawLine(startX, startY, endx, endy):
    # 导入所需的WinAPI函数
    gdi32 = ctypes.WinDLL('gdi32')
    user32 = ctypes.WinDLL('user32')

    # 获取屏幕的宽度和高度
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # 定义起点和终点坐标
    start_x, start_y = startX, startY
    end_x, end_y = endx, endy

    # 获取CS:GO窗口的句柄
    csgo_window = user32.FindWindowA(None, b"Counter-Strike: Global Offensive - Direct3D 9")

    # 计算起点和终点的屏幕坐标
    start_pos = screen_width * start_x // 2560, screen_height * start_y // 1440
    end_pos = screen_width * end_x // 2560, screen_height * end_y // 1440


    # 将绘图设备连接到CS:GO窗口
    device_context = user32.GetDC(csgo_window)

    # 创建一个画笔
    pen = gdi32.CreatePen(0, 2, 0x00FF00)  # 线条颜色为绿色

    # 将画笔选入设备上下文
    gdi32.SelectObject(device_context, pen)

    # 绘制线条
    gdi32.MoveToEx(device_context, start_pos[0], start_pos[1], None)
    gdi32.LineTo(device_context, end_pos[0], end_pos[1])

    # 释放设备上下文和画笔
    user32.ReleaseDC(csgo_window, device_context)
    gdi32.DeleteObject(pen)

    # 等待一段时间，以便观察结果
