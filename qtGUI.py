import serial
import serial.tools.list_ports
import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# GUI Part import
import sys
from PyQt5.QtCore import *

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QGridLayout

# global variables
capCamera = 0
counter = 0
medianSize = 7
originImgShow = False
blueMaskShow = False
redMaskShow = False
yellowMaskShow = False
greenMaskShow = False
toggleSampleChecking = False
imgHeight = 360
imgWidth = 640
HSV_sets = {
    'BHH' : 115,
    'BLH' : 85,
    'BHS' : 105,
    'BLS' : 75,
    'BHV' : 95,
    'BLV' : 65,

    'RHH' : 15,
    'RLH' : 0,
    'RHS' : 210,
    'RLS' : 190,
    'RHV' : 195,
    'RLV' : 175,

    'YHH' : 30,
    'YLH' : 15,
    'YHS' : 260,
    'YLS' : 220,
    'YHV' : 220,
    'YLV' : 190,

    'GHH' : 40,
    'GLH' : 27,
    'GHS' : 110,
    'GLS' : 80,
    'GHV' : 75,
    'GLV' : 60
}

# Slot functions
def changeOriginImgShow():
    global originImgShow
    originImgShow = 1 - originImgShow

def changeBlueMaskShow():
    global blueMaskShow
    blueMaskShow = 1 - blueMaskShow

def changeRedMaskShow():
    global redMaskShow
    redMaskShow = 1 - redMaskShow

def changeYellowMaskShow():
    global yellowMaskShow
    yellowMaskShow = 1 - yellowMaskShow

def changeGreenMaskShow():
    global greenMaskShow
    greenMaskShow = 1 - greenMaskShow

def changeAdjustSample():
    plt.close('all')
    global toggleSampleChecking
    toggleSampleChecking = 1 - toggleSampleChecking

def changeBH(h, s, v):
    HSV_sets['BHH'] = h
    HSV_sets['BHS'] = s
    HSV_sets['BHV'] = v

def changeBL(h, s, v):
    HSV_sets['BLH'] = h
    HSV_sets['BLS'] = s
    HSV_sets['BLV'] = v

def changeRH(h, s, v):
    HSV_sets['RHH'] = h
    HSV_sets['RHS'] = s
    HSV_sets['RHV'] = v

def changeRL(h, s, v):
    HSV_sets['RLH'] = h
    HSV_sets['RLS'] = s
    HSV_sets['RLV'] = v

def changeYH(h, s, v):
    HSV_sets['YHH'] = h
    HSV_sets['YHS'] = s
    HSV_sets['YHV'] = v

def changeYL(h, s, v):
    HSV_sets['YLH'] = h
    HSV_sets['YLS'] = s
    HSV_sets['YLV'] = v

def changeGH(h, s, v):
    HSV_sets['GHH'] = h
    HSV_sets['GHS'] = s
    HSV_sets['GHV'] = v

def changeGL(h, s, v):
    HSV_sets['GLH'] = h
    HSV_sets['GLS'] = s
    HSV_sets['GLV'] = v

