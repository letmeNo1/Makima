import cv2
import numpy as np
import pyscreeze
import tkinter
from tkinter import filedialog

src_path = None
part_path = None
def openfile():  # 打开文件并显示
    global src_path
    src_path = filedialog.askopenfilename()  # 获得选择好的文件,单个文件
    imgtype = [".jpg", ".png"]  # 规定读取的文件类型
    if str(src_path)[-4:] in imgtype:
        print("打开文件", src_path)

    else:
        tkinter.messagebox.showinfo('提示', '请选择.jpg .png 图片')

def openfile2():  # 打开文件并显示
    global part_path
    part_path = filedialog.askopenfilename()  # 获得选择好的文件,单个文件
    imgtype = [".jpg", ".png"]  # 规定读取的文件类型
    if str(part_path)[-4:] in imgtype:
        print("打开文件", part_path)

    else:
        tkinter.messagebox.showinfo('提示', '请选择.jpg .png 图片')


def recognition():
    img1 = None
    img2 = None
    algorithms_name = variable.get()
    distance = float(variable2.get())
    print(distance)
    algorithms_all = {
        "SIFT": cv2.SIFT_create(),
        "BRISK": cv2.BRISK_create(),
        "ORB": cv2.ORB_create()
    }
    algorithms = algorithms_all[algorithms_name]


    if part_path is None:
        tkinter.messagebox.askokcancel(message='Please pass the picture first')
        return 0
    else:
        img1 = cv2.imread(part_path, 0)

    if src_path is None:
        img = pyscreeze.screenshot()
        img2 = np.array(img)
    else:
        img2 = cv2.imread(src_path)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)


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

        print(x_of_point1_of_transform_image, y_of_point1_of_transform_image)
        print(x_of_point3_of_transform_image, y_of_point3_of_transform_image)

        x = (x_of_point3_of_transform_image + x_of_point1_of_transform_image) / 2
        y = (y_of_point3_of_transform_image + y_of_point1_of_transform_image) / 2
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        cv2.circle(img2, (int(x), int(y)), 20, (2, 30, 200), 6)
        cv2.imshow('image', img2)

        cv2.waitKey(0)
        return x, y
    else:
        tkinter.messagebox.askokcancel(message='no match')




root = tkinter.Tk("Tools")  # 通常习惯将这个变量名设置为root或者window

# 进入消息循环

OptionList = [
"SIFT",
"BRISK",
"ORB",
]
variable = tkinter.StringVar(root)
variable.set(OptionList[0])
opt = tkinter.OptionMenu(root, variable, *OptionList)
opt.config(width=5, font=('Helvetica', 12))
label = tkinter.Label(root, text="algorithms:",font = 12)


OptionList2 = [
"0.1",
"0.2",
"0.3",
"0.4",
"0.5",
"0.6",
"0.7",
"0.8",
"0.9",
"1.0",
]
variable2 = tkinter.StringVar(root)
variable2.set(OptionList2[6])
opt2 = tkinter.OptionMenu(root, variable2, *OptionList2)
opt2.config(width=5, font=('Helvetica', 12))
label2 = tkinter.Label(root, text="distance:",font = 12)

bt_open = tkinter.Button(root, command=openfile, text='open src pic', height=2, width=12, activebackground='red', font=9)
bt2_open = tkinter.Button(root, command=openfile2, text='open part pic', height=2, width=13, activebackground='red', font=9)

bt_recognition = tkinter.Button(root, command=recognition, text='recognize', height=2, width=10, activebackground='red',font=9)

bt_open.grid(row=0, column=0)
bt2_open.grid(row=0, column=1)
bt_recognition.grid(row=0, column=3)

label.grid(row=1, column=0)
opt.grid(row=1, column=1)
label2.grid(row=2, column=0)
opt2.grid(row=2, column=1)

root.geometry("350x150+700+300")
root.mainloop()
