import numpy as np
import cv2
import math
hor = 30.0
ver = 25.0
FIXED_PIX = (320.0, 240.0)
px = 640.0
py = 480.0
lower_red = np.array([0, 120, 170])
upper_red = np.array([50, 220, 255])
lower_red1 = np.array([170, 120, 170])
upper_red1 = np.array([255, 220, 255])

#lower_red = np.array([0, 120, 210])
#upper_red = np.array([50, 200, 255])
#lower_red1 = np.array([210, 120, 210])
#upper_red1 = np.array([255, 200, 255])
MIN_SIZE = 150

def getBall(img):
    ing = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(ing, lower_red, upper_red)
    res1 = cv2.bitwise_and(ing, ing, mask=mask)
    mask1 = cv2.inRange(ing, lower_red1, upper_red1)
    res2 = cv2.bitwise_and(ing, ing, mask=mask1)
    res1 = cv2.bitwise_or(res1, res2)
    kernel1 = np.ones((12,12), np.uint8)
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
            point = [(float(point[0]) - px/2)/px, -(float(point[1]) -
                                                     py/2)/py]
            bloons.append([point[0]*hor, point[1]*ver])
    return bloons

def canShoot(img):
    ing = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(ing, lower_red, upper_red)
    res1 = cv2.bitwise_and(ing, ing, mask=mask)
    mask1 = cv2.inRange(ing, lower_red1, upper_red1)
    res2 = cv2.bitwise_and(ing, ing, mask=mask1)
    res1 = cv2.bitwise_or(res1, res2)
    kernel1 = np.ones((12, 12), np.uint8)
    kernel2 = np.ones((2, 2), np.uint8)
    kernel3 = np.ones((6, 6), np.uint8)
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
        im1, contours, hier = cv2.findContours(gray, cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_NONE)
    toDelete = []
    for j in range(len(contours)):
        if len(contours[j]) < 5:
            toDelete.append(contours[j])
            continue
        ellipse = cv2.fitEllipse(contours[j])
        ratio = ellipse[1][0] / ellipse[1][1]
        if ratio > 2 or ratio < 0.5:
            toDelete.append(contours[j])
        elif cv2.contourArea(contours[j]) < \
                                                0.5 * 0.25 * ellipse[1][0] * \
                                ellipse[1][1] * math.pi:
            toDelete.append(contours[j])
        elif cv2.contourArea(contours[j]) < 150:
            toDelete.append(contours[j])
        else:
            if cv2.pointPolygonTest(contours[j], FIXED_PIX, False) >= 0:
                return 1
    return 0

def getColor(img):
    """returns a binary image of the color specified"""
    ing = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_color = np.array(lower_red)
    upper_color = np.array(upper_red)
    mask = cv2.inRange(ing, lower_color, upper_color)
    res1 = cv2.bitwise_and(ing, ing, mask=mask)
    return res1

def didPop(imgBEFORE, imgAFTER):
    """returns true if red balloon popped, false otherwise"""
    lowerBound = lower_red
    upperBound = upper_red
    min_size = MIN_SIZE
    color1 = getColor(imgBEFORE)
    color2 = getColor(imgAFTER)
    return 0
