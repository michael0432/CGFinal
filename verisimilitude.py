import cv2
import sys
import numpy as np
import color
source_image = cv2.imread(sys.argv[1])
target_image = cv2.imread(sys.argv[2])
source_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2LAB)
target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2LAB)
src_data_average = np.array([np.average(source_image[0]),np.average(source_image[1]),np.average(source_image[2])])
src_data_std = np.array([np.std(source_image[0]),np.std(source_image[1]),np.std(source_image[2])])
target_data_average = np.array([np.average(target_image[0]),np.average(target_image[1]),np.average(target_image[2])])
target_data_std = np.array([np.std(target_image[0]),np.std(target_image[1]),np.std(target_image[2])])

# color adjustment
dst_lab = (source_image - src_data_average) * (target_data_std / src_data_std) + target_data_average
dst_lab = dst_lab.astype(np.uint8)
dst_lab = cv2.cvtColor(dst_lab, cv2.COLOR_LAB2BGR)
cv2.imwrite('./testout/coloradjust.jpg',dst_lab)