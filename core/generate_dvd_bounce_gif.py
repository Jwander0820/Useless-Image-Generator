import cv2
import random
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
            location, vector = MoveTextByVector.vector_setting(img_shape, start_point=location, vector=vector)
            color = MoveTextByVector.color_setting(color, vector, old_vector)  # 若兩幀間向量不同，隨機骰新的顏色
            cv2.putText(frame, "DVD", location, cv2.FONT_HERSHEY_DUPLEX,
                        1, color, 1, cv2.LINE_AA)
        return gif_list


if __name__ == "__main__":
    _gif_list = GenerateDVDBounceGif.dvd_bounce_by_random_color(img_shape=(300, 300))
    GifTools.show_gif(_gif_list, frame_rate=100)
