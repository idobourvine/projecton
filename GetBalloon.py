import numpy as np
import cv2
import math
hor = 30.0
ver = 25.0
px = 640.0
py = 480.0
def getBall(img):
    ing = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([130, 100, 140])
    upper_red = np.array([200, 220, 255])
    mask = cv2.inRange(ing, lower_red, upper_red)
    res1 = cv2.bitwise_and(ing, ing, mask=mask)
    kernel1 = np.ones((12,12), np.uint8)
    kernel2 = np.ones((2,2), np.uint8)
    kernel3 = np.ones((6,6), np.uint8)
    close1 = cv2.morphologyEx(res1, cv2.MORPH_CLOSE, kernel1)
    open1 = cv2.morphologyEx(close1, cv2.MORPH_OPEN, kernel3)
    gray = cv2.cvtColor(open1, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    im1, contours, hier = cv2.findContours(gray, cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_NONE)
    if not len(contours):
        close1 = cv2.morphologyEx(res1, cv2.MORPH_CLOSE, kernel1)
        gray = cv2.cvtColor(close1, cv2.COLOR_HSV2BGR)
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        im1, contours, hier = cv2.findContours(gray,cv2.RETR_TREE,
                                          cv2.CHAIN_APPROX_NONE)
    toDelete = []
    bloons = []
    i = 0
    for j in range(len(contours)):
        if(len(contours[j]) < 5):
            toDelete.append(contours[j])
            continue
        ellipse = cv2.fitEllipse(contours[j])
        ratio = ellipse[1][0]/ellipse[1][1]
        if ratio > 2 or ratio < 0.5:
            toDelete.append(contours[j])
        elif cv2.contourArea(contours[j]) < \
                                0.5*0.25*ellipse[1][0]*ellipse[1][1]*math.pi:
            toDelete.append(contours[j])
        elif cv2.contourArea(contours[j]) < 150:
            toDelete.append(contours[j])
        else:
            i += 1
            point = ellipse[0]
            point = [(float(point[0]) - px/2)/px, -(float(point[1]) - py/2)/py]
            bloons.append([point[0]*hor, point[1]*ver])
    return bloons
