import cv2
import numpy as np

img = cv2.imread('./template/class1.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imshow("LSD1", edges)
cv2.imshow("LSD2", img)
cv2.waitKey(0)


# 把图像缩小减少运算量
#edges_img = Image.fromarray(edges)
#w, h = edges_img.size
#edges_img_resized = edges_img.resize((w // 3, h // 3))
#edges_img_resized_array = np.array(edges_img_resized)