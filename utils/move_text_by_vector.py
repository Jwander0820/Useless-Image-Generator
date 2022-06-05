import random
import cv2


class MoveTextByVector:
    @staticmethod
    def vector_setting(frame, start_point=(0, 0), vector=(1, 2), paste_img=(0, 0, 0),
                       bounce_setting=False, random_factor=False):
        """
        設定物件移動向量，函數內部可以設定是否要再變換方向時添加隨機向量!
        :param frame: 圖片尺寸大小(用於計算邊界相關處理)
        :param start_point: 物件每幀起始點
        :param vector: 移動向量
        :param paste_img:欲貼上的圖片(需與bounce_setting連動)
        :param bounce_setting:設定物件是否反彈(只看左上座標，不看貼圖邊界)
        :param random_factor: 隨機向量因子；碰到四邊界時向量反轉，並在沒有反轉的向量添加隨機因子(讓每次碰撞時可能不是全反彈)
        :return: 新的座標以及向量
        """
        # 解析變數
        # frame_height, frame_width, frame_channel = frame.shape
        start_x, start_y = start_point
        vector_x, vector_y = vector

        new_start_x = start_x + vector_x  # x座標+x向量=x新座標
        new_start_y = start_y + vector_y  # y座標+y向量=y新座標
        location = (new_start_x, new_start_y)
        if bounce_setting:
            # 回傳新向量，若物件的座標超出框線將其向量反轉，若不執行下面的操作，物件會直接飛出邊界(不同的效果)
            new_vector = MoveTextByVector.bounce_setting(frame, paste_img, location, vector, random_factor=random_factor)
            return location, new_vector
        else:
            return location, vector

    @staticmethod
    def bounce_setting(frame, paste_img, location, vector, random_factor=False):
        """
        反彈設定(僅改變方向)
        :param frame: 圖片尺寸大小(用於計算邊界相關處理)
        :param paste_img:欲貼上的圖片(需與bounce_setting連動)
        :param location: 物件座標
        :param vector: 移動向量
        :param random_factor: 隨機向量因子；碰到四邊界時向量反轉，並在沒有反轉的向量添加隨機因子(讓每次碰撞時可能不是全反彈)
        :return:
        """
        # 解析變數
        frame_height, frame_width, frame_channel = frame.shape
        try:
            img_height, img_width, img_channel = paste_img.shape  # 貼圖的寬高通道數，先嘗試解析，解析失敗則使用(0,0,0)
        except AttributeError:  # AttributeError: 'tuple' object has no attribute 'shape'
            img_height, img_width, img_channel = (0, 0, 0)  # 預設為tuple型態，不能讀取.shape形狀，因此令為0，如此不影響不輸入圖片時的函數

        new_start_x, new_start_y = location  # 提取初始左上座標
        new_end_x = new_start_x + img_width  # 計算貼圖的右下座標x
        new_end_y = new_start_y + img_height  # 計算貼圖的右下座標y

        vector_x, vector_y = vector
        new_vector = vector  # 複製一份原始向量，用於後續若有變換向量時的隨機因子計算
        random_vector_factor = 0  # default=0
        if random_factor:  # 碰到四邊界時向量反轉，並在沒有反轉的向量添加隨機因子(每次碰撞時可能不是全反彈)
            random_vector_factor = random.randint(-1, 1)
        # 若碰到邊界，將向量反轉
        if new_end_x > frame_width and new_end_y > frame_height:
            new_vector = (-vector_x, -vector_y)  # 若paste_img右下角碰到 右下角界線
        elif new_end_x > frame_width and new_start_y < 0:
            new_vector = (-vector_x, -vector_y)  # 若paste_img右上角碰到 右上角界線
        elif new_start_x < 0 and new_start_y < 0:
            new_vector = (-vector_x, -vector_y)  # 若paste_img左上角碰到 左上角界線
        elif new_start_x < 0 and new_end_y > frame_height:
            new_vector = (-vector_x, -vector_y)  # 若paste_img左下角碰到 左下角界線
        elif new_end_x > frame_width:
            new_vector = (-vector_x, vector_y + random_vector_factor)  # 若paste_img右邊界碰到 右邊界線
        elif new_start_x < 0:
            new_vector = (-vector_x, vector_y + random_vector_factor)  # 若paste_img左邊界碰到 左邊界線
        elif new_end_y > frame_height:
            new_vector = (vector_x + random_vector_factor, -vector_y)  # 若paste_img下邊界碰到 下邊界線
        elif new_start_y < 0:
            new_vector = (vector_x + random_vector_factor, -vector_y)  # 若paste_img上邊界碰到 上邊界線

        return new_vector

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

    @staticmethod
    def draw_img_in_frame(frame, location, vector, img, init_size=0.1, resize_refresh=0):
        """
        集成的物件，輸出的GIF圖像大小，每次更新的座標，固定向量，底圖，欲貼上的圖
        :param frame: 底圖
        :param location: 每次更新的座標
        :param vector: 固定向量
        :param img: 欲貼上的圖
        :param init_size: 貼圖初始大小
        :param resize_refresh: 更新resize大小的參數
        :return: frame更新後的底圖 location更新後的座標
        """
        location, vector = MoveTextByVector.vector_setting(frame, start_point=location, vector=vector)
        whether_to_draw = MoveTextByVector.according_location_decide_draw(frame, img, location)
        if whether_to_draw:
            img_resize = cv2.resize(img, dsize=None, fx=init_size + resize_refresh, fy=init_size + resize_refresh)
            frame = MoveTextByVector.img_moving(frame, img_resize, location)
        return frame, location

    @staticmethod
    def img_moving(frame, img, location):
        """
        繪製位移縮放過後的圖像在frame上
        :param frame:底圖
        :param img: 欲貼上的圖片
        :param location: 貼在底圖的左上座標
        :return:frame 貼完圖的結果
        """
        # frame_height, frame_width, frame_channel = frame.shape
        height, width, channel = img.shape
        img_loc_x_start, img_loc_y_start = location

        img_loc_x_end = img_loc_x_start + width
        img_loc_y_end = img_loc_y_start + height

        left_up_pint = (img_loc_x_start, img_loc_y_start)  # 繪製於底圖的左上座標
        right_down_point = (img_loc_x_end, img_loc_y_end)  # 繪製於底圖的右下座標
        # 回傳檢測是否超出框線並將貼圖繪製於frame上
        frame = MoveTextByVector.detect_frame_line(frame, img, left_up_pint, right_down_point)
        return frame

    @staticmethod
    def according_location_decide_draw(frame, img, location):
        """
        根據左上角座標和右下角座標決定是否貼圖在frame上 (避免不必要的運算，因為少了檢測會讓後續沒有意義的貼圖繼續計算)
        核心概念為；判斷左上座標是否超出右和下邊界，判斷右下座標是否超出左和上邊界。超出代表貼圖範圍完全超出底圖範圍了，後續沒有計算的意義
        :param frame:底圖
        :param img: 欲貼上的圖片
        :param location: 貼在底圖的左上座
        :return: True or False
        """
        frame_height, frame_width, frame_channel = frame.shape
        height, width, channel = img.shape
        img_loc_x_start, img_loc_y_start = location

        img_loc_x_end = img_loc_x_start + width
        img_loc_y_end = img_loc_y_start + height

        whether_to_draw = True
        if img_loc_x_start > frame_width:  # 判斷左上座標是否超出右和下邊界
            whether_to_draw = False
        elif img_loc_y_start > frame_height:
            whether_to_draw = False
        elif img_loc_x_end < 0:  # 判斷右下座標是否超出左和上邊界
            whether_to_draw = False
        elif img_loc_y_end < 0:
            whether_to_draw = False
        return whether_to_draw

    @staticmethod
    def detect_frame_line(frame, img, left_up_pint, right_down_point):
        """
        判斷圖像是否超出框線外
        :param frame:原始圖像
        :param img:欲貼上的圖片
        :param left_up_pint:要貼在frame上的左上座標
        :param right_down_point:要貼在frame上的右下座標
        :return:frame 貼完圖的結果
        """
        frame_height, frame_width, frame_channel = frame.shape
        height, width, channel = img.shape
        (img_loc_x_start, img_loc_y_start) = left_up_pint  # 底圖上繪製的左上座標
        (img_loc_x_end, img_loc_y_end) = right_down_point  # 底圖上繪製的右下座標

        img_x_start = 0  # 圖片是否裁切的左下x座標
        img_y_start = 0  # 圖片是否裁切的左下y座標
        img_x_end = width  # 圖片是否裁切的右下x座標
        img_y_end = height  # 圖片是否裁切的右下y座標

        if img_loc_x_start < 0:  # 向左移動超過邊界後start歸零
            img_x_start = -img_loc_x_start
            img_loc_x_start = 0
        if img_loc_y_start < 0:
            img_y_start = -img_loc_y_start
            img_loc_y_start = 0
        if img_loc_x_end < 0:  # 向左移動超過邊界後end也要歸零
            img_x_end = -img_loc_x_end
            img_loc_x_end = 0
        if img_loc_y_end < 0:
            img_y_end = -img_loc_y_end
            img_loc_y_end = 0

        if img_loc_x_end > frame_width:  # 向右移動超過邊界後end歸零
            img_x_end = frame_width - img_loc_x_end
            img_loc_x_end = frame_width
        if img_loc_y_end > frame_height:
            img_y_end = frame_height - img_loc_y_end
            img_loc_y_end = frame_height

        # 指定frame上四點座標 = 將貼圖位置四點座標 與(*) frame上四點座標相乘 並乘以255 (等同於將圖片貼到frame上)
        frame[img_loc_y_start:img_loc_y_end, img_loc_x_start:img_loc_x_end] = \
            img[img_y_start:img_y_end, img_x_start:img_x_end] * \
            frame[img_loc_y_start:img_loc_y_end, img_loc_x_start:img_loc_x_end] * 255

        return frame
        # 把繪製在frame上也合併於此了，以下僅供留存，下方為回傳所有座標，太長(回傳貼圖的四點座標和貼在frame上的四點座標)
        # return img_x_start, img_y_start, img_x_end, img_y_end, img_loc_x_start, img_loc_y_start, img_loc_x_end, img_loc_y_end
