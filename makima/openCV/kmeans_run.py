import numpy as np
import cv2
import pyautogui

from makima.openCV.lof import LOF


def kmeans_run(path, distance=0.4):
    img = pyautogui.screenshot()

    img1 = np.array(img)
    img2 = cv2.imread(path,
                      0)
    # 初始化SIFT选择器
    sift = cv2.SIFT_create()

    # 检测关键点并计算描述符
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # FLANN 参数
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # 使用基于FLANN的匹配器, 筛选符合条件的坐标
    matches = flann.knnMatch(des1, des2, k=2)

    # ratio test as per Lowe's paper
    result = []
    for i, (m, n) in enumerate(matches):
        # distance越小匹配度越高
        if m.distance < distance * n.distance:
            result.append(kp1[m.queryIdx].pt)

    if not result or len(result)<2:
        return None, None
    else:
        return LOF(result)

