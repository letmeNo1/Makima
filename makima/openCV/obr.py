import cv2
import numpy as np
import pyscreeze


class OBR:
    def __init__(self, target_image, n=50):
        self.target_image = target_image
        self.value_n = n

    def pic_match(self):
        screenshot = pyscreeze.screenshot()
        gray_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        # 读取目标图像和待匹配图像
        target_image_gray = cv2.cvtColor(self.target_image, cv2.COLOR_BGR2GRAY)
        matching_image = gray_image  # 以灰度模式读取待匹配图像

        # 初始化特征检测器和特征描述子
        orb = cv2.ORB_create()

        # 在目标图像和待匹配图像中检测关键点和计算特征描述子
        keypoints1, descriptors1 = orb.detectAndCompute(target_image_gray, None)
        keypoints2, descriptors2 = orb.detectAndCompute(matching_image, None)

        # 使用匹配器进行特征匹配
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = matcher.match(descriptors1, descriptors2)

        # 对匹配结果按距离进行排序
        matches = sorted(matches, key=lambda x: x.distance)

        # 选择前N个最佳匹配结果
        good_matches = matches[:self.value_n]

        # 提取匹配对的关键点坐标
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 计算透视变换矩阵
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        if M is not None:
            # 对图像1进行透视变换
            h, w = target_image_gray.shape
            corners = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
            transformed_corners = cv2.perspectiveTransform(corners, M)
            # print([np.int32(transformed_corners)])
            rect = cv2.minAreaRect(np.int32(transformed_corners))

            # 计算最小矩形的边界框
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            center_x = int((box[0][0] + box[2][0]) / 2)
            center_y = int((box[0][1] + box[2][1]) / 2)
            return center_x, center_y


# screenshot = pyscreeze.screenshot()
# # 将PIL图像对象转换为OpenCV格式
# image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
#
# cv2.imshow("imshow",image,)
# r = cv2.selectROI(image)
# # time.sleep(2)
#
# if r != (0, 0, 0, 0):
#     roi = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
#     cv2.imwrite("marked_image.png", image)
#
# cv2.destroyAllWindows()
# print("done")
# obj = OBR(roi).pic_match()
# print(obj)
