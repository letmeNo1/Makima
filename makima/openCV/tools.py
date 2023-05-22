import time

import cv2
import numpy as np
import pyscreeze

def pic_matc(target_image):
    screenshot = pyscreeze.screenshot()
    gray_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    color_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    # 读取目标图像和待匹配图像
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
    matching_image = gray_image  # 以灰度模式读取待匹配图像

    # 初始化特征检测器和特征描述子
    sift = cv2.SIFT_create()

    # 在目标图像和待匹配图像中检测关键点和计算特征描述子
    # 在目标图像和待匹配图像中检测关键点和计算特征描述子
    keypoints1, descriptors1 = sift.detectAndCompute(target_image, None)
    keypoints2, descriptors2 = sift.detectAndCompute(matching_image, None)

    # 使用匹配器进行特征匹配
    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(descriptors1, descriptors2, k=2)

    # 应用 Lowe's ratio test 进行筛选
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # 提取匹配对的关键点坐标
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # 计算透视变换矩阵
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    if M is not None:
        # 对图像1进行透视变换
        h, w = target_image.shape
        corners = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        transformed_corners = cv2.perspectiveTransform(corners, M)
        # print([np.int32(transformed_corners)])
        rect = cv2.minAreaRect(np.int32(transformed_corners))

        # 计算最小矩形的边界框
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # # 框选匹配区域并绘制红色圈
        color_image = cv2.drawContours(color_image, [box], 0, (0, 0, 255), 2)

    # 显示结果图像
    cv2.imshow('Feature Matching', color_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



screenshot = pyscreeze.screenshot()
# 将PIL图像对象转换为OpenCV格式
image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

cv2.imshow("imshow",image,)
r = cv2.selectROI(image)
# time.sleep(2)

if r != (0, 0, 0, 0):
    roi = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

cv2.destroyAllWindows()
print("done")
pic_matc(roi)
