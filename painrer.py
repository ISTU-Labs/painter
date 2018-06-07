﻿с добавлением проверки на текстуру

import numpy as np
import random
import math
import cv2

color = cv2.imread("photos/ineshin/1.jpg")
BlackAndWhite = cv2.imread("photos/ineshin/22.jpg")


def fY(R, G, B):
    res = 0.299 * R + 0.526 * G + 0.114 * B
    return res


height = np.size(color, 0)
width = np.size(color, 1)
Ycl = []
RGB = []
Sgcl = []
TTcl = []


def middle(randI, randJ, img):
    Rm = 0
    Gm = 0
    Bm = 0
    for k in range(randI - 2, randI + 3, 1):
        for l in range(randJ - 2, randJ + 3, 1):
            RGBokr = img[k, l]
            Rm += RGBokr[0]
            Gm += RGBokr[1]
            Bm += RGBokr[2]
    Rm = Rm/N
    Gm = Gm/N
    Bm = Bm/N
    return Rm, Gm, Bm


def calcSg(randI, randJ, img):
    Sum = 0
    mRGB = middle(randI, randJ, img)
    for k in range(randI - 2, randI + 3, 1):
        for l in range(randJ - 2, randJ + 3, 1):
            RGBcl = img[k, l]
            Sum += \
                ((RGBcl[0] - mRGB[0]) ** 2) + \
                ((RGBcl[1] - mRGB[1]) ** 2) + \
                ((RGBcl[2] - mRGB[2]) ** 2)
    res = (1 / (N - 1)) * Sum
    return res


def vost(i):
    r = RGB[i][0]
    g = RGB[i][1]
    b = RGB[i][2]
    return r, g, b


def texture(randI, randJ, img):
    TT = []
    y = 0
    yC = fY(img[randI, randJ][0], img[randI, randJ][1], img[randI, randJ][2])
    for i in range(randI - 2, randI + 3, 1):
        for j in range(randJ - 2, randJ + 3, 1):
            TT = []
            for k in range(i - 1, i + 2, 1):
                for l in range(j - 1, j + 2, 1):
                    if k != i and l != j:
                        rgb = img[k, l]
                        y = fY(rgb[0], rgb[1], rgb[2])
                    if y <= yC:
                        TT.append(0)
                    else:
                        TT.append(1)
                    mm = TT.count(1)
                    TT[mm - 1] += 1
    Tmax = 0
    Tid = 0
    for i in range(0, len(TT), 1):
        if TT[i] > Tmax:
            Tmax = TT[i]
            Tid = i

    return Tid


N = 25
set = 15
print("Phase 1")
step1 = int(math.floor(height / set))
step2 = int(math.floor(width / set))
hh = set * step1
ww = set * step2
for i in range(0, hh-step1, step1):
    for j in range(0, ww-step2, step2):
        randI = random.randint(i+3, i + step1-3)
        randJ = random.randint(j+3, j + step2-3)
        RGBcl = color[randI, randJ]
        Ycl.append(fY(RGBcl[0], RGBcl[1], RGBcl[2]))
        RGB.append(RGBcl)
        Sgcl.append(calcSg(randI, randJ, color))
        TTcl.append(texture(randI, randJ, color))

print("Phase 2")
height2 = np.size(BlackAndWhite, 0)
width2 = np.size(BlackAndWhite, 1)
for i in range(0, height2, 1):
    for j in range(1, width2-1, 1):
        Dmin = 10000
        D = []
        ID = 0
        RGBbw = BlackAndWhite[i, j]
        Ybw = RGBbw[0]
        Sgbw = calcSg(i, j, BlackAndWhite)
        TTbw = texture(i, j, BlackAndWhite)
        for k in range(0, len(Ycl), 1):
            D.append(abs(Ybw-Ycl[k])*0.5 + abs(math.sqrt(Sgbw) -
                                               math.sqrt(Sgcl[k])*0.5)+abs(TTbw-TTcl[k])*0.5)
        for k in range(0, len(Ycl), 1):
            if D[k] < Dmin:
                Dmin = D[k]
                ID = k
        BlackAndWhite[i, j] = vost(ID)

print("Writing end")
cv2.imwrite("photos/ineshin/22.jpg", BlackAndWhite)
