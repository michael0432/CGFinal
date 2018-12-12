import cv2
import numpy as np
from operator import itemgetter
import sys
import math
import random

def paint(sourceImage, *arg):

    # style parameters
    fs = 0.5

    #cv2.imshow("input", sourceImage)
    # canvas := a new constant color image
    height, width = sourceImage.shape[:2]
    canvas = np.zeros([height, width, 3])
    canvas.fill(255)
    # paint the canvas
    # print(sorted(arg,reverse=True))
    # for each brush radius Ri,from largest to smallest do
    for brushSize in sorted(arg, reverse=True):
        # apply Gaussian blur
        # referenceImage = sourceImage * G(fs Ri)
        # print(brushSize)
        referenceImage = cv2.GaussianBlur(sourceImage, ksize=(5, 5), sigmaX=fs*brushSize, sigmaY=fs*brushSize)
        #cv2.imshow("burred", referenceImage)
        #ref_img = cv2.GaussianBlur(sourceImage, ksize=(5,5), sigmaX=blur_factor*brushSize)
        #cv2.imshow("ref_img", ref_img)
        # paint a layer
        canvas = paintLayer(canvas, referenceImage, brushSize)
        cv2.imshow("canvas", canvas)

    return canvas


def paintLayer(canvas, referenceImage, R):

    fg = 1
    T = 1

    cv2.imshow("referenceImage", referenceImage)
    height, width = referenceImage.shape[:2]
    # S: = a new set of strokes, initially empty
    S = []
    # create a pointwise difference image
    # D: = difference(canvas, referenceImage)
    #D = difference(canvas, referenceImage)
    D = canvas - referenceImage
    #cv2.imshow("D", D)
    # grid: = fg R
    grid = fg * R
    # for x = 0 to imageWidth stepsize grid do
    # for y = 0 to imageHeight stepsize grid do
    for x in range(0, height, grid):
        for y in range(0, width, grid):
            # sum the error near(x, y)
            # M: = the region(x-grid/2..x+grid/2,y-grid/2..y+grid/2)
            # areaError: = åi, jÎM Di, j / grid2
            M = D[int(x-grid/2):int(x+grid/2), int(y-grid/2):int(y+grid/2)]
            areaError = M.sum() / (grid*grid)
            #print(D[x][y])

            max = -sys.maxsize - 1
            # if (areaError > T) then
            if(areaError > T):
                # find the largest error point
                # (x1, y1): = arg max i, jÎM Di, j
                for i in range(int(x-grid/2), int(x+grid/2)):
                    for j in range(int(y-grid/2), int(y+grid/2)):
                        if(i < height and j < width):
                            #print(i, j, width, height)
                            #print(D[i][j])
                            if(math.sqrt(pow(D[i][j][0], 2) + pow(D[i][j][1], 2) + pow(D[i][j][2], 2)) > max):
                                max = math.sqrt(pow(D[i][j][0], 2) + pow(D[i][j][1], 2) + pow(D[i][j][2], 2))
                                x1 = i
                                y1 = j
                # print(max)
                # s: = makeStroke(R, x1, y1, referenceImage)
                #s = makeSplineStroke(R, x1, y1, referenceImage, canvas)
                b = int(referenceImage[x][y][0])
                print(b)
                cv2.circle(canvas, (y1, x1), R, (int(referenceImage[x1,y1][0]),int(referenceImage[x1,y1][1]),int(referenceImage[x1,y1][2])), -1)
                # cv2.circle(canvas, (y1, x1), R, (b,0,0), -1)
                #cv2.circle(canvas, (y1, x1), R, (0,0,0), -1)
                # add s to S
                #S += [s]

    #print(S)
    # paint all strokes in S on the canvas,in random order
    
    #np.random.shuffle(S)
    #for i in range(0,len(S)):
    #    #print(S[i][1])
        #print(type(S[i][1][0]))
    #    for j in range(2,len(S[i])):
    #        cv2.circle(canvas, (int(S[i][j][0]), int(S[i][j][1])), S[i][0], S[i][1], -1)
    return canvas
    



