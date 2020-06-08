import cv2
import numpy as np

#Read gray image
corrected_img_path = "./img_test_corrected/test1.png"
corrected_img = cv2.imread(corrected_img_path, 0)

#Create default parametrization LSD
lsd = cv2.createLineSegmentDetector(0)

#Detect lines in the image
lines = lsd.detect(corrected_img)[0]

# Find the pointer according to the prior knowledge of the specified table class


# calculate the angle, then get the reading number according to the angle->reading num


#Draw detected lines in the image
drawn_img = lsd.drawSegments(corrected_img, lines)

#Show image
cv2.imshow("LSD", drawn_img)
cv2.waitKey(0)
