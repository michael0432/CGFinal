import cv2
import sys
# src = cv2.imread(sys.argv[1])
# dst_gray, dst_color = cv2.pencilSketch(src, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
# cv2.imwrite('./testout/pencil_1.jpg',dst_gray)

for i in range(0,769):
    src = cv2.imread('./videoframe/frame'+str(i)+'.jpg')
    dst_gray, dst_color = cv2.pencilSketch(src, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    cv2.imwrite('./videoframeAfterProcessing/frame'+str(i)+'.jpg',dst_gray)