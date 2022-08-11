import numpy as np
import cv2
import pyautogui
from sklearn.neighbors import LocalOutlierFactor


def LOF(data):
    point_of_x = []
    point_of_y = []
    k = len(data) if len(data) < 6 else 6
    clf = LocalOutlierFactor(n_neighbors=k, algorithm='auto', contamination=0.1, n_jobs=-1, novelty=False)
    clf.fit_predict(data)
    for index, outlier in enumerate(clf.negative_outlier_factor_):
        if 1.1 > abs(outlier) > 0.9:
            point_of_x.append(data[index][0])
            point_of_y.append(data[index][1])
    return [np.mean(point_of_x), np.mean(point_of_y)]


img = pyautogui.screenshot()
print(img)
img1 = np.array(img)
# img1 = cv2.imread('C:\\Users\\hanhuang\\OneDrive - GN Store Nord\\Desktop\\001.png',0)          # queryImage
img2 = cv2.imread('C:\\Users\hanhuang\\OneDrive - GN Store Nord\\Desktop\\0002.png',0) # trainImage

# Initiate SIFT detector
sift = cv2.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params,search_params)

# 使用基于FLANN的匹配器, 筛选符合条件的坐标
matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]


result = []
# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    # distance越小匹配度越高
    if m.distance < 0.4*n.distance:
        result.append(kp1[m.queryIdx].pt)
        matchesMask[i]=[1,0]


draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 0)

img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

plt.imshow(img3),plt.show()
aa = LOF(result)
print(aa)

window_name = 'Image'

# Center coordinates
center_coordinates = (int(aa[0]), int(aa[1]))

# Radius of circle
radius = 20

# Blue color in BGR
color = (0, 0, 0)

# Line thickness of 2 px
thickness = 2

# Using cv2.circle() method
# Draw a circle with blue line borders of thickness of 2 px
image = cv2.circle(img1, center_coordinates, radius, color, thickness)

# Displaying the image
plt.imshow(image),plt.show()