def makeSplineStroke(R, x0, y0, refImage, canvas):

    maxStrokeLength = 16
    minStrokeLength = 4
    fc = 1

    height, width = canvas.shape[:2]

    #strokeColor = refImage.color(x0, y0)
    bs, gs, rs = refImage[int(x0), int(y0)]
    strokeColor = [int(bs),int(gs),int(rs)]
    #K = a new stroke with radius:R and color:strokeColor
    K = [] # 0：radius 1：color
    K += [R]
    K += [strokeColor]
    #add point(x0, y0) to K
    #(x, y): = (x0, y0)
    x = x0
    y = y0
    #(lastDx, lastDy): = (0, 0)
    lastDx = 0
    lastDy = 0
    #for i = 1 to maxStrokeLength do
    for i in range(1,maxStrokeLength):
        if(x > height or y > width):
            return K
        #if (i > minStrokeLength and | refImage.color(x, y)-canvas.color(x, y) | < | refImage.color(x, y)-strokeColor |) then
        #if(i > minStrokeLength and abs(diffPixel(canvas,refImage,x,y,x,y)) < abs(diffPixel(refImage,refImage,x,y,x0,y0))):
        #if(i > minStrokeLength and abs(canvas[x][y] - refImage[x][y]) < abs(refImage[x][y] - refImage[x0],[y0])):
        diffvalue1 = canvas[int(x)][int(y)] - refImage[int(x)][int(y)]
        diffvalue2 = refImage[int(x)][int(y)] - refImage[int(x0)][int(y0)]
        if(i > minStrokeLength and math.sqrt(pow(diffvalue1[0], 2) + pow(diffvalue1[1], 2) + pow(diffvalue1[2], 2)) < math.sqrt(pow(diffvalue2[0], 2) + pow(diffvalue2[1], 2) + pow(diffvalue2[2], 2))): 
            #return K
            return K
        #detect vanishing gradient
        #if (refImage.gradientMag(x, y) == 0) then
        b, g, r = refImage[int(x), int(y)]
        gradientMag = 0.30*r + 0.59*g + 0.11*b
        if(gradientMag == 0):
            #return K
            return K
        #print(gradientMag)
        #get unit vector of gradient
        #(gx, gy): = refImage.gradientDirection(x, y)
        gx = -math.sin(gradientMag)
        gy = math.cos(gradientMag)
        #compute a normal direction
        #(dx, dy): = (-gy, gx)
        dx, dy = -gy, gx
        #if necessary, reverse direction
        #if (lastDx * dx + lastDy * dy < 0) then
        if(lastDx * dx + lastDy * dy < 0):
            #(dx, dy): = (-dx, -dy)
            dx, dy = -dx, -dy
        #filter the stroke direction
        #(dx, dy): = fc*(dx, dy)+(1-fc)*(lastDx, lastDy)
        dx = fc * dx + (1 - fc) * lastDx
        dy = fc * dy + (1 - fc) * lastDy
        #(dx, dy): = (dx, dy)/(dx2 + dy2)1/2
        dx = dx / math.sqrt(pow(dx,2) + pow(dy,2))
        dx = dy / math.sqrt(pow(dx,2) + pow(dy,2))
        #(x, y): = (x+R*dx, y+R*dy)
        x = x + R * dx
        y = y + R * dy
        #(lastDx, lastDy): = (dx, dy)
        lastDx = dx
        lastDy = dy
        #add the point(x, y) to K
        K += [[dx, dy]]
    #return K
    return K

"""
def diffPixel(canvas, referenceImage, x1, y1, x2, y2):
    rc, gc, bc = canvas[int(x1), int(y1)]
    bi, gi, ri = referenceImage[int(x2), int(y2)]
    return math.sqrt(pow(ri - rc, 2) + pow(gi - gc, 2) + pow(bi - bc, 2))

def difference(canvas, referenceImage):
    height, width = canvas.shape[:2]
    diff = np.zeros((height, width))
    for i in range(0, height):
        for j in range(0, width):
            bi, gi, ri = referenceImage[i, j]
            # print(ri,gi,bi)
            rc, gc, bc = canvas[i, j]
            diff[i][j] = math.sqrt(pow(ri - rc, 2) + pow(gi - gc, 2) + pow(bi - bc, 2))
    return diff
"""

source = cv2.imread("./testimg/i2.jpg")
#cv2.imshow("input", source)
output = paint(source, 8, 4, 2)
cv2.imshow("oilpaint", output)
cv2.waitKey(0)
