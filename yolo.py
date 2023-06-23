import cv2
import torch
import pyautogui
from PIL import Image
import numpy as np
import ctypes
import drawline as dr
import pygetwindow as gw
from PIL import ImageGrab
from lock import lock


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.hub.load('ultralytics/yolov5', 'yolov5l6', pretrained=True).to(device)

# 取得特定程式視窗
window_title = 'Counter-Strike: Global Offensive - Direct3D 9'  # 替換為目標程式的標題
window = gw.getWindowsWithTitle(window_title)[0]
game_screen_coordinates = [0, 0, 2560, 1440]

gdi32 = ctypes.WinDLL('gdi32')
user32 = ctypes.WinDLL('user32')
csgo_window = user32.FindWindowA(None, b"Counter-Strike: Global Offensive - Direct3D 9")


# 取得視窗的座標資訊
left, top, right, bottom = window.left, window.top, window.right, window.bottom
sqLeft, sqTop , sqRight , sqBottom = 880, 420, 1680, 1020
window_width = right - left
window_height = bottom - top


# 開始遊戲畫面擷取與人物辨識
while True:
    # 擷取遊戲畫面圖像
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    game_screen = torch.from_numpy(cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)).to(device)

    # 將圖像轉換為PIL Image
    image = Image.fromarray(game_screen.cpu().numpy())
    # 使用YOLOv5進行人物辨識
    results = model(image)
    # 取得預測結果
    predictions = results.pandas().xyxy[0]
    person_predictions = predictions[predictions['name'] == 'person']
    string = 'person'
    
    if string in predictions['name'].values:        
        person = predictions.iloc[0]
        if person.confidence>0.85:
            x_center = int((person.xmax + person.xmin) / 2)
            y_center = int((person.ymax + person.ymin) / 2)
            current_x, current_y = pyautogui.position()
            
            xmin = int(person['xmin'])
            ymin = int(person['ymin'])
            xmax = int(person['xmax'])
            ymax = int(person['ymax'])     
            lock(current_x, current_y, x_center, y_center) 
            # 計算滑鼠移動目標位置
            target_x = x_center 
            target_y =y_center 

            dr.drawLine(current_x, current_y, target_x, target_y)
            
            # cv2.rectangle(game_screen, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            
            # cv2.rectangle(game_screen, (sqLeft, sqRight),(  sqTop , sqBottom),( 255,0,0),2 )

            # cv2.imshow("Counter-Strike: Global Offensive - Direct3D 9", game_screen)
            
            # print("target",target_x,target_y)
            # time.sleep(0.0005)


# 釋放資源並關閉視窗
cv2.destroyAllWindows()


