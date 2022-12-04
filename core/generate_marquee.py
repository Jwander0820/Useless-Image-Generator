# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from utils.gif_tools import GifTools
from utils.move_text_by_straight_flow import MoveText
from utils.generator_data import GenerateRandomParam


class GenerateMarquee:
    @staticmethod
    def text_flow(text, **kwargs):
        """
        橫向跑馬燈動圖
        :param text: 文字內容
        :return:
        """
        # 可以調整的設定
        kwargs.setdefault('color', (255, 255, 255))  # 文字顏色
        kwargs.setdefault('background', (0, 0, 0))  # 底圖顏色
        kwargs.setdefault('word_size', 50)  # 文字大小，建議值為0.5~3，每個文字的間隔與字體大小相關，係數為25*size
        kwargs.setdefault('move_step', 10)  # 字串每次移動步伐，影響的是移動的速度
        kwargs.setdefault('direction', "right2left")  # 字串由右向左(right2left)；由左向右(left2right)
        # 不太需要調整的設定
        kwargs.setdefault('img_shape', (720, kwargs["word_size"] + kwargs["word_size"] // 2))  # 圖像尺寸大小，高度部分設定為1.5倍字大小
        kwargs.setdefault('location_y', 0)  # 固定的y座標，想要設定不同的y位置時可以調整該設定
        kwargs.setdefault('gif_sec', 30)  # 生成的GIF總時長(文字到底時就會自動從頭開始，所以實際GIF秒數不會這麼長，若文字太長的話這邊秒數需要增加)
        kwargs.setdefault('reverse', True)  # 反轉字串順序，只有當direction為left2right才有效

        # 基礎設定
        width, height = kwargs["img_shape"]
        gif_img_shape = (height, width, 3)
        # 生成GIF底圖
        gif_list = GifTools.generate_frame(gif_img_shape, frame=60, gif_sec=kwargs["gif_sec"],
                                           background=kwargs["background"])
        n = 0  # 迴圈計數器，若字串超過界線，回到起點重新跑
        if kwargs["direction"] == "left2right" and kwargs["reverse"]:  # 若跑馬燈設為由左至右的話，反轉字串排序
            text = text[::-1]

        # 文字移動處理
        for i in range(len(gif_list)):
            if n == 1:  # n = 1 表示跑馬燈已經到底了，刪除後續gif的圖片，以實現迴圈滾動的效果
                del gif_list[i:len(gif_list)]
                break
            mask = gif_list[i]  # 取出第i幀的圖片
            move = 0  # 初始位移

            if kwargs["direction"] == "left2right":  # 跑馬燈從左到右
                # word_size*-len(text) 為字體大小*字數，目的為讓起始位置從最右邊開始
                # move_step*i 為每幀移動步伐
                # 計算要移動到哪個點
                move = kwargs["word_size"] * -len(text) + kwargs["move_step"] * i
                if move > width:  # 長度超過寬度，計數器+1
                    n += 1
            elif kwargs["direction"] == "right2left":  # 跑馬燈從右到左
                # width；讓起始位置從最右邊開始
                # -move_step*i；每幀移動步伐，右到左需要將步伐設置為負的
                # -word_size * len(text)；字體大小 * 字數，代表最左邊的位置需要小於該值才會終止，實現的效果為最後一個文字跑完才會重置
                # 計算要移動到哪個點
                move = width - kwargs["move_step"] * i
                if move < -kwargs["word_size"] * len(text):  # 長度超過寬度，計數器+1
                    n += 1
            img = GenerateMarquee.x_flow_cht(mask, text, move, **kwargs)
            gif_list[i] = img
        return gif_list

    @staticmethod
    def x_flow_cht(img, text, move, **kwargs):
        """
        x方向的移動，須配合迴圈輸入圖片，連續圖片的組合才有"移動"的視覺效果(可以輸入中文)
        :param img: 要繪製在上面的原圖
        :param text:要繪製的清單
        :param move:繪製的起點座標
        :return:繪製完的圖片
        """
        if len(img.shape) == 2:  # 檢測圖像尺寸，若為灰階圖形式，則需要轉換成RGB形式
            img2pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))
        else:
            img2pil = Image.fromarray(img)
        draw_pil = ImageDraw.Draw(img2pil)
        font_text = ImageFont.truetype("font/msjhbd.ttc", kwargs["word_size"], encoding="utf-8")  # 微軟正黑粗體

        pos = (move + int(kwargs["word_size"]), kwargs["location_y"])
        draw_pil.text(pos, text, kwargs["color"], font=font_text)
        img = cv2.cvtColor(np.asarray(img2pil), cv2.COLOR_RGB2BGR)
        return img

    @staticmethod
    def cv2_can_not_show_chinese():
        """
        範例說明；因為cv2無法透過函數顯示中文，因此需要透過PIL轉出中文再轉回cv2格式
        :return:
        """
        img2pil = np.uint8(np.zeros((512, 512)))
        if isinstance(img2pil, np.ndarray):  # 判斷是否 OpenCV 圖片類型
            img2pil = Image.fromarray(cv2.cvtColor(img2pil, cv2.COLOR_GRAY2RGB))
        text = "OpenCV, 中文顯示測試"
        pos = (50, 20)  # (left, top)，字符串左上角坐标
        color = (255, 255, 255)  # 字体颜色
        text_size = 40
        draw_pil = ImageDraw.Draw(img2pil)
        font_text = ImageFont.truetype("font/msjhbd.ttc", text_size, encoding="utf-8")  # 微軟正黑粗體
        draw_pil.text(pos, text, color, font=font_text)
        img_put_text = cv2.cvtColor(np.asarray(img2pil), cv2.COLOR_RGB2BGR)

        cv2.imshow("img_put_text", img_put_text)  # 显示叠加图像 imgAdd
        cv2.waitKey(0)  # 等待按键命令


if __name__ == '__main__':
    # GenerateMarquee.cv2_can_not_show_chinese()
    _test_text = "這是一串測試用的中文字，This is a English text test, 123"
    _gif_list = GenerateMarquee.text_flow(_test_text,
                                          color=(255, 50, 50),
                                          background=(0, 0, 0),
                                          word_size=100,
                                          move_step=10,
                                          direction="right2left")
    GifTools.show_gif(_gif_list, frame_rate=60)
