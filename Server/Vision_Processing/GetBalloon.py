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

lower_car = np.array([45, 100, 25])
upper_car = np.array([170, 255, 165])
lower_line = np.array([[55, 55, 30]])
upper_line = np.array([[95, 95, 75]])

lower_lights = np.array([100, 100, 100])
upper_lights = np.array([255, 255, 255])

#lower_red = np.array([0, 120, 210])
#upper_red = np.array([50, 200, 255])
#lower_red1 = np.array([210, 120, 210])
#upper_red1 = np.array([255, 200, 255])
MIN_SIZE = 150
FACTOR_OF_ENLARGEMENT = 1.5
MIN_WHITES = 5000


def turnOnLights(img):
    """returns true if the lights are on in the image, false otherwise"""
    mask = cv2.inRange(img, lower_lights, upper_lights)
    res1 = cv2.bitwise_and(img, img, mask=mask)
    res1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
    if cv2.countNonZero(res1) > MIN_WHITES:
        return True
    else:
        return False


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
    lower_color = np.array(red_lower)
    upper_color = np.array(red_upper)
    mask = cv2.inRange(ing, lower_color, upper_color)
    res1 = cv2.bitwise_and(ing, ing, mask=mask)
    return res1

def getColor1(img, colorMin, colorMax):
    """returns a binary image of the color specified"""
    ing = img
    lower_color = np.array(colorMin)
    upper_color = np.array(colorMax)
    mask = cv2.inRange(ing, lower_color, upper_color)
    res1 = cv2.bitwise_and(ing, ing, mask=mask)
    return res1

def didPop(imgBEFORE, imgAFTER):
    """returns true if red balloon popped, false otherwise"""
    color1 = getColor(imgBEFORE)
    color2 = getColor(imgAFTER)
    color1 = cv2.cvtColor(color1, cv2.COLOR_BGR2GRAY)
    color2 = cv2.cvtColor(color2, cv2.COLOR_BGR2GRAY)
    numBefore = cv2.countNonZero(color1)
    numAfter = cv2.countNonZero(color2)
    if numBefore > numAfter + MIN_SIZE:
        return 1
    else:
        return 0


d = 30
BAD1 = [5, 5, 5]
d1 = 10
BAD2 = [200, 200, 200]
d2 = 56
BAD3 = [5, 5, 250]
d3 = 10
BAD4 = [65, 15, 150]
d4 = 25
red_lower = [0, 20, 140]  # security cameras
red_upper = [185, 160, 255]
red_lower_sec = [0, 0, 700]  # car camera
red_upper_sec = [110, 100, 180]


def canShoot1(circles):
    """return if you can shoot or not"""
    for circle in circles:
        if (FIXED_PIX[0] - circle[0])**2 + (FIXED_PIX[1] - circle[1])**2 < \
                FACTOR_OF_ENLARGEMENT * circle[2]**2:
            return 1
    return 0


def getBalloon(img):
    """returns a list, the first object is a boolean that says if you can
    shoot or not, and the second one is a list of angles to each red balloon in
    the image"""
    bloons = getEnemiesSec(img)[0]
    can_shoot = canShoot1(bloons)
    angles = []
    for bloon in bloons:
        # cv2.circle(img, (bloon[0], bloon[1]), bloon[2], (0, 255, 0), 4)
        bloon[0] = (bloon[0] - px/2) / px
        bloon[1] = (py/2 - bloon[1]) / py
        angles.append([bloon[0] * hor, bloon[1] * ver])
    # cv2.imshow("image", img)
    return [can_shoot, angles]


def getEnemiesSec(img):
    """returns a list of enemy balloons and their sizes in image works for
    the car camera!!"""
    red_bloons = []
    red_sizes = []
    bloons, sizes = getCircle(img)
    for i in range(len(bloons)):
        if isRed(img, bloons[i]):
            # cv2.circle(img, (bloons[i][0], bloons[i][1]), bloons[i][2], (0,
            #
            # 255, 0), 4)
            # cv2.imshow("image", img)
            cv2.waitKey(100)
            red_bloons.append(bloons[i])
            red_sizes.append(sizes[i])
    # cv2.imshow("image", img)
    return [red_bloons, red_sizes]


def getEnemies(img):
    """returns a list of enemy balloons and their sizes in image works for
    the security cameras!!!"""
    red_bloons = []
    red_sizes = []
    bloons, sizes = getCircle(img)
    for i in range(len(bloons)):
        if isRedSec(img, bloons[i]):
            cv2.circle(img, (bloons[i][0], bloons[i][1]), bloons[i][2], (0,
                                                                        255, 0), 4)
            red_bloons.append(bloons[i])
            red_sizes.append(sizes[i])
    cv2.imshow("image", img)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    return [red_bloons, red_sizes]


def getFriends(img):
    """returns a list of friendly balloons and their sizes in image"""
    friend_bloons = []
    friend_sizes = []
    bloons, sizes = getCircle(img)
    for i in range(len(bloons)):
        if not isRedSec(img, bloons[i]):
            friend_bloons.append(bloons[i])
            friend_sizes.append(sizes[i])
    return [friend_bloons, friend_sizes]


def getCircle(img):
    """returns a list of circles and their sizes in image"""
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 0.7, 100,
                               param1=80, param2=7, minRadius=7,
                               maxRadius=0)
    bloons = []
    sizes = []
    if circles is not None:
        circles = circles[0]  # syntax
        for lst in circles:
            x = lst[0]
            y = lst[1]
            r = lst[2]
            if not isWhite(img, lst):
                bloons.append(lst)
                sizes.append(math.pi * r * r)
                #cv2.circle(output, (x, y), r, (0, 255, 0), 4)
    return [bloons, sizes]