def resetValues(_self):
    HSV_sets['BHH'] = 115
    _self.lineEditors['BHH'].setText(str(HSV_sets['BHH']))
    HSV_sets['BLH'] = 85
    _self.lineEditors['BLH'].setText(str(HSV_sets['BLH']))
    HSV_sets['BHS'] = 105
    _self.lineEditors['BHS'].setText(str(HSV_sets['BHS']))
    HSV_sets['BLS'] =  75
    _self.lineEditors['BLS'].setText(str(HSV_sets['BLS']))
    HSV_sets['BHV'] = 95
    _self.lineEditors['BHV'].setText(str(HSV_sets['BHV']))
    HSV_sets['BLV'] =  65
    _self.lineEditors['BLV'].setText(str(HSV_sets['BLV']))

    HSV_sets['RHH'] = 15
    _self.lineEditors['RHH'].setText(str(HSV_sets['RHH']))
    HSV_sets['RLH'] = 0
    _self.lineEditors['RLH'].setText(str(HSV_sets['RLH']))
    HSV_sets['RHS'] = 210
    _self.lineEditors['RHS'].setText(str(HSV_sets['RHS']))
    HSV_sets['RLS'] = 190
    _self.lineEditors['RLS'].setText(str(HSV_sets['RLS']))
    HSV_sets['RHV'] = 195
    _self.lineEditors['RHV'].setText(str(HSV_sets['RHV']))
    HSV_sets['RLV'] = 175
    _self.lineEditors['RLV'].setText(str(HSV_sets['RLV']))

    HSV_sets['YHH'] = 30
    _self.lineEditors['YHH'].setText(str(HSV_sets['YHH']))
    HSV_sets['YLH'] = 15
    _self.lineEditors['YLH'].setText(str(HSV_sets['YLH']))
    HSV_sets['YHS'] = 260
    _self.lineEditors['YHS'].setText(str(HSV_sets['YHS']))
    HSV_sets['YLS'] = 220
    _self.lineEditors['YLS'].setText(str(HSV_sets['YLS']))
    HSV_sets['YHV'] = 220
    _self.lineEditors['YHV'].setText(str(HSV_sets['YHV']))
    HSV_sets['YLV'] = 190
    _self.lineEditors['YLV'].setText(str(HSV_sets['YLV']))

    HSV_sets['GHH'] = 40
    _self.lineEditors['GHH'].setText(str(HSV_sets['GHH']))
    HSV_sets['GLH'] = 27
    _self.lineEditors['GLH'].setText(str(HSV_sets['GLH']))
    HSV_sets['GHS'] = 110
    _self.lineEditors['GHS'].setText(str(HSV_sets['GHS']))
    HSV_sets['GLS'] = 80
    _self.lineEditors['GLS'].setText(str(HSV_sets['GLS']))
    HSV_sets['GHV'] = 75
    _self.lineEditors['GHV'].setText(str(HSV_sets['GHV']))
    HSV_sets['GLV'] = 60
    _self.lineEditors['GLV'].setText(str(HSV_sets['GLV']))

