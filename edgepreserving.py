import sys
import cv2

# src = cv2.imread(sys.argv[1])
# dst = cv2.edgePreservingFilter(src, flags=1, sigma_s=60, sigma_r=0.2)
# cv2.imwrite('./testout/edgepreserving2.jpg',dst)

for i in range(0,769):
    src = cv2.imread('./videoframe/frame'+str(i)+'.jpg')
    dst = cv2.edgePreservingFilter(src, flags=1, sigma_s=60, sigma_r=0.2)
    cv2.imwrite('./videoframeAfterProcessing/frame'+str(i)+'.jpg',dst)