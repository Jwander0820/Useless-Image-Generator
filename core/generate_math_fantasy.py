import cv2
import random
from utils.gif_tools import GifTools
from utils.move_text_by_vector import MoveTextByVector
from utils.img_tools import ImgTools


class GenerateMathFantasyGif:
    @staticmethod
    def math_fantasy(img_shape=(1280, 720), gif_sec=10):
        """
        數學幻想(?)
        :param img_shape: 輸出的GIF圖像大小
        :param gif_sec:生成GIF的秒數
        :return:
        """
        width, height = img_shape
        gif_img_shape = (height, width, 3)
        gif_list = GifTools.generate_frame(gif_img_shape, frame=60, gif_sec=gif_sec, background=(255, 255, 255))  # 生成gif底圖
        # 初始參數設定
        location = (500, 500)
        vector = (random.randint(-10, 10), random.randint(-10, 10))
        img = cv2.imread("../database/math_1+1=2.png", cv2.IMREAD_UNCHANGED)
        new_git_list = []
        for frame in gif_list:  # 在每幀間繪圖
            location, vector = MoveTextByVector.vector_setting(img_shape, start_point=location, vector=vector, bounce_setting=True)
            frame = MoveTextByVector.img_moving(frame, img, location)
            new_git_list.append(frame)
        return new_git_list


if __name__ == "__main__":
    # Develop
    _gif_list = GenerateMathFantasyGif.math_fantasy(img_shape=(1000, 1000))
    GifTools.show_gif(_gif_list, frame_rate=100)
