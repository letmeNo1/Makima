import cv2
import numpy as np
import pyscreeze

image_path = "./ggg.png"
img = pyscreeze.screenshot()
frame = np.array(img)
r = cv2.selectROI(frame)

if r != (0, 0, 0, 0):
    roi = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    cv2.imwrite(image_path, roi)

cv2.destroyAllWindows()
print("done")