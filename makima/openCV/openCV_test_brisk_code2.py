import cv2
import numpy as np
import pyscreeze

img2 = cv2.imread('C:\\Users\\hanhuang\\test.png', 0)  # trainImage
img1 = pyscreeze.screenshot()
img1 = np.array(img1)


# Initiate SIFT detector
BRISK = cv2.BRISK_create()

BFMatcher = cv2.BFMatcher(normType=cv2.NORM_HAMMING,
                          crossCheck=True)

# find the keypoints and descriptors with SIFT
kp1, des1 = BRISK.detectAndCompute(img1, None)
kp2, des2 = BRISK.detectAndCompute(img2, None)

# FLANN parameters

#
matches = BFMatcher.match(queryDescriptors=des1,
                          trainDescriptors=des2)

matchesMask = [[0, 0] for i in range(len(matches))]

# Need to draw only good matches, so create a mask
matches = sorted(matches, key=lambda x: x.distance)

# FLANN_INDEX_KDTREE = 0
# index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
# search_params = dict(checks=100)  # or pass empty dictionary
# flann = cv2.FlannBasedMatcher(index_params, search_params)
#
# matches = flann.knnMatch(des1, des2, k=2)
# matchesMask = [[0, 0] for i in range(len(matches))]


draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(255, 0, 0),
                   matchesMask=matchesMask,
                   flags=0)

output_image = cv2.drawKeypoints(img2, kp1, 0, (0, 0, 255),
                                 flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

# displaying the image with keypoints as the
# output on the screen

# Draw first 15 matches
output = cv2.drawMatches(img1=img1,
                         keypoints1=kp1,
                         img2=img2,
                         keypoints2=kp2,
                         matches1to2=matches[:15],
                         outImg=None,
                         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


#
# window_name = 'Image'
#
# # Center coordinates
# center_coordinates = (int(x), int(y))
# print(center_coordinates)
#
# # Radius of circle
# radius = 20
#
# # Blue color in BGR
# color = (0, 0, 0)
#
# # Line thickness of 2 px
# thickness = 2
#
# print(x_of_point1_of_transform_image)
# # Using cv2.circle() method
# # Draw a circle with blue line borders of thickness of 2 px
# cv2.circle(img2, center_coordinates, 10, (255, 0, 0), 2)
# cv2.rectangle(img2, (x_of_point1_of_transform_image, y_of_point1_of_transform_image),
#               (x_of_point3_of_transform_image, y_of_point3_of_transform_image), (255, 0, 0), 2)  # 画大矩形
# image = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)  # 色彩空间转换
cv2.imshow("绘制矩形", output)
cv2.waitKey(100000)
