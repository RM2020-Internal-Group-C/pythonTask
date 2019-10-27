import cv2

img = cv2.imread('3.jpg')

img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
