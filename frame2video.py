import cv2
import sys

videoWriter = cv2.VideoWriter(sys.argv[2], 0x00000021, 25, (1280,720))

for i in range(0,int(sys.argv[3])):
    img = cv2.imread(sys.argv[1]+'/frame'+str(i)+'.jpg')
    videoWriter.write(img)