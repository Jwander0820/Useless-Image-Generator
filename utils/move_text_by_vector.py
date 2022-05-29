import random


class MoveTextByVector:
    @staticmethod
    def vector_setting(img_shape, start_point=(0, 0), vector=(1, 2)):
        """
        設定物件移動向量
        :param img_shape: 圖片尺寸大小(用於計算邊界相關處理)
        :param start_point: 物件每幀起始點
        :param vector: 移動向量
        :return: 新的座標以及向量
        """
        # 解析變數
        # width, height = img_shape
        start_x, start_y = start_point
        vector_x, vector_y = vector

        end_x = start_x + vector_x  # x座標+x向量=x新座標
        end_y = start_y + vector_y  # y座標+y向量=y新座標
        location = (end_x, end_y)
        # 回傳新向量，若物件的座標超出框線將其向量反轉，若不執行下面的操作，物件會直接飛出邊界(不同的效果)
        new_vector = MoveTextByVector.bounce_setting(img_shape, location, vector)
        return location, new_vector

    @staticmethod
    def bounce_setting(img_shape, location, vector):
        """
        反彈設定(僅改變方向)
        :param img_shape: 圖片尺寸大小(用於計算邊界相關處理)
        :param location: 物件座標
        :param vector: 移動向量
        :return:
        """
        # 解析變數
        width, height = img_shape
        end_x, end_y = location
        vector_x, vector_y = vector
        # 若碰到邊界，將向量反轉
        if end_x > width and end_y > height:
            vector = (-vector_x, -vector_y)  # 若x,y越過 右下角界線
        elif end_x > width and end_y < 0:
            vector = (-vector_x, -vector_y)  # 若x,y越過 右上角界線
        elif end_x < 0 and end_y < 0:
            vector = (-vector_x, -vector_y)  # 若x,y越過 左上角界線
        elif end_x < 0 and end_y > height:
            vector = (-vector_x, -vector_y)  # 若x,y越過 左下角界線
        elif end_x > width:
            vector = (-vector_x, vector_y)  # 若x越過 右邊界線
        elif end_x < 0:
            vector = (-vector_x, vector_y)  # 若x越過 左邊界線
        elif end_y > height:
            vector = (vector_x, -vector_y)  # 若y越過 下邊界線
        elif end_y < 0:
            vector = (vector_x, -vector_y)  # 若y越過 上邊界線
        return vector

    @staticmethod
    def color_setting(color, new_vector, old_vector):
        """
        回傳新顏色，若物件的向量有反轉過，將其顏色隨機改變
        :param color: 原始顏色
        :param new_vector: 計算出來新的向量
        :param old_vector: 前一幀的向量
        :return: 若向量有反轉，回傳新的隨機顏色，若向量沒有反轉，回傳原始顏色
        """
        if new_vector != old_vector:
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            color = (blue, green, red)  # cv2色彩呈現為BGR形式
            return color
        else:
            return color