def inBetween(ToCheck, BadArray, d):
    """checks if ToCheck is in the range (badArray - d, badArray + d)"""
    if (BadArray[0] - d < ToCheck[0] < BadArray[0] + d) and (
                        BadArray[1] - d < ToCheck[1] < BadArray[
                1] + d) and (BadArray[2] - d < ToCheck[2] <
                                             BadArray[2] + d):
        return True
    else:
        return False


def manyConds(ToCheck, BadArrays, ds):
    """checks if ToCheck is in one of the ranges around badArrays"""
    for i in range(len(ds)):
        if inBetween(ToCheck, BadArrays[i], ds[i]):
            return True
    return False


def isClose(color, dist):
    if abs(color[0] - color[1]) < dist and abs(color[1] - color[2]) < dist \
            and \
            abs(color[2] - color[0]) < dist:
        return True
    else:
        return False


def isRed(img, circle):
    """checks if a circle average color is red-ish"""
    circle = [int(X) for X in circle]
    xc, yc, r = circle
    cropImg = img[yc-r:yc+r, xc-r:xc+r]
    average_color = cv2.mean(cropImg)
    if red_lower[0] <= average_color[0] <= red_upper[0] and red_lower[1] <= \
            average_color[1] <= red_upper[1] and red_lower[2] <= \
            average_color[2] <= red_upper[2]:
        return True
    else:
        return False


def isRedSec(img, circle):
    """checks if a circle average color is red-ish"""
    circle = [int(X) for X in circle]
    xc, yc, r = circle
    cropImg = img[yc-r:yc+r, xc-r:xc+r]
    average_color = cv2.mean(cropImg)
    if red_lower_sec[0] <= average_color[0] <= red_upper_sec[0] and \
                            red_lower_sec[1] <= \
            average_color[1] <= red_upper_sec[1] and red_lower_sec[2] <= \
            average_color[2] <= red_upper_sec[2]:
        return True
    else:
        return False


def isWhite(img, circle):
    """checks if a circles average color is white-ish"""
    circle = [int(X) for X in circle]
    xc, yc, r = circle
    cropImg = img[yc-r:yc+r, xc-r:xc+r]
    average_color = cv2.mean(cropImg)
    if manyConds(average_color, [BAD1, BAD2, BAD3, BAD4], [d1, d2, d3,
                                                               d4]) or \
            isClose(average_color, d):
        return True
    else:
        return False

def drawCircle(img, r):
    contour = []
    xc = len(img)/2
    yc = len(img[0])/2
    for i in range(len(img)):
        for j in range(len(img[0])):
            if ((i-xc)**2+(j-yc)**2) < r**2:
                contour.append([i, j])
    return contour

def isGreen(img, circle):
    """checks if a circle average color is red-ish"""
    circle = [int(X) for X in circle]
    xc, yc, r = circle
    cropImg = img[yc - r:yc + r, xc - r:xc + r]
    # cv2.imshow("1", cropImg)
    # cv2.waitKey()
    contour = drawCircle(cropImg, r)
    average_color = [0.0, 0.0, 0.0]
    for i in range(len(cropImg)):
        for j in range(len(cropImg[0])):
            if [i, j] in contour:
                average_color = [average_color[0] + cropImg[i][j][0], average_color[1] + cropImg[i][j][1],
                                 average_color[2] + cropImg[i][j][2]]
    average_color = [average_color[0] / len(contour), average_color[1] / len(contour), average_color[2] / len(contour)]
    if lower_car[0] <= average_color[0] <= upper_car[0] and lower_car[1] <= \
            average_color[1] <= upper_car[1] and lower_car[2] <= \
            average_color[2] <= upper_car[2]:
        return True
    else:
        return False

def getCircleCar(img):
    """returns a list of circles and their sizes in image"""
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.9, 30,
                               param1=80, param2=10, minRadius=0,
                               maxRadius=15)
    bloons = []
    sizes = []
    if circles is not None:
        circles = circles[0]  # syntax
        for lst in circles:
            x = lst[0]
            y = lst[1]
            r = lst[2]
            if not isWhite(img, lst) and y > 200:
                bloons.append(lst)
                sizes.append(math.pi * r * r)
                # cv2.circle(output, (x, y), r, (0, 255, 0), 4)
    # return output
    return bloons, sizes

def getCar(img):
    """returns an array of green balloons from the regular web-cams"""

 

    options, sizes = getCircleCar(img)
    filtered = []
    for option in options:
        if isGreen(img, option):
            filtered.append(option)
    return filtered

def getOrientation(img):
    options = getLine(img, lower_line, upper_line)
    if not options:
        return None
    counter, x, y = 0.0, 0.0, 0.0
    for option in options:
        counter += 1
        x += option[2][0]
        y += option[3][0]
    x, y = x / counter, y / counter
    if inLine(np.array([x, y])):
        return 0
    return (320.0-x)/640.0*30.0

def inLine(point):
    if (point[0] > 330 or point[0] < 310):
        return False
    return True

def getLine(img, colorMin1, colorMax1):
    """checks the car's relation to the orientation line"""
    res1 = getColor1(img, colorMin1, colorMax1)
    kernel1 = np.ones((12, 12), np.uint8)
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
    if not len(contours):
        return None
    bloons = []
    for j in range(len(contours)):
        if (len(contours[j])>100):
            line = cv2.fitLine(contours[j], 1, 0, 0.01, 0.01)
            dir = np.array([line[0][0], line[1][0]])
            if abs(dir.dot(np.array([0, 1])))>0.95:
                bloons.append(line)
    return bloons