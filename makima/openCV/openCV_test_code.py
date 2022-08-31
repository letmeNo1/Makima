import numpy as np
import cv2
import pyautogui
from matplotlib import pyplot as plt
from sklearn.neighbors import LocalOutlierFactor


# img = pyautogui.screenshot()
# print(img)
# img1 = np.array(img)
img1 = cv2.imread('C:\\Users\\hanhuang\\1.png', 0)  # trainImage
img2 = cv2.imread('C:\\Users\\hanhuang\\2.png', 0)  # trainImage


img1 = img1[100:900, 50:1850]
img2 = img2[100:900, 50:1850]

# image = img1[100:900, 50:1850]
# plt.imshow(image)
# plt.show()
# Initiate SIFT detector
sift = cv2.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)  # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params, search_params)

# 使用基于FLANN的匹配器, 筛选符合条件的坐标
matches = flann.knnMatch(des1, des2, k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0, 0] for i in range(len(matches))]

result = []
good = []

# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    # distance越小匹配度越高
    if m.distance < 0.4 * n.distance:
        good.append(m)
        result.append(kp1[m.queryIdx].pt)
        matchesMask[i] = [1, 0]

x_of_point1_of_transform_image = 0
y_of_point1_of_transform_image = 0
x_of_point3_of_transform_image = 0
y_of_point3_of_transform_image = 0
x = 0
y = 0

MIN_MATCH_COUNT = 10
if len(good) > MIN_MATCH_COUNT:
    # Gets the coordinates of the key points
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    # Compute the transformation matrix and MASK
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    h, w = img1.shape

    # Calculate the original image size
    original_image_size = h * w

    # Use the transformation matrix to obtain the coordinates of the four corners of the original image after
    # transformation
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    # Get the coordinates of the lower right corner of the transformed image
    x_of_point1_of_transform_image = [np.int32(dst)][0][0][0][0]
    y_of_point1_of_transform_image = [np.int32(dst)][0][0][0][1]

    # Get the coordinates of the lower right corner of the transformed image
    x_of_point3_of_transform_image = [np.int32(dst)][0][2][0][0]
    y_of_point3_of_transform_image = [np.int32(dst)][0][2][0][1]

    print(x_of_point1_of_transform_image, y_of_point1_of_transform_image)
    print(x_of_point3_of_transform_image, y_of_point3_of_transform_image)

    x = (x_of_point3_of_transform_image + x_of_point1_of_transform_image) / 2
    y = (y_of_point3_of_transform_image + y_of_point1_of_transform_image) / 2

draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(255, 0, 0),
                   matchesMask=matchesMask,
                   flags=0)

output_image = cv2.drawKeypoints(img2, kp1, 0, (0, 0, 255),
                                 flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

# displaying the image with keypoints as the
# output on the screen

plt.imshow(output_image)

# plotting image
plt.show()

img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
cv2.imshow("绘制矩形", img3)
cv2.waitKey(100000)


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
# cv2.imshow("绘制矩形", image)
# cv2.waitKey(100000)
