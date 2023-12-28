import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2
import numpy as np
import keras


class MyWindow():
    def __init__(self, app):

        self.app = app
        self.app.title("车牌定位：矫正和识别软件")
        self.app.geometry("%dx%d-%d-%d" % (992, 550, 200, 200))
        self.px = tk.PhotoImage(width=1, height=1)

        self.label1 = tk.Label(self.app, text="原图：", font=('黑体', 10),
                               image=self.px, compound="c",
                               width=40, height=20, )
        self.label1.place(x=0, y=0)

        self.canvas = tk.Canvas(self.app, width=512, height=512, background="white",
                                highlightbackground="black", highlightthickness=1)
        self.canvas.place(x=40, y=0)

        self.plate_canva1 = tk.Canvas(self.app, width=300, height=80, background="white", highlightbackground="black",
                                      highlightthickness=1)
        self.plate_canva1.place(x=672, y=0)
        self.plate_canva2 = tk.Canvas(self.app, width=300, height=80, background="white", highlightbackground="black",
                                      highlightthickness=1)
        self.plate_canva2.place(x=672, y=160)
        self.plate_canva3 = tk.Canvas(self.app, width=300, height=80, background="white", highlightbackground="black",
                                      highlightthickness=1)
        self.plate_canva3.place(x=672, y=320)

        self.panel_pri1 = tk.Canvas(self.app, width=300, height=50, background="white", highlightbackground="black",
                                    highlightthickness=1)
        self.panel_pri1.place(x=672, y=90)
        self.panel_pri2 = tk.Canvas(self.app, width=300, height=50, background="white", highlightbackground="black",
                                    highlightthickness=1)
        self.panel_pri2.place(x=672, y=250)
        self.panel_pri3 = tk.Canvas(self.app, width=300, height=50, background="white", highlightbackground="black",
                                    highlightthickness=1)
        self.panel_pri3.place(x=672, y=410)

        y = 0
        for i in range(1, 4):
            tk.Label(self.app, text=f"车牌区域{i}:", font=('黑体', 10),
                     image=self.px, compound="c",
                     width=70, height=10).place(x=592, y=y)
            y = y + 90
            tk.Label(self.app, text=f"识别结果{i}:", font=('黑体', 10),
                     image=self.px, compound="c",
                     width=70, height=10).place(x=592, y=y)
            y = y + 70

        texts = ['选择文件', '识别车辆', '清空所有']
        x = 632
        for text in texts:
            tk.Button(self.app, text=text, font=('黑体', 15), image=self.px, compound="c",
                      width=100, height=30, command=lambda b=text: self.on_button_click(b)).place(x=x, y=510)
            x += 110

        self.canvas_image = None
        self.image_path = ""
        self.dic_img_tk1 = None
        self.dic_img_tk2 = None
        self.dic_img_tk3 = None

    # 识别车牌
    def recognize_panel(self, image):
        image = image.reshape(1, 80, 240, 3)
        characters = ["京", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "皖", "闽", "赣", "鲁",
                      "豫",
                      "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "0", "1", "2",
                      "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
                      "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        result = cnn.predict(image)
        panel_str = ""
        for item in result:
            index = np.argmax(item)
            panel_str = panel_str + characters[index]
        return panel_str[:2] + "." + panel_str[2:]
    # 清理显示区域
    def detepri(self):
        self.plate_canva1.delete("all")
        self.plate_canva2.delete("all")
        self.plate_canva3.delete("all")
        self.panel_pri1.delete("all")
        self.panel_pri2.delete("all")
        self.panel_pri3.delete("all")
    # 清除所有
    def clear_canvases(self):
        self.canvas.delete("all")
        self.detepri()
        self.canvas_image = None
        self.image_path = ""
        self.dic_img_tk1 = None
        self.dic_img_tk2 = None
        self.dic_img_tk3 = None
    # 展现车牌
    def show(self,panel_result,dic_img_tk,i):
        if i == 0:
            self.panel_pri1.create_text(150, 25, text=panel_result, font=('黑体', 30), fill="black")
            self.plate_canva1.create_image(150, 40, image=dic_img_tk, anchor="center")
            self.dic_img_tk1 = dic_img_tk  # 存储引用
        elif i == 1:
            self.panel_pri2.create_text(150, 25, text=panel_result, font=('黑体', 30), fill="black")
            self.plate_canva2.create_image(150, 40, image=dic_img_tk, anchor="center")
            self.dic_img_tk2 = dic_img_tk  # 存储引用
        else:
            self.panel_pri3.create_text(150, 25, text=panel_result, font=('黑体', 30), fill="black")
            self.plate_canva3.create_image(150, 40, image=dic_img_tk, anchor="center")
            self.dic_img_tk3 = dic_img_tk  # 存储引用

        # 拉伸图片
    def stretch_img(self, contours):
        i = 0
        for cont in contours:
            x, y, w, h = cv2.boundingRect(cont)
            if (w + h) < 10:
                continue
            x0, y0 = x, y
            x1, y1 = x, y + h
            x2, y2 = x + w, y
            x3, y3 = x + w, y + h

            d0, d1, d2, d3 = np.inf, np.inf, np.inf, np.inf
            l0, l1, l2, l3 = (x0, y0), (x1, y1), (x2, y2), (x3, y3)
            for item in cont:
                (current_x, current_y) = item[0]
                dis0 = (current_x - x0) ** 2 + (current_y - y0) ** 2
                dis1 = (current_x - x1) ** 2 + (current_y - y1) ** 2
                dis2 = (current_x - x2) ** 2 + (current_y - y2) ** 2
                dis3 = (current_x - x3) ** 2 + (current_y - y3) ** 2
                if dis0 < d0:
                    d0 = dis0
                    l0 = (current_x, current_y)
                if dis1 < d1:
                    d1 = dis1
                    l1 = (current_x, current_y)
                if dis2 < d2:
                    d2 = dis2
                    l2 = (current_x, current_y)
                if dis3 < d3:
                    d3 = dis3
                    l3 = (current_x, current_y)
            # 用红色线框出车牌区域
            self.canvas.create_line(l0, l2, fill="red", width=2)
            self.canvas.create_line(l2, l3, fill="red", width=2)
            self.canvas.create_line(l3, l1, fill="red", width=2)
            self.canvas.create_line(l1, l0, fill="red", width=2)
            # ------------------ 将车牌区域拉伸放到程序的车牌区域 ------------------
            pts1 = np.float32([l0, l2, l1, l3])
            pts2 = np.float32([
                [0, 0],
                [240, 0],
                [0, 80],
                [240, 80]
            ])
            M = cv2.getPerspectiveTransform(pts1, pts2)
            dic_img = cv2.warpPerspective(self.image, M, (240, 80))
            panel_result = self.recognize_panel(dic_img)
            dic_img = dic_img.astype(np.uint8)
            dic_img = cv2.cvtColor(dic_img, cv2.COLOR_BGR2RGB)
            dic_img = Image.fromarray(dic_img)
            dic_img_tk = ImageTk.PhotoImage(dic_img)
            self.show(panel_result, dic_img_tk, i)
            i = i + 1
    # 处理图片
    def pro_img(self):
        if not self.image_path:
            return
        self.image = cv2.imdecode(np.fromfile(self.image_path, dtype=np.uint8), -1)
        if self.image.shape != (512, 512, 3):
            self.image = cv2.resize(self.image, dsize=(512, 512), interpolation=cv2.INTER_AREA)[:, :, :3]
        self.image = self.image.reshape((1, 512, 512, 3))
        img_mask = unet.predict(self.image)
        img_mask = img_mask.reshape(512, 512, 3)
        img_mask = img_mask / np.max(img_mask) * 255
        img_mask[:, :, 2] = img_mask[:, :, 1] = img_mask[:, :, 0]
        img_mask = np.array(img_mask, dtype=np.uint8)

        try:
            contours, hierarchy = cv2.findContours(img_mask[:, :, 0], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        except:
            ret, contours, hierarchy = cv2.findContours(img_mask[:, :, 0], cv2.RETR_EXTERNAL,
                                                        cv2.CHAIN_APPROX_SIMPLE)

        self.image = self.image.reshape(512, 512, 3)
        self.stretch_img(contours)

    def on_button_click(self, button):
        if button == "选择文件":
            self.canvas.delete("all")
            self.image_path = askopenfilename()
            if self.image_path:
                image = Image.open(self.image_path)
                image = image.resize((512, 512))
                self.img_tk = ImageTk.PhotoImage(image)
                self.canvas.create_image(256, 256, image=self.img_tk, anchor="center")
        elif button == "识别车辆":
            self.detepri()
            self.pro_img()
        else:
            self.clear_canvases()


if __name__ == "__main__":
    unet = keras.models.load_model("unet.h5")
    cnn = keras.models.load_model("cnn.h5")
    app = tk.Tk()
    window = MyWindow(app)
    app.mainloop()
