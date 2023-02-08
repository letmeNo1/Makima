import cv2
import numpy as np

def kmeans_run(path, path2,distance=0.7, algorithms_name="SIFT"):
    algorithms_all = {
        "SIFT": cv2.SIFT_create(),
        "BRISK": cv2.BRISK_create(),
        "ORB": cv2.ORB_create()
    }
    algorithms = algorithms_all[algorithms_name]

    img2 = cv2.imread(path2, 0)
    img1 = cv2.imread(path, 0)

    # img2 = cv2.imread('C:\\Users\\hanhuang\\Untitled.png')
    # 检测关键点并计算描述符
    kp1, des1 = algorithms.detectAndCompute(img1, None)
    kp2, des2 = algorithms.detectAndCompute(img2, None)

    if algorithms_name == "BRISK" or algorithms_name == "ORB":
        BFMatcher = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = BFMatcher.knnMatch(des1, des2, k=2)

    else:
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary

        # 使用基于FLANN的匹配器, 筛选符合条件的坐标
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

    result = []
    good = []
    for i, (m, n) in enumerate(matches):
        # distance越小匹配度越高
        if m.distance < distance * n.distance:
            good.append(m)
            result.append(kp1[m.queryIdx].pt)

    if len(good) > 5:
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

        x = (x_of_point3_of_transform_image + x_of_point1_of_transform_image) / 2
        y = (y_of_point3_of_transform_image + y_of_point1_of_transform_image) / 2
        output = cv2.rectangle(img2, (x_of_point1_of_transform_image, y_of_point1_of_transform_image), (x_of_point3_of_transform_image, y_of_point3_of_transform_image), (0, 0, 255), 3)
        cv2.imshow("绘制矩形", output)
        cv2.waitKey(0)
        return x, y
    else:
        return None, None

def find_contours(imgname):
    img = cv2.imread(imgname)
    margin_top = 100
    margin_left = 70

    img_copy = img[100:220, 70:]
    cv2.imshow('img', img_copy)

    img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('img_gray', img_gray)

    ret, thresh = cv2.threshold(img_gray, 125, 255, cv2.THRESH_BINARY)
    # cv2.imshow('thresh', thresh)

    img_inverted = cv2.bitwise_not(thresh)

    # 显示反转后的图像
    cv2.imshow("Inverted Image", img_inverted)
    cv2.waitKey(0)


    dilate_picture = cv2.dilate(img_inverted, None, iterations=4)
    cv2.imshow('dilate_picture', dilate_picture)

    all_contours_areas =[]
    contours, hierarchy = cv2.findContours(dilate_picture, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)

    for c in range(len(contours)):
        all_contours_areas.append(cv2.contourArea(contours[c]))
        # get area of max contours (find LED light area) and Analyze the current LED light color
    if all_contours_areas:
        # get area of max contours
        max_id = all_contours_areas.index(max(all_contours_areas))
        min_rect = cv2.minAreaRect(contours[max_id])
        box = np.int0(cv2.boxPoints(min_rect))
        # cv2.drawContours(img_copy, [box], -1, (0, 255, 0), 3)
        # cv2.imshow("Image", img_copy)
        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        x2 = max(Xs)
        y1 = min(Ys)
        y2 = max(Ys)

        hight = y2 - y1
        width = x2 - x1
        cropImg = img_copy[abs(y1):y1+hight, abs(x1):x1+width]
        cv2.imshow('img2', img_copy[abs(y1):y1+hight, abs(x1):x1+width])
        cv2.imwrite("result.png", cropImg)
        # cv2.waitKey(0)




        # draw_img = cv2.rectangle(img_copy, min_rect, (0, 0, 255), 3)
        # draw_img = cv2.rectangle(img, (min_rect[0]+70,min_rect[1]+100,min_rect[2],min_rect[3]), (0, 0, 255), 3)
    #
    # color_area = img[int(max_rect[0][1] - max_rect[1][1] / 2): int(max_rect[0][1] + max_rect[1][1] / 2),
    #              int(max_rect[0][0] - max_rect[1][0] / 2): int(max_rect[0][0] + max_rect[1][0] / 2)]




if __name__ == "__main__":
    img = "sss1.png"
    img2 = "sss2.png"
    res = "result.png"
    find_contours(img)
    print(kmeans_run(img2,res,0.9))