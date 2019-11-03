import serial
import serial.tools.list_ports
import cv2
import numpy as np

# ser = serial.Serial('/dev/ttyUSB0')
# print(ser.name)
print ('Search ports...')
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print ('-- Find ports --')
    print (p)

try:
    ser = serial.Serial(ports[0])
    print('Connected to port', ports[0])
except:
    print('Cannot find any port available!')
    pass

sendStr = ''
imgHeight = 600
imgWidth = 800
# Four sets of thres for specifying the colors
# Bule
blueUpperThres = np.array([115, 105, 95])
blueLowerThres = np.array([85, 75, 65])
# Orange
orangeUpperThres = np.array([15, 210, 195])
orangeLowerThres = np.array([0, 190, 175])
# Yellow
yellowUpperThres = np.array([30, 195, 195])
yellowLowerThres = np.array([15, 185, 185])
# Green
greenUpperThres = np.array([40, 110, 75])
greenLowerThres = np.array([27, 80, 60])

def getCoor(img):
    for i in range(0, imgHeight, 3):
        for j in range(0, imgWidth, 8):
            if img[i][j] > 0:
                return j
    return 0
counter = 0
while counter < 1000:
    img = cv2.imread('3.jpg')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blueMask = cv2.inRange(hsv, blueLowerThres, blueUpperThres)
    orangeMask = cv2.inRange(hsv, orangeLowerThres, orangeUpperThres)
    yellowMask = cv2.inRange(hsv, yellowLowerThres, yellowUpperThres)
    greenMask = cv2.inRange(hsv, greenLowerThres, greenUpperThres)

    blueMask = cv2.medianBlur(blueMask, 7)
    orangeMask = cv2.medianBlur(orangeMask, 7)
    yellowMask = cv2.medianBlur(yellowMask, 7)
    greenMask = cv2.medianBlur(greenMask, 7)
        
    blueX = getCoor(blueMask)
    orangeX = getCoor(orangeMask)
    yellowX = getCoor(yellowMask)
    greenX = getCoor(greenMask)

    if blueX < orangeX < yellowX < greenX:
        sendStr = '0'
    elif blueX < orangeX < greenX < yellowX:
        sendStr = '1'
    elif blueX < greenX < orangeX < yellowX:
        sendStr = '2'
    elif blueX < greenX < yellowX < orangeX:
        sendStr = '3'
    elif blueX < yellowX < greenX < orangeX:
        sendStr = '4'
    elif blueX < yellowX < orangeX < greenX:
        sendStr = '5'
    elif yellowX < blueX < orangeX < greenX:
        sendStr = '6'
    elif yellowX < blueX < greenX < orangeX:
        sendStr = '7'
    elif yellowX < orangeX < blueX < greenX:
        sendStr = '8'
    elif yellowX < orangeX < greenX < blueX:
        sendStr = '9'
    elif yellowX < greenX < blueX < orangeX:
        sendStr = '10'
    elif yellowX < greenX < orangeX < blueX:
        sendStr = '11'
    elif greenX < yellowX < orangeX < blueX:
        sendStr = '12'
    elif greenX < yellowX < blueX < orangeX:
        sendStr = '13'
    elif greenX < blueX < yellowX < orangeX:
        sendStr = '14'
    elif greenX < blueX < orangeX < yellowX:
        sendStr = '15'
    elif greenX < orangeX < blueX < yellowX:
        sendStr = '16'
    elif greenX < orangeX < yellowX < blueX:
        sendStr = '17'
    elif orangeX < blueX < yellowX < greenX:
        sendStr = '18'
    elif orangeX < blueX < greenX < yellowX:
        sendStr = '19'
    elif orangeX < yellowX < blueX < greenX:
        sendStr = '20'
    elif  orangeX < yellowX < greenX < blueX:
        sendStr = '21'
    elif orangeX < greenX < yellowX < blueX:
        sendStr = '22'
    elif orangeX < greenX < blueX < yellowX:
        sendStr = '23'
    else:
        sendStr = '24'
    print(counter, sendStr)
    counter += 1
# cap.release()