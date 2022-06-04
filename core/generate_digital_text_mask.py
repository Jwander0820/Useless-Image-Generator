import numpy as np
import cv2
from utils.gif_tools import GifTools
from core.generate_digital_map_gif import GenerateDigitalMapGif


class GenerateDigitalTextGif:
    @staticmethod
    def digital_text_mask(img_shape=(1280, 720), few_frame_transform=2):
        """
        數位文字圖像，大文字由隨機不斷變換的小數字構成，亦可以替換成自己的剪影(蒙版)
        :param img_shape: 輸出的GIF圖像大小 預設為(1280,720)
        :param few_frame_transform: 幾幀變換一次數字圖像，預設為2，每幀都會變換，數字越大代表每次變換數字的時間間隔越長
        :return:
        """
        # 提取full_random_number_map做細緻的調參，要獲得較小文字的思路除了調整基礎文字大小以外，也可以將數字寫在大圖上在resize回小圖
        # 如此便可以提升文字密度，並不影響文字像素的畫質
        weight, height = img_shape
        oversampling_img_shape = (weight*3, height*3)  # 超採樣，生成n倍大小的底圖之後在resize回來
        gif_list = GenerateDigitalMapGif.full_random_number_map(oversampling_img_shape, word_distance=25,
                                                                few_frame_transform=few_frame_transform)

        new_gif_list = []
        for frame in gif_list:  # 在每幀間繪圖
            frame = cv2.resize(frame, dsize=None, fx=1/3, fy=1/3)  # resize回指定尺寸
            # 重點，以下為剪影合併運算(蒙版)，mask資料為黑底白字，若要套用其他圖片蒙版，也須按照此概念，想要保留的資訊以"白色"作蒙版
            mask = np.full(frame.shape, 0).astype(np.uint8)  # 生成相同大小的蒙版
            # 此處為測試用文字，自行生成文字時，需要調整位移與縮放才會有較佳的效果，此處亦可以替換成自己的蒙版
            cv2.putText(mask, "test", (5, 190), cv2.FLOODFILL_FIXED_RANGE,
                        5, (255, 255, 255), 15, cv2.LINE_AA)

            frame = frame * mask * 255  # 蒙版疊加處理
            new_gif_list.append(frame)
        return new_gif_list


if __name__ == "__main__":
    _gif_list = GenerateDigitalTextGif.digital_text_mask(img_shape=(300, 300), few_frame_transform=2)
    GifTools.show_gif(_gif_list, frame_rate=30)
