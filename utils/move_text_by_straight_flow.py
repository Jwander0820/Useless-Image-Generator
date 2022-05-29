import random
import cv2
from utils.generator_data import GenerateRandomParam
from utils.gif_tools import GifTools


class MoveText:
    @staticmethod
    def generate_y_flow_element_param(img_shape, gif_list, text_list):
        """
        生成y方向移動字串的參數
        :param img_shape: 圖像大小(主要需要取用最大寬度，來決定x座標區間)
        :param gif_list: 幀數(所有張數)(主要用於取樣start_frame起始幀)
        :param text_list: 從該清單內隨機挑選資料
        :return:element_param字串參數； output_string字串資料(清單)
        """
        # 資料規範
        # start_frame   起始幀；建議值，計算所有張數前5分之1，然後 0~n 隨機取樣，ex. 1s60幀，10秒共600幀，取0~120隨機數，表示從該幀開始
        # repeat_time   字串重複的次數；預設為0不改變，用於計算字串到底後+1，將總距離減去(高度*repeat_time)
        # location_x    x座標；影響文字從何處移動(由上往下)
        # move_step     步伐；影響字串移動速度，每幀移動多少pixel，建議值為5~15
        # choose_num    選取的字元數；隨機選多少資料做為要寫入的字串，建議值為5~20，字串太長會跑不完(當然這也算是一種效果，可以改設定)
        # word_size     字體大小；單位字體大小，在更內部的參數會以該參數決定文字粗度(round)，決定文字間隔int(25 * word_size))
        # 基礎文字間隔係數為25 (文字大小=1，建議間隔25pixel)
        width, height = img_shape

        start_frame = random.randrange(0, len(gif_list)//5, 1)
        repeat_time = 0
        location_x = random.randrange(0, width, 10)
        move_step = random.randint(5, 15)
        choose_num = random.randint(5, 20)
        word_size = random.randint(8, 25) * 0.1

        height = height
        element_param = [start_frame, repeat_time, location_x, move_step, choose_num, word_size, height]

        output_string = GenerateRandomParam.rt_random_list(text_list, choose_num)  # 生成要寫入的字串，從清單中隨機挑出指定數量

        return element_param, output_string

    @staticmethod
    def x_flow(img, output_string, move, location_y, word_size):
        """
        x方向的移動，須配合迴圈輸入圖片，連續圖片的組合才有"移動"的視覺效果
        :param img: 要繪製在上面的原圖
        :param output_string:要繪製的清單
        :param move:繪製的起點座標
        :param location_y:固定的y座標
        :param word_size:文字大小，建議值為0.5~3，每個文字的間隔與字體大小相關，係數為25*size
        :return:繪製完的圖片
        """
        for i in range(len(output_string)):
            # 每次繪製一張圖片，循序讀取清單，依序填入，並每次位移i個像素。
            cv2.putText(img, output_string[i], (move + i * int(25 * word_size), location_y), cv2.FONT_HERSHEY_DUPLEX,
                        word_size, (255, 255, 255), round(word_size), cv2.LINE_AA)
        return img

    @staticmethod
    def x_flow_random_number(img_shape=(1280, 720), location_y=100, move_step=10, word_size=1, choose_num=7):
        """
        x方向隨機字串動圖示範(較原始的版本，僅供參考流程用)
        :param img_shape: 圖像尺寸大小
        :param location_y:固定的y座標
        :param move_step:字串每次移動步伐
        :param word_size:文字大小，建議值為0.5~3，每個文字的間隔與字體大小相關，係數為25*size
        :param choose_num:隨機挑選清單內多少個資料
        :return:
        """
        width, height = img_shape
        gif_img_shape = (height, width, 3)
        text_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        output_string = GenerateRandomParam.rt_random_list(text_list, choose_num)  # 隨機挑選多少資料

        gif_list = GifTools.generate_frame(gif_img_shape, frame=60, gif_sec=5)  # 生成多少張資料
        n = 0  # 迴圈計數器，若字串超過界線，回到起點重新跑
        word_size = word_size
        for i in range(len(gif_list)):
            mask = gif_list[i]
            # word_distance*(-choose_num) 為起始座標；move_step*i 為每幀移動步伐；
            # n為計數用，若move長度超過寬度，則減去一個圖像寬度，且起點多後退一步，這樣就能讓字串從起點再跑一次
            move = int(word_size * 25) * (-choose_num) * (n + 1) + move_step * i - (width * n)
            if move > width:  # 長度超過寬度，計數器+1
                n += 1
            MoveText.x_flow(mask, output_string, move, location_y, word_size)

        # 原始概念，供參考；move為起點座標，10是移動步伐
        # 文字間隔(word_distance)*字數(num)*(-1)，表示起始位置往前推一個字串長度
        # for move in range(word_distance*(-choose_num), width, move_step):
        #     mask = np.full(img_shape, (0, 0, 0), dtype=np.uint8)  # 生成蒙版
        #     MoveText.x_flow(mask, output_string, move, word_distance, location_y)
        #     gif_list.append(mask)

        GifTools.show_gif(gif_list, frame_rate=60)

    @staticmethod
    def y_flow(img, output_string, move, location_x, word_size):
        """
        y方向的移動，須配合迴圈輸入圖片，連續圖片的組合才有"移動"的視覺效果
        :param img: 要繪製在上面的原圖
        :param output_string:要繪製的清單
        :param move:繪製的起點座標
        :param location_x:固定的x座標
        :param word_size: 文字大小，建議值為0.5~3，每個文字的間隔與字體大小相關，係數為25*size
        :return:繪製完的圖片
        """
        for i in range(len(output_string)):
            # 每次繪製一張圖片，循序讀取清單，依序填入，並每次位移i個像素。
            if i == (len(output_string)-1):
                cv2.putText(img, output_string[i], (location_x, move + i * int(25 * word_size)), cv2.FONT_HERSHEY_DUPLEX,
                            word_size, (240, 255, 210), round(word_size), cv2.LINE_AA)
            elif i == (len(output_string)-2):
                cv2.putText(img, output_string[i], (location_x, move + i * int(25 * word_size)), cv2.FONT_HERSHEY_DUPLEX,
                            word_size, (140, 240, 150), round(word_size), cv2.LINE_AA)
            else:
                cv2.putText(img, output_string[i], (location_x, move + i * int(25 * word_size)), cv2.FONT_HERSHEY_DUPLEX,
                            word_size, (63, 200, 60), round(word_size), cv2.LINE_AA)
        return img

    @staticmethod
    def y_flow_random_number(img_shape=(1280, 720)):
        """
        y方向隨機字串動圖示範
        :param img_shape: 圖像尺寸大小
        :return:
        """
        width, height = img_shape
        gif_img_shape = (height, width, 3)
        text_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        gif_list = GifTools.generate_frame(gif_img_shape, frame=60, gif_sec=5)

        element_param, output_string = MoveText.generate_y_flow_element_param(img_shape, gif_list, text_list)
        for i in range(len(gif_list)):  # 循序處理每張底圖
            [start_frame, repeat_time, location_x, move_step, choose_num, word_size, height] = element_param
            mask = gif_list[i]
            move = int(word_size * 25) * (-choose_num) * (repeat_time + 1) + move_step * (i - start_frame) - (
                        height * repeat_time)
            if move > height:
                repeat_time += 1
            mask = MoveText.y_flow(mask, output_string, move, location_x, word_size)
            element_param = [start_frame, repeat_time, location_x, move_step, choose_num, word_size, height]

        GifTools.show_gif(gif_list, frame_rate=60)


if __name__ == '__main__':
    # Done
    # 觀察使用，單字串x,y方向位移
    MoveText.x_flow_random_number()
    MoveText.y_flow_random_number()
