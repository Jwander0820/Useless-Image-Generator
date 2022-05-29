import cv2
import numpy as np
from PIL import Image


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
    def pil_import_img_trans_cv2(file_path):
        """
        透過PIL匯入圖片並轉換成cv2格式傳出
        :param file_path: 要讀取的圖片路徑
        :return: 回傳cv2形式的圖像資料
        """
        img = Image.open(file_path)  # 使用PIL讀取檔案，避開cv2無法讀取中文路徑的問題
        pil2cv2 = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        return pil2cv2