# Create a subclass of QMainWindow to setup the GUI
class pyTuningGUI(QMainWindow, QObject):
    # pyTuningGUI's view
    def __init__(self):
        # View initializer
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('CV Tuning')
        # self.setFixedSize(1000, 1000)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        # Set the central widgets
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the elements
        self._createElements()

    # Create the buttons
    def _createElements(self):
        # Create the buttons
        self.labels = {}
        self.lineEditors = {}
        self.buttons = {}
        labelButtonLineEditorLayout = QGridLayout()
        # Label text | positon on the QGridLayout
        labels = {
            'BlueHighThres:' : (0, 0),
            'BlueLowthres:' : (1, 0),
            'RedHighThres: ' : (2, 0),
            'RedLowThres: ' : (3, 0),
            'YellowHighThres: ' : (4, 0),
            'YellowLowThres: ' : (5, 0),
            'GreenHighThres: ' : (6, 0),
            'GreenLowThres: ' : (7, 0)
        }
        # LineEditor text | position on the QGridLayout
        lineEditors = {
            'BHH' : (0, 1),
            'BHS' : (0, 2),
            'BHV' : (0, 3),
            'BLH' : (1, 1),
            'BLS' : (1, 2),
            'BLV' : (1, 3),
            'RHH' : (2, 1),
            'RHS' : (2, 2),
            'RHV' : (2, 3),
            'RLH' : (3, 1),
            'RLS' : (3, 2),
            'RLV' : (3, 3),
            'YHH' : (4, 1),
            'YHS' : (4, 2),
            'YHV' : (4, 3),
            'YLH' : (5, 1),
            'YLS' : (5, 2),
            'YLV' : (5, 3),
            'GHH' : (6, 1),
            'GHS' : (6, 2),
            'GHV' : (6, 3),
            'GLH' : (7, 1),
            'GLS' : (7, 2),
            'GLV' : (7, 3)
        }

        # Button text | position on the QGridLayout
        buttons = {
            'BHSave' : (0, 4),
            'BLSave' : (1, 4),
            'RHSave' : (2, 4),
            'RLSave' : (3, 4),
            'YHSave' : (4, 4),
            'YLSave' : (5, 4),
            'GHSave' : (6, 4),
            'GLSave' : (7, 4),
            'BlueShow' : (0, 5),
            'RedShow' : (2, 5),
            'YellowShow' : (4, 5),
            'GreenShow' : (6, 5),
            'OriginShow' : (8, 0),
            'ToggleAdjust' : (8, 1),
            'ResetValue' : (8, 2)
        }

        # Create labels and add them to the grid layout
        for LBText, LBCoor in labels.items():
            self.labels[LBText] = QLabel(LBText)
            self.labels[LBText].setFixedSize(100, 30)
            labelButtonLineEditorLayout.addWidget(self.labels[LBText], LBCoor[0], LBCoor[1])

        # Create lineEditors and add them to the grid layout
        for LEText, LECoor in lineEditors.items():
            self.lineEditors[LEText] = QLineEdit(str(HSV_sets[LEText]))
            self.lineEditors[LEText].setFixedSize(50, 30)
            labelButtonLineEditorLayout.addWidget(self.lineEditors[LEText], LECoor[0], LECoor[1])

        # Create buttons and add them to the grid layout
        for BTText, BTCoor in buttons.items():
            self.buttons[BTText] = QPushButton(BTText)
            self.buttons[BTText].setFixedSize(100, 30) # width and height
            labelButtonLineEditorLayout.addWidget(self.buttons[BTText], BTCoor[0], BTCoor[1])
        self.generalLayout.addLayout(labelButtonLineEditorLayout)

        self.buttons['BlueShow'].clicked.connect(changeBlueMaskShow)
        self.buttons['RedShow'].clicked.connect(changeRedMaskShow)
        self.buttons['YellowShow'].clicked.connect(changeYellowMaskShow)
        self.buttons['GreenShow'].clicked.connect(changeGreenMaskShow)
        self.buttons['OriginShow'].clicked.connect(changeOriginImgShow)
        self.buttons['ToggleAdjust'].clicked.connect(changeAdjustSample)
        self.buttons['BHSave'].clicked.connect(lambda : changeBH(int(self.lineEditors['BHH'].text()), int(self.lineEditors['BHS'].text()), int(self.lineEditors['BHV'].text())))
        self.buttons['BLSave'].clicked.connect(lambda : changeBL(int(self.lineEditors['BLH'].text()), int(self.lineEditors['BLS'].text()), int(self.lineEditors['BLV'].text())))
        self.buttons['RHSave'].clicked.connect(lambda : changeRH(int(self.lineEditors['RHH'].text()), int(self.lineEditors['RHS'].text()), int(self.lineEditors['RHV'].text())))
        self.buttons['RLSave'].clicked.connect(lambda : changeRL(int(self.lineEditors['RLH'].text()), int(self.lineEditors['RLS'].text()), int(self.lineEditors['RLV'].text())))
        self.buttons['YHSave'].clicked.connect(lambda : changeYH(int(self.lineEditors['YHH'].text()), int(self.lineEditors['YHS'].text()), int(self.lineEditors['YHV'].text())))
        self.buttons['YLSave'].clicked.connect(lambda : changeYL(int(self.lineEditors['YLH'].text()), int(self.lineEditors['YLS'].text()), int(self.lineEditors['YLV'].text())))
        self.buttons['GHSave'].clicked.connect(lambda : changeGH(int(self.lineEditors['GHH'].text()), int(self.lineEditors['GHS'].text()), int(self.lineEditors['GHV'].text())))
        self.buttons['GLSave'].clicked.connect(lambda : changeGL(int(self.lineEditors['GLH'].text()), int(self.lineEditors['GLS'].text()), int(self.lineEditors['GLV'].text())))
        self.buttons['ResetValue'].clicked.connect(lambda : resetValues(self))


