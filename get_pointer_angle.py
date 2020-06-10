import cv2
import numpy as np
from PIL import Image

corrected_img_path = "./img_test/test1.png"

# 读取图像变成灰度并可以图像预处理
img = cv2.imread(corrected_img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 图像的边缘检测
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# 把图像缩小减少运算量
edges_img = Image.fromarray(edges)
w, h = edges_img.size
edges_img_resized = edges_img.resize((w // 3, h // 3))
edges_img_resized_array = np.array(edges_img_resized)

# 使用Hough Circle Transform对缩小的图像进行仪表盘的检测。
circles = cv2.HoughCircles(edges_img_resized_array, cv2.HOUGH_GRADIENT, 1, 100,
                            param1=150, param2=100, minRadius=0, maxRadius=0)
circles_int = np.uint16(np.around(circles))
x, y, _ = circles[0][0]  # 假设找到一个最大的圆 ！！！！！！！！
x, y = x * 3, y * 3   # 缩小前原图仪表盘的圆心用来作为检测指针的先验条件

# 使用Hough Line Transform对原始灰度图进行检测直线检测
minLineLength = 120
maxLineGap = 10
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap).squeeze(1)

"""使用先验条件检测出指针: 直线经过指针；指针的线段长度最长。"""
current_lines = []
for x1, y1, x2, y2 in lines:
    # 首先使用指向圆心筛选直线
    error = np.abs((y2 - y) * (x1 - x) - (y1 - y) * (x2 - x))
    if error < 1000:  # 可以调节阈值 ！！！！！！
        current_lines.append((x1, y1, x2, y2))
        # 显示
        #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
pointer_line = ()
pointer_length = 0
for x1, y1, x2, y2 in current_lines:
    length = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
    if length > pointer_length:
        pointer_length = length
        pointer_line = (x1, y1, x2, y2)
# 测试显示
x1, y1, x2, y2 = pointer_line
cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
# 求出指针角度
pointer_grad = (y2 - y1) / (x2 - x1)
poiner_degree = np.arccos(pointer_grad) / np.pi * 180
if x1 > x2:
    if x1 > x:
        if poiner_degree > 90:
            poiner_degree = 180 - poiner_degree
    else:
        if poiner_degree < 90:
            poiner_degree = 180 - poiner_degree
else:
    if x2 > x:
        if poiner_degree > 90:
            poiner_degree = 180 - poiner_degree
    else:
        if poiner_degree < 90:
            poiner_degree = 180 - poiner_degree
print(poiner_degree)
# 显示
for i in circles_int[0, :]:
    # draw the outer circle
    cv2.circle(edges_img_resized_array, (i[0], i[1]), i[2],(255,255,0), 2)
    # draw the center of the circle
    cv2.circle(edges_img_resized_array, (i[0], i[1]), 2, (255,0,0), 3)

# 显示图像
cv2.imshow("edges", edges)
cv2.imshow("img", img)
cv2.imshow("edges_resized", edges_img_resized_array)
cv2.waitKey(0)

