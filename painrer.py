import numpy as np
import random
import math
import cv2


# import pudb
# pu.db


color = cv2.imread("ineshin/4.jpg")
BlackAndWhite = cv2.imread("ineshin/5bw.jpg")

# cv2.imshow("color image", color)
# cv2.waitKey(0)


def fY(R, G, B):
    res = 0.299 * R + 0.526 * G + 0.114 * B
    return res


def fCb(R, G, B):
    res = 128-0.169*R-0.331*G+0.500*B
    return res


def fCr(R, G, B):
    res = 128+0.500*R-0.419*G-0.081*B
    return res


height = np.size(color, 0)
width = np.size(color, 1)
Ycl = []
Cb = []
Cr = []
Sgcl = []
D = []
N = 25
step = 15
ID = 1

#gray = fY(color[:, :, 0], color[:, :, 1], color[:, :, 2])
#cv2.imwrite("ineshin/4-bw.jpg", gray)


def middle(randI, randJ):
    Rm = 0
    Gm = 0
    Bm = 0
    for k in range(randI - 2, randI + 3, 1):
        for l in range(randJ - 2, randJ + 3, 1):
            RGBokr = color[k, l]


# IndexError: index 2298 is out of bounds for axis 1 with size 2296

            Rm += RGBokr[0]
            Gm += RGBokr[1]
            Bm += RGBokr[2]
    Rm = Rm/N
    Gm = Gm/N
    Bm = Bm/N
    return Rm, Gm, Bm


def calcSg(randI, randJ):
    Sum = 0
    mRGB = middle(randI, randJ)
    for k in range(randI - 2, randI + 3, 1):
        for l in range(randJ - 2, randJ + 3, 1):
            RGBcl = color[k, l]
            Sum += \
                ((RGBcl[0] - mRGB[0]) ** 2) + \
                ((RGBcl[1] - mRGB[1]) ** 2) + \
                ((RGBcl[2] - mRGB[2]) ** 2)
    res = (1 / (N - 1)) * Sum
    return res


def vost(i):
    r = Ycl[i]+(Cb[i]-128)+(Cr[i]+128)
    g = Ycl[i] - 0.343*(Cb[i]-128) - 0.711*(Cr[i]+128)
    b = Ycl[i] + 1.765*(Cr[i]-128)
    return r, g, b


print("Phase 1")

for i in range(0, height - step, height / step):
    for j in range(0, width - step, width / step):
        randI = random.randint(i, i + step)
        randJ = random.randint(j, j + step)
        RGBcl = color[randI, randJ]
        Ycl.append(fY(RGBcl[0], RGBcl[1], RGBcl[2]))
        Cb.append(fCb(RGBcl[0], RGBcl[1], RGBcl[2]))
        Cr.append(fCr(RGBcl[0], RGBcl[1], RGBcl[2]))
        Sgcl.append(calcSg(randI, randJ))
        # List of Standard Deviations in a Square


print("Phase 2")
height2 = np.size(BlackAndWhite, 0)
width2 = np.size(BlackAndWhite, 1)

Dmin = 10000000
for i in range(0, height2-1, 1):
    for j in range(0, width2 - 1, 1):
        RGBbw = BlackAndWhite[i, j]
        Ybw = RGBbw[0]
        Sgbw = calcSg(i, j)
        for k in range(0, len(Sgcl), 1):
            D.append(abs(Ybw-Ycl[k])*0.5 +
                     abs(math.sqrt(Sgbw) - math.sqrt(Sgcl[k])*0.5))
        for k in range(0, len(D), 1):
            if D[k] < Dmin:
                Dmin = D[k]
                ID = k
        BlackAndWhite[i, j] = vost(k)

print("Writing result")

cv2.imwrite("ineshin/5bw.jpg", BlackAndWhite)
