import cv2
import numpy as np
from PIL import Image

corrected_img_path = "./img_test_corrected/test1.png"

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
x, y = x * 3, y * 3   # 缩小前原图仪表盘的圆心

# 使用Hough Line Transform对原始灰度图进行检测直线指针检测
lines = cv2.HoughLines(edges, 1, np.pi/180, 125).squeeze(1)

# 使用仪表盘圆心坐标进行正则化选出指针
pointer_arr = []  # 目前是只用仪表盘圆心坐标就能选出指针来 ！！！！！！！！！
for rho, theta in lines:
    a = np.cos(theta)
    b = np.sin(theta)
    threshold = np.abs(rho - x * a - y * b)
    if threshold < 10: #  这个参数得试验得到 ！！！！！！！！！！
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)
        pointer_arr.append((rho, theta))

# 求出指针角度

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

