import os
import random
import cv2
import numpy as np
from PIL import Image
from utils.gif_tools import GifTools
from utils.move_text_by_vector import MoveTextByVector


class GenerateDVDBounceGif:
    @staticmethod
    def dvd_bounce_by_random_color(img_shape=(1280, 720), gif_sec=5):
        """
        DVD反彈碰撞GIF
        :param img_shape: 輸出的GIF圖像大小
        :param gif_sec:生成GIF的秒數
        :return:
        """
        width, height = img_shape
        gif_img_shape = (height, width, 3)
        gif_list = GifTools.generate_frame(gif_img_shape, frame=60, gif_sec=gif_sec)  # 生成gif底圖
        # 初始參數設定
        location = (random.randint(0, width), random.randint(0, height))
        vector = (random.randint(3, 5), random.randint(3, 5))
        color = (200, 255, 250)

        for frame in gif_list:  # 在每幀間繪圖
            old_vector = vector  # 紀錄前一幀的向量，用於處理顏色反轉
            location, vector = MoveTextByVector.vector_setting(frame, start_point=location, vector=vector,
                                                               bounce_setting=True)
            color = MoveTextByVector.color_setting(color, vector, old_vector)  # 若兩幀間向量不同，隨機骰新的顏色
            cv2.putText(frame, "DVD", location, cv2.FONT_HERSHEY_DUPLEX,
                        1, color, 1, cv2.LINE_AA)
        return gif_list

    @staticmethod
    def dvd_bounce_with_img(img_shape=(1280, 720), gif_sec=5, bounce_img_path=None):
        """
        DVD反彈碰撞GIF進階版 - 以圖像來做碰撞 ；vector_setting函數內部可以設定是否要再變換方向時添加隨機向量!
        :param bounce_img_path: 可自訂反彈的圖像，不建議使用彩色圖片，彩色圖片可能會有異常
        :param img_shape: 輸出的GIF圖像大小
        :param gif_sec:生成GIF的秒數
        :return:
        """
        width, height = img_shape
        gif_img_shape = (height, width, 3)
        gif_list = GifTools.generate_frame(gif_img_shape, frame=60, gif_sec=gif_sec,
                                           background=(255, 255, 255))  # 生成gif底圖
        if bounce_img_path and os.path.isfile(bounce_img_path):
            img = Image.open(bounce_img_path)
            img = np.uint8(img)
        else:
            img_path = r"./database/DVD.png"  # 提取指定資料夾的圖片  # 主程式要調用時請用這行
            # img_path = r"../database/DVD.png"  # 提取指定資料夾的圖片  # generate_dvd_bounce_gif要用時調用這行!!!
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        # 初始參數設定
        # 建議匯入的圖片需要二值化，避免疊圖時產生雜訊
        img = cv2.resize(img, dsize=None, fx=0.2, fy=0.2)  # 圖像太大的話要resize到適合的尺寸
        location = (100, 100)  # 若要隨機座標還須做判斷，不能讓初始座標在太右邊or下邊，會導致無法繪圖
        # 生成隨機向量
        vector = (random.randint(2, 4), random.randint(2, 4))
        color = (255, 255, 255)  # 初始顏色

        new_gif_list = []
        for frame in gif_list:  # 在每幀間繪圖
            old_vector = vector  # 紀錄前一幀的向量，用於處理顏色反轉
            location, vector = MoveTextByVector.vector_setting(frame, start_point=location, vector=vector,
                                                               paste_img=img, bounce_setting=True)
            frame = MoveTextByVector.img_moving(frame, img, location)
            color = MoveTextByVector.color_setting(color, vector, old_vector)  # 若兩幀間向量不同，隨機骰新的顏色
            _, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV)
            frame[:, :, 0] = frame[:, :, 0] * color[0] * 255  # 將通道平面與顏色相乘 (類似顏色的蒙版)
            frame[:, :, 1] = frame[:, :, 1] * color[1] * 255
            frame[:, :, 2] = frame[:, :, 2] * color[2] * 255
            new_gif_list.append(frame)
        return new_gif_list


if __name__ == "__main__":
    # Done
    _gif_list = GenerateDVDBounceGif.dvd_bounce_by_random_color(img_shape=(300, 300))
    GifTools.show_gif(_gif_list, frame_rate=100)  # 簡陋版文字示範

    _gif_list = GenerateDVDBounceGif.dvd_bounce_with_img(img_shape=(300, 300))
    GifTools.show_gif(_gif_list, frame_rate=100)  # 碰撞圖片示範，效果較佳
