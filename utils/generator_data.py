import cv2
import numpy as np
import random
from utils.img_tools import ImgTools


class GenerateRandomLocation:
    @staticmethod
    def generate_range_random_num(width, height):
        """
        指定寬高，輸出寬高內隨機座標
        :param width: 圖像寬度
        :param height: 圖像高度
        :return: 隨機座標
        """
        x = random.randint(0, width)
        y = random.randint(0, height)
        location = (x, y)
        return location

    @staticmethod
    def generate_same_range_random_num(width, height, step=25):
        """
        指定寬高和文字間隔，輸出寬高內固定間隔隨機座標
        :param width: 圖像寬度
        :param height: 圖像高度
        :param step: 文字間隔
        :return: 固定間隔下隨機座標
        """
        x = random.randrange(0, width+step, step)
        y = random.randrange(0, height+step, step)
        location = (x, y)
        return location


class MoveText:
    @staticmethod
    def rt_random_list(text_list, choose_num):
        """
        輸入清單內隨機挑選指定數量的資料輸出清單
        :param text_list: 輸入的清單
        :param choose_num: 選擇資料數量
        :return: 輸出的清單(輸入清單內隨機挑選n個組成)
        """
        output_list = []
        for i in range(choose_num):
            tmp_choose = random.choice(text_list)
            output_list.append(tmp_choose)
        return output_list

    @staticmethod
    def generate_frame(img_shape, frame, gif_sec):
        """
        生成gif圖像的單張圖片，指定圖像尺寸大小、幀數、秒數
        :param img_shape: 欲生成的圖像大小
        :param frame: 幀數
        :param gif_sec: 秒數
        :return: 單張圖片清單
        """
        # frame*sec等於gif圖所需的所有張數，後許可使用1 sec. N frame來讀取
        gif_list = []
        for i in range(frame * gif_sec):  # 生成所有幀
            mask = np.full(img_shape, (0, 0, 0), dtype=np.uint8)  # 生成蒙版
            gif_list.append(mask)
        return gif_list

    @staticmethod
    def x_flow(img, output_list, move, word_distance, location_y):
        """
        x方向的移動，須配合迴圈輸入圖片，連續圖片的組合才有"移動"的視覺效果
        :param img: 要繪製在上面的原圖
        :param output_list:要繪製的清單
        :param move:繪製的起點座標
        :param word_distance:每個文字的間隔
        :param location_y:固定的y座標
        :return:繪製完的圖片
        """
        for i in range(len(output_list)):
            # 每次繪製一張圖片，循序讀取清單，依序填入，並每次位移i個像素，
            cv2.putText(img, output_list[i], (move + i * word_distance, location_y), cv2.FONT_HERSHEY_DUPLEX,
                        1, (255, 255, 255), 2, cv2.LINE_AA)
        return img

    @staticmethod
    def y_flow(img, output_list, move, word_distance, location_x):
        """
        y方向的移動，須配合迴圈輸入圖片，連續圖片的組合才有"移動"的視覺效果
        :param img: 要繪製在上面的原圖
        :param output_list:要繪製的清單
        :param move:繪製的起點座標
        :param word_distance:每個文字的間隔
        :param location_x:固定的x座標
        :return:繪製完的圖片
        """
        for i in range(len(output_list)):
            # 每次繪製一張圖片，循序讀取清單，依序填入，並每次位移i個像素，
            cv2.putText(img, output_list[i], (location_x, move + i * word_distance), cv2.FONT_HERSHEY_DUPLEX,
                        1, (30, 167, 52), 2, cv2.LINE_AA)
        return img

    @staticmethod
    def x_flow_random_number(img_shape=(1280, 720), location_y=100, move_step=10, word_distance=25, choose_num=7):
        """
        x方向隨機字串動圖示範
        :param img_shape: 圖像尺寸大小
        :param location_y:固定的y座標
        :param move_step:字串每次移動步伐
        :param word_distance:每個文字的間隔
        :param choose_num:隨機挑選清單內多少個資料
        :return:
        """
        weight, height = img_shape
        img_shape = (height, weight, 3)
        text_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        output_list = MoveText.rt_random_list(text_list, choose_num)

        gif_list = MoveText.generate_frame(img_shape, frame=60, gif_sec=10)
        n = 0  # 迴圈計數器，若字串超過界線，回到起點重新跑
        for i in range(len(gif_list)):
            mask = gif_list[i]
            # word_distance*(-choose_num) 為起始座標；move_step*i 為每幀移動步伐；
            # n為計數用，若move長度超過寬度，則減去一個圖像寬度，且起點多後退一步，這樣就能讓字串從起點再跑一次
            move = word_distance*(-choose_num)*(n+1) + move_step * i - (weight * n)
            if move > weight:  # 長度超過寬度，計數器+1
                n += 1
            MoveText.x_flow(mask, output_list, move, word_distance, location_y)

        # 原始概念，供參考；move為起點座標，10是移動步伐
        # 文字間隔(word_distance)*字數(num)*(-1)，表示起始位置往前推一個字串長度
        # for move in range(word_distance*(-choose_num), weight, move_step):
        #     mask = np.full(img_shape, (0, 0, 0), dtype=np.uint8)  # 生成蒙版
        #     MoveText.x_flow(mask, output_list, move, word_distance, location_y)
        #     gif_list.append(mask)

        ImgTools.show_gif(gif_list, frame_rate=60)

    @staticmethod
    def y_flow_random_number(img_shape=(1280, 720), location_x=100, move_step=10, word_distance=25, choose_num=7):
        """
        x方向隨機字串動圖示範
        :param img_shape: 圖像尺寸大小
        :param location_x:固定的x座標
        :param move_step:字串每次移動步伐
        :param word_distance:每個文字的間隔
        :param choose_num:隨機挑選清單內多少個資料
        :return:
        """
        weight, height = img_shape
        img_shape = (height, weight, 3)
        text_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        output_list = MoveText.rt_random_list(text_list, choose_num)

        gif_list = MoveText.generate_frame(img_shape, frame=60, gif_sec=10)
        n = 0  # 迴圈計數器，若字串超過界線，回到起點重新跑
        for i in range(len(gif_list)):
            mask = gif_list[i]
            move = word_distance * (-choose_num) * (n + 1) + move_step * i - (height * n)
            if move > height:
                n += 1
            MoveText.y_flow(mask, output_list, move, word_distance, location_x)

        ImgTools.show_gif(gif_list, frame_rate=60)


if __name__ == '__main__':
    # Done
    # print(GenerateRandomLocation.generate_same_range_random_num(720, 1280))
    # 觀察使用，單字串x,y方向位移
    MoveText.x_flow_random_number()
    MoveText.y_flow_random_number()

    # Develop
