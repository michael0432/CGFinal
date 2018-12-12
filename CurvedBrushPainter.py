import cv2
import numpy as np
import sys
import random
# params
Approximation_threshold = 1
Brush_size = [8,4,2]
Curvature_Filter = 1
Blur_Factor = 9
Grid_size = 1

def paint(s_img,brush_size):
    canvas = np.zeros((s_img.shape[0],s_img.shape[1],3), np.uint8)
    canvas.fill(255)
    for i in brush_size:
        ref_img = cv2.GaussianBlur(s_img,(Blur_Factor,Blur_Factor),0)
        canvas = paintLayer(canvas,ref_img,i)
        
    return canvas

def paintLayer(canvas,r_img,radius):
    Strokes = []
    dif = difference(canvas,r_img)
    grid = Grid_size*radius

    # for spline
    r_img_gray = cv2.cvtColor(r_img, cv2.COLOR_BGR2GRAY)
    r_img_dx = cv2.Sobel(r_img_gray,cv2.CV_32F,1,0)
    r_img_dy = cv2.Sobel(r_img_gray,cv2.CV_32F,0,1)
    r_img_mag = cv2.magnitude(r_img_dx,r_img_dy)
    r_img_gradient_dir = cv2.phase(r_img_dx,r_img_dy)
    # print(r_img_gradient_dir.shape)
    # for spline

    for x in range(grid,r_img.shape[0]-grid,grid):
        for y in range(grid,r_img.shape[1]-grid,grid):
            D = dif[(x-int(grid/2)):(x+int(grid/2)),(y-int(grid/2)):(y+int(grid/2))]
            area_error = (np.sum(D)) / (grid ** 2)
            if area_error > Approximation_threshold:
                max_index = np.unravel_index(D.argmax(), D.shape)
                s = makeStroke(radius,x-int(grid/2)+max_index[0],y-int(grid/2)+max_index[1],r_img)
                # s2 = makeSplineStroke(canvas,radius,x-int(grid/2)+max_index[0],y-int(grid/2)+max_index[1],r_img,r_img_gray)
                Strokes.append(s)
    # make circle stroke           
    Strokes_size = len(Strokes)
    # for i in range(Strokes_size):
    #     randi = random.randint(0,len(Strokes)-1)
    #     cv2.circle(canvas,(Strokes[randi][1], Strokes[randi][0]),Strokes[randi][2], (int(Strokes[randi][3][0]),int(Strokes[randi][3][1]),int(Strokes[randi][3][2])), -1)
    #     Strokes.remove(Strokes[randi])
    for i in range(Strokes_size):
        cv2.circle(canvas,(Strokes[i][1], Strokes[i][0]),Strokes[i][2], (int(Strokes[i][3][0]),int(Strokes[i][3][1]),int(Strokes[i][3][2])), -1)

    # make Spline stroke
    
    return canvas 
    
def makeStroke(radius,x,y,r_img):
    return [x,y,radius,r_img[x,y]]

def makeSplineStroke(canvas,radius,x,y,r_img,r_img_mag):
    stroke_color = r_img[x,y]
    K = [[[x,y]],radius,r_img[x,y]]
    dif = difference(canvas,r_img)
    nowxy = [x,y]
    lastDxDy = np.array([0,0])
    MaxLen = 30
    MinLen = 5
    
    for i in range(1,MaxLen):
        if (i > MinLen) and np.linalg.norm((r_img[nowxy[0],nowxy[1]] - canvas[nowxy[0],nowxy[1]])) > np.linalg.norm((r_img[nowxy[0],nowxy[1]] - stroke_color)):
            return K
        if r_img_mag[nowxy[0],nowxy[1]] == 0:
            return K



def difference(img1,img2):
    return np.sum((img1 - img2) ** 2 ,axis = 2)

def deal_white(img):
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if img[x][y][0] == 255 and img[x][y][1] == 255 and img[x][y][2] == 255:
                img[x][y] = img[x][y-1]
    return img

for i in range(0,684):
    src = cv2.imread('./videoframe/frame'+str(i)+'.jpg')
    dst = cv2.edgePreservingFilter(src, flags=1, sigma_s=60, sigma_r=0.2)
    cv2.imwrite('./videoframeAfterProcessing/frame'+str(i)+'.jpg',deal_white(paint(src,Brush_size)))
# source_image = cv2.imread(sys.argv[1])

# cv2.imwrite('./testout/out4.jpg',deal_white(paint(source_image,Brush_size)))
