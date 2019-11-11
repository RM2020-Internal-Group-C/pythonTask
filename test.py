import cv2

from matplotlib import pyplot as plt

img = cv2.imread('81.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
plt.imshow(hsv)
plt.title('grayscale')
plt.show()

