import random


class GenerateRandomParam:
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

    @staticmethod
    def rt_random_list(text_list, choose_num):
        """
        輸入清單內隨機挑選指定數量的資料輸出清單
        :param text_list: 輸入的清單
        :param choose_num: 選擇資料數量
        :return: 輸出的清單(輸入清單內隨機挑選n個組成)
        """
        output_string = []
        for i in range(choose_num):
            tmp_choose = random.choice(text_list)
            output_string.append(tmp_choose)
        return output_string


if __name__ == '__main__':
    # Done
    print(GenerateRandomParam.generate_same_range_random_num(720, 1280))
    _text_list = [1, 2, 3, 4, 5]
    print(GenerateRandomParam.rt_random_list(text_list=_text_list, choose_num=3))

    # Develop
