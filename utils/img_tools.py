import cv2
import os
import numpy as np
from PIL import Image
from PIL import ImageSequence


class ImgTools:

    @staticmethod
    def show_img(img):
        """
        以視窗的形式展現圖片，視窗大小為圖片的一半
        若圖片太大，直接用cv2.imshow會以完整解析度呈現，所以改用下面的nameWindow把圖像放在裡面限制大小
        :param img: 要顯示的圖像
        :return: None
        """
        # 冷知識:在imshow顯示的時候，可以在選定的窗口中做圖片的複製(Ctrl+C)與保存(Ctrl+S)
        cv2.namedWindow("windows", 0)
        # 設定窗口大小，("名稱", x, y) x是寬度 y是高度，此處暫以縮小一半作呈現
        cv2.resizeWindow("windows", int(img.shape[1]), int(img.shape[0]))
        cv2.imshow("windows", img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    @staticmethod
    def show_gif(gif_list, frame_rate=30):
        """
        讀取cv2連續圖片清單，並展示gif圖像，按空白鍵關閉視窗
        :param gif_list:cv2連續圖片清單
        :param frame_rate:幀數，每秒顯示多少張圖片，預設為30幀
        :return: None
        """
        # 將幀數換算成每張圖像間隔時間，公式 = 1秒//幀數 = 1000毫秒//幀數
        interval_sec = 1000 // frame_rate
        loop = True  # 設定 loop 為 True
        while loop:
            for i in gif_list:
                cv2.imshow('show gif press blank key leave windows', i)  # 不斷讀取並顯示串列中的圖片內容
                if cv2.waitKey(interval_sec) == ord(" "):
                    loop = False  # 停止時同時也將 while 迴圈停止
                    break
        cv2.destroyAllWindows()

    @staticmethod
    def read_and_show_gif(path, frame_rate=30):
        """
        讀取gif檔案，並展示gif圖像，按空白鍵關閉視窗
        :param path:gif檔案路徑
        :param frame_rate:幀數，每秒顯示多少張圖片，預設為30幀
        :return:
        """
        interval_sec = 1000//frame_rate
        gif = Image.open(path)
        img_list = []  # 建立儲存影格的空串列
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert('RGBA')  # 轉換成 RGBA
            opencv_img = np.array(frame, dtype=np.uint8)  # 轉換成 numpy 陣列
            opencv_img = cv2.cvtColor(opencv_img, cv2.COLOR_RGBA2BGRA)  # 顏色從 RGBA 轉換為 BGRA
            img_list.append(opencv_img)  # 利用串列儲存該圖片資訊

        loop = True  # 設定 loop 為 True
        while loop:
            for i in img_list:
                cv2.imshow('show gif press blank key leave windows', i)  # 不斷讀取並顯示串列中的圖片內容
                if cv2.waitKey(interval_sec) == ord(" "):
                    loop = False  # 停止時同時也將 while 迴圈停止
                    break
        cv2.destroyAllWindows()

    @staticmethod
    def pil_import_img_trans_cv2(file_path):
        """
        透過PIL匯入圖片並轉換成cv2格式傳出
        :param file_path: 要讀取的圖片路徑
        :return: 回傳cv2形式的圖像資料
        """
        img = Image.open(file_path)  # 使用PIL讀取檔案，避開cv2無法讀取中文路徑的問題
        pil2cv2 = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        return pil2cv2

    @staticmethod
    def cv2_img_list_save_gif(gif_list, save_file_name, interval_sec=150):
        """
        將cv2的圖片清單儲存成gif檔案
        :param gif_list: cv2圖片清單
        :param save_file_name: 儲存檔名
        :param interval_sec: 每張圖間格秒數
        :return: 回傳檔案路徑 final_path
        """
        folder_dir = "./data"  # 儲存的資料夾
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
        final_path = os.path.join(folder_dir, save_file_name)  # 最終檔案儲存路徑

        output = []
        for img in gif_list:
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # 轉換成 PIL 格式(同時BGR轉RGB讓顯色與cv2呈現出來相同)
            output.append(img)  # 加入 output
        output[0].save(final_path, save_all=True, append_images=output[1:], loop=0, duration=interval_sec, disposal=0)
        return final_path
