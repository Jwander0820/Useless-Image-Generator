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
        gif_img_shape = (height, weight, 3)
        text_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        gif_list = []
        for frame in range(30):
            mask = np.full(gif_img_shape, (0, 0, 0), dtype=np.uint8)  # 生成蒙版
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
        if save_gif_name is None:
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
        gif_img_shape = (height, weight, 3)
        text_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        gif_list = []
        for frame in range(30):
            mask = np.full(gif_img_shape, (0, 0, 0), dtype=np.uint8)  # 生成蒙版
            for i in range(0, weight+word_distance, word_distance):
                for j in range(0, height+word_distance, word_distance):
                    location = (i, j)
                    cv2.putText(mask, random.choice(text_list), location, cv2.FONT_HERSHEY_DUPLEX,
                                1, (255, 255, 255), 2, cv2.LINE_AA)
            gif_list.append(mask)
        if save_gif_name is None:
            ImgTools.show_gif(gif_list, frame_rate=10)
        if save_gif_name:
            ImgTools.cv2_img_list_save_gif(gif_list, save_gif_name)

    @staticmethod
    def _y_element(mask, element_param, output_string, i):
        """
        y_flow單位字串處理；須配合y_element的for迴圈處理每張圖像，才會有字串"移動"的感覺
        :param mask:被繪製的蒙版
        :param element_param:元素字串參數
        :param output_string:字串資料(清單)
        :param i:迭代器對應到外部迴圈的第幾張圖片
        :return:element_param更新過後的元素字串參數(主要是更新repeat_time，字串重複到底的次數)
        """
        # start_frame為起始幀，假設start_frame為10代表從第10張開始出現
        # repeat_time = 0  # 迴圈計數器，若字串超過界線，回到起點重新跑
        [start_frame, repeat_time, location_x, move_step, choose_num, word_size, height] = element_param
        if i < start_frame:  # 若起始幀大於現在幀數，直接回傳跳出該迴圈，如此能保證一定是從最上面出發
            return element_param
        # int(word_size * 25) * (-choose_num) * (n + 1) 為起始座標
        # move_step * (i - start_frame) 為每幀移動步伐
        # repeat_time為計數用，若move長度超過高度，則減去一個圖像高度，且起點多後退一步，這樣就能讓字串從起點再跑一次
        move = int(word_size * 25) * (-choose_num) * (repeat_time + 1) + move_step * (i - start_frame) - (height * repeat_time)
        if move > height:
            repeat_time += 1
        mask = MoveText.y_flow(mask, output_string, move, location_x, word_size)
        element_param = [start_frame, repeat_time, location_x, move_step, choose_num, word_size, height]  # 更新元素字串參數
        return element_param

    @staticmethod
    def y_element(gif_list, text_list,  img_shape=(1280, 720), number_of_string=1):
        """
        y_flow的單位圖像處理；本函式也可以外部重複執行(更換text_list等...)
        :param gif_list:底圖清單資料
        :param text_list:隨機從該清單內挑選n個字繪製於底圖上
        :param img_shape:圖像尺寸大小
        :param number_of_string:共要生成幾組單位字串(1次就代表會有1行文字從上到下)
        :return: 回傳處理完的底圖清單資料
        """
        element_param_list = []
        output_string_list = []
        for i in range(number_of_string):  # 生成n組字串參數
            element_param, output_string = MoveText.generate_y_flow_element_param(img_shape, gif_list, text_list)
            element_param_list.append(element_param)
            output_string_list.append(output_string)
        for i in range(len(gif_list)):  # 循序處理每張底圖
            mask = gif_list[i]
            for j in range(len(element_param_list)):  # 根據參數畫在每張底圖上
                element_param_list[j] = GenerateDigitalMap._y_element(
                    mask, element_param_list[j], output_string_list[j], i)
        return gif_list

    @staticmethod
    def y_flow_random_map(img_shape=(1280, 720), save_gif_name=None):
        """
        生成y方向移動的隨機字串gif，類似The Matrix駭客任務的風格圖像
        :param img_shape:指定圖像尺寸大小
        :param save_gif_name:儲存的檔案名稱
        :return:
        """
        weight, height = img_shape
        gif_img_shape = (height, weight, 3)  # 底圖尺寸大小
        gif_list = MoveText.generate_frame(gif_img_shape, frame=60, gif_sec=3)  # 生成幀數*秒數的底圖張數，並儲存成清單
        text_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]  # 從該清單內隨機取樣資料繪製於底圖上

        gif_list = GenerateDigitalMap.y_element(gif_list, text_list, img_shape=img_shape, number_of_string=weight // 20)

        if save_gif_name is None:
            ImgTools.show_gif(gif_list, frame_rate=60)  # 若要儲存圖片，不建議顯示圖片，會占用大量記憶體==
        if save_gif_name:
            ImgTools.cv2_img_list_save_gif(gif_list, save_gif_name, frame_rate=30)


if __name__ == '__main__':
    example_shape = (500, 500)
    # Done
    # GenerateDigitalMap.random_number_map(example_shape)
    # GenerateDigitalMap.full_random_number_map(example_shape)
    GenerateDigitalMap.y_flow_random_map(example_shape)

    # Develop
