import cv2
import numpy as np
import random
from utils.img_tools import ImgTools
from utils.generator_data import *


class GenerateDigitalMap:
    @staticmethod
    def random_number_map(img_shape=(1280, 720), numbers_of_numbers=1000, save_gif_name=None):
        """
        生成隨機位置的隨機數字圖，黑底白數字
        :param img_shape:圖像尺寸大小 預設為(1280,720)
        :param numbers_of_numbers:生成多少個隨機數字
        :param save_gif_name:儲存的檔案名稱
        :return:
        """
        weight, height = img_shape
        img_shape = (height, weight, 3)
        text_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        gif_list = []
        for frame in range(30):
            mask = np.full(img_shape, (0, 0, 0), dtype=np.uint8)  # 生成蒙版
            location_list = []
            for i in range(numbers_of_numbers):  # 隨機填入1000(default)個數字
                # location = GenerateRandomLocation.generate_range_random_num(weight, height)  # 全隨機生成寬高區間內的座標
                location = GenerateRandomLocation.generate_same_range_random_num(
                    weight, height, step=25)
                if location not in location_list:   # 若座標沒有重複，加入清單，並繪製隨機數字於圖像上
                    location_list.append(location)
                    cv2.putText(mask, random.choice(text_list), location, cv2.FONT_HERSHEY_DUPLEX,
                                1, (255, 255, 255), 2, cv2.LINE_AA)
            gif_list.append(mask)
        ImgTools.show_gif(gif_list, frame_rate=10)
        if save_gif_name:
            ImgTools.cv2_img_list_save_gif(gif_list, save_gif_name)

    @staticmethod
    def full_random_number_map(img_shape=(1280, 720), word_distance=25, save_gif_name=None):
        """
        生成填滿區塊的隨機數字圖，黑底白數字。數字大小倍率為1粗度為2的建議步伐為25，步伐越小填充的數字越密，計算時間越長
        :param img_shape:圖像尺寸大小 預設為(1280,720)
        :param word_distance: 文字間隔
        :param save_gif_name:儲存的檔案名稱
        :return:
        """
        weight, height = img_shape
        img_shape = (height, weight, 3)
        text_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        gif_list = []
        for frame in range(30):
            mask = np.full(img_shape, (0, 0, 0), dtype=np.uint8)  # 生成蒙版
            for i in range(0, weight+word_distance, word_distance):
                for j in range(0, height+word_distance, word_distance):
                    location = (i, j)
                    cv2.putText(mask, random.choice(text_list), location, cv2.FONT_HERSHEY_DUPLEX,
                                1, (255, 255, 255), 2, cv2.LINE_AA)
            gif_list.append(mask)
        ImgTools.show_gif(gif_list, frame_rate=10)
        if save_gif_name:
            ImgTools.cv2_img_list_save_gif(gif_list, save_gif_name)

    @staticmethod
    def y_flow_random_map(img_shape=(1280, 720), location_x=100, move_step=10, word_distance=25, choose_num=7):
        weight, height = img_shape
        img_shape = (height, weight, 3)
        text_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        output_list = MoveText.rt_random_list(text_list, choose_num)
        output_list1 = MoveText.rt_random_list(text_list, 10)
        output_list2 = MoveText.rt_random_list(text_list, 15)

        gif_list = MoveText.generate_frame(img_shape, frame=60, gif_sec=10)
        n = 0  # 迴圈計數器，若字串超過界線，回到起點重新跑
        n1 = 0
        n2 = 0
        for i in range(len(gif_list)):
            mask = gif_list[i]
            move = word_distance * (-choose_num) * (n + 1) + move_step * i - (height * n)
            if move > height:
                n += 1
            MoveText.y_flow(mask, output_list, move, word_distance, location_x)

            mask = gif_list[i]
            move = word_distance * (-10) * (n1 + 1) + 20 * i - (height * n1)
            if move > height:
                n1 += 1
            MoveText.y_flow(mask, output_list1, move, word_distance, 500)

            mask = gif_list[i]
            move = word_distance * (-15) * (n2 + 1) + 25 * i - (height * n2)
            if move > height:
                n2 += 1
            MoveText.y_flow(mask, output_list2, move, word_distance, 1000)

        ImgTools.show_gif(gif_list, frame_rate=60)

        # if save_gif_name:
        #     ImgTools.cv2_img_list_save_gif(gif_list, save_gif_name)

    @staticmethod
    def y_element(gif_list, img_shape=(1280, 720), location_x=100, move_step=10, word_distance=25, choose_num=7):
        weight, height = img_shape
        text_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        output_list = MoveText.rt_random_list(text_list, choose_num)
        n = 0  # 迴圈計數器，若字串超過界線，回到起點重新跑
        for i in range(len(gif_list)):
            mask = gif_list[i]
            move = word_distance * (-choose_num) * (n + 1) + move_step * i - (height * n)
            if move > height:
                n += 1
            MoveText.y_flow(mask, output_list, move, word_distance, location_x)
        return gif_list

    @staticmethod
    def main(img_shape=(1280, 720)):
        weight, height = img_shape
        gif_img_shape = (height, weight, 3)
        gif_list = MoveText.generate_frame(gif_img_shape, frame=60, gif_sec=10)

        # 資料規範
        location_x = random.randrange(0, weight, 25)  # x座標 影響文字從何處移動
        move_step = random.randint(5, 30)  # 步伐 影響字串移動速度
        choose_num = random.randint(5, 20)  # 選取的字元數
        for i in range(10):  # 現在的寫法是 傳遞整個圖像清單，所以是一個人畫完後換另一個人畫，不是全部一起畫，效能有差，可以優化
            gif_list = GenerateDigitalMap.y_element(gif_list, img_shape=img_shape,
                                                    location_x=random.randrange(0, weight, 25),
                                                    move_step=random.randint(5, 30), word_distance=25,
                                                    choose_num=random.randint(5, 20))
        ImgTools.show_gif(gif_list, frame_rate=60)


if __name__ == '__main__':
    # example_shape = (500, 500)
    # Done
    # GenerateDigitalMap.random_number_map(example_shape)
    # GenerateDigitalMap.full_random_number_map(example_shape)

    # Develop
    # GenerateDigitalMap.y_flow_random_map()
    GenerateDigitalMap.main()