def changeResolutin(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)
 
def readSamples(counter):
    subCounter = 1 + (counter % 11)
    return cv2.imread('samples/%d.jpg' % subCounter)

def toggleSampleCheck(img):
    global toggleSampleChecking
    plt.imshow(img)
    plt.title('Adjust Sample')
    plt.show()
    toggleSampleChecking = False

def getCoor(img):
    for i in range(0, imgHeight, 3):
        for j in range(0, imgWidth, 8):
            if img[i][j] > 0:
                return j
    return 0

def cvTask():
    global originImgShow, blueMaskShow, redMaskShow, yellowMaskShow, greenMaskShow,toggleSampleChecking ,counter
    while True:
        img = readSamples(1)
    # while cap.isOpened():
    #     _, img = cap.read()

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        blueMask = cv2.inRange(hsv, (HSV_sets['BLH'], HSV_sets['BLS'], HSV_sets['BLV']),  (HSV_sets['BHH'], HSV_sets['BHS'], HSV_sets['BHV']))
        redMask = cv2.inRange(hsv, (HSV_sets['RLH'], HSV_sets['RLS'], HSV_sets['RLV']),  (HSV_sets['RHH'], HSV_sets['RHS'], HSV_sets['RHV']))
        yellowMask = cv2.inRange(hsv, (HSV_sets['YLH'], HSV_sets['YLS'], HSV_sets['YLV']),  (HSV_sets['YHH'], HSV_sets['YHS'], HSV_sets['YHV']))
        greenMask = cv2.inRange(hsv, (HSV_sets['GLH'], HSV_sets['GLS'], HSV_sets['GLV']),  (HSV_sets['GHH'], HSV_sets['GHS'], HSV_sets['GHV']))

        blueMask = cv2.medianBlur(blueMask, medianSize)
        redMask = cv2.medianBlur(redMask, medianSize)
        yellowMask = cv2.medianBlur(yellowMask, medianSize)
        greenMask = cv2.medianBlur(greenMask, medianSize)

        blueX = getCoor(blueMask)
        redX = getCoor(redMask)
        yellowX = getCoor(yellowMask)
        greenX = getCoor(greenMask)

        print('%6d' % counter, blueX, redX, yellowX, greenX)

        if originImgShow == True:
            cv2.imshow('origin', img)
        else:
            cv2.destroyWindow('origin')
        if blueMaskShow == True:
            cv2.imshow('blueMask', blueMask)
        else:
            cv2.destroyWindow('blueMask')
        if redMaskShow == True:
            cv2.imshow('redMask', redMask)
        else:
            cv2.destroyWindow('redMask')
        if yellowMaskShow == True:
            cv2.imshow('yellowMask', yellowMask)
        else:
            cv2.destroyWindow('yellowMask')
        if greenMaskShow == True:
            cv2.imshow('greenMask', greenMask)
        else:
            cv2.destroyWindow('greenMask')

        # if toggleSampleChecking == True:
        plt.imshow(img)
        plt.title('Adjust Sample')
        plt.show()
            

        counter += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            blueMaskShow  = False
            redMaskShow = False
            yellowMaskShow = False
            greenMaskShow = False
            originImgShow = False
            cv2.destroyAllWindows()

# Client Code
def main():
    # Create an instance of QApplication
    ptGUI = QApplication(sys.argv)
    # Show the GUI
    view = pyTuningGUI()
    view.show()
    # Execute the main loop
    cvTask()
    sys.exit(ptGUI.exec_())


if __name__ == '__main__':
    cap = cv2.VideoCapture(capCamera)
    changeResolutin(cap, imgWidth, imgHeight)
    main()
    cap.release()

