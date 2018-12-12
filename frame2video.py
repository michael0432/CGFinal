import cv2

videoWriter = cv2.VideoWriter('./outputvideo/birdout.mp4', 0x00000021, 25, (1280,720))

for i in range(0,769):
    img = cv2.imread('./videoframeAfterProcessing/frame'+str(i)+'.jpg')
    videoWriter.write(img)