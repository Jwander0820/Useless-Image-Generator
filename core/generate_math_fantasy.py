import cv2
import random
import glob
from utils.gif_tools import GifTools
from utils.move_text_by_vector import MoveTextByVector
from utils.generator_data import GenerateRandomParam


class GenerateMathFantasyGif:
    @staticmethod
    def math_fantasy(img_shape=(1280, 720), gif_sec=3):
        """
        數學幻想(?)；可以調整的變數
        1. 在database/equation資料夾下新增新的圖片
        2. init_size貼圖的初始大小，需與圖像尺寸作連動，調整到較佳的參數
        3. resize_refresh每幀間貼圖的縮放比例
        4. rt_random_location_vector 可以到內部修改向量的清單，改變移動速度(較深層)
        :param img_shape: 輸出的GIF圖像大小
        :param gif_sec:生成GIF的秒數
        :return:
        """
        width, height = img_shape
        gif_img_shape = (height, width, 3)
        gif_list = GifTools.generate_frame(gif_img_shape, frame=60, gif_sec=gif_sec, background=(255, 255, 255))  # 生成gif底圖

        fold_path = r"./database/equation\*.*"  # 提取指定資料夾的圖片  # 主程式要調用時請用這行
        # fold_path = r"../database/equation\*.*"  # 提取指定資料夾的圖片  # generate_math_fantasy要用時調用這行!!!
        equation_img_path = glob.glob(fold_path)
        random.shuffle(equation_img_path)  # 清單混洗
        equation_img_list = []
        location_list = []
        vector_list = []
        # 初始參數設定
        for i in range(len(equation_img_path)):
            # 建議匯入的圖片需要二值化，避免疊圖時產生雜訊
            img = cv2.imread(equation_img_path[i], cv2.IMREAD_COLOR)
            _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            # 生成隨機座標和隨機向量
            location, vector = GenerateRandomParam.rt_random_location_vector(img_shape=img_shape)
            equation_img_list.append(img)
            location_list.append(location)
            vector_list.append(vector)

        new_gif_list = []
        resize_refresh = 0
        for frame in gif_list:  # 在每幀間繪圖
            for i in range(len(equation_img_list)):
                # 圖片清單內 結合隨機座標和向量做繪圖
                frame, location_list[i] = MoveTextByVector.draw_img_in_frame(
                    img_shape, location_list[i], vector_list[i], frame, equation_img_list[i],
                    init_size=0.1, resize_refresh=resize_refresh)
            resize_refresh += 0.002
            # 黑白顛倒取反色
            _, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV)
            new_gif_list.append(frame)
        return new_gif_list


if __name__ == "__main__":
    # Done
    _gif_list = GenerateMathFantasyGif.math_fantasy(img_shape=(1000, 1000))
    GifTools.show_gif(_gif_list, frame_rate=60)
