from utils.gif_tools import GifTools
from core.generate_digital_map_gif import GenerateDigitalMapGif
from core.generate_dvd_bounce_gif import GenerateDVDBounceGif
from core.generate_math_fantasy import GenerateMathFantasyGif
from core.generate_digital_text_mask import GenerateDigitalTextGif

if __name__ == '__main__':
    # Notice : if you use show_gif function, you need to press "blank key" to leave windows
    # 注意 : 如果您使用show_gif功能，您需要按“空白鍵”離開視窗
    # 0. 顯示GIF圖像
    path = "./data/300x300_y_flow_random_map.gif"
    GifTools.read_and_show_gif(path, frame_rate=60)

    # Example GIF
    example_shape = (300, 300)

    # 1. random_number_map；生成隨機座標隨機數字圖像
    gif_list = GenerateDigitalMapGif.random_number_map(example_shape, numbers_of_numbers=100)
    GifTools.show_gif(gif_list, frame_rate=10)  # 顯示生成的GIF圖片
    # 儲存圖片則調用下面此行，以下為示範，其後不示範儲存圖像，設定檔名.gif，檔案將儲存在/data資料夾下 (若要儲存圖片，不建議顯示圖片，會占用大量記憶體==)
    # GifTools.cv2_img_list_save_gif(gif_list, "300x300_same_range_random_number_map.gif", frame_rate=10)

    # 2. full_random_number_map；生成全區域隨機數字圖像
    gif_list = GenerateDigitalMapGif.full_random_number_map(example_shape, word_distance=25)
    GifTools.show_gif(gif_list, frame_rate=10)

    # 3. y_flow_random_map；生成類似The Matrix(駭客任務)風格背景
    gif_list = GenerateDigitalMapGif.y_flow_random_map(example_shape, gif_sec=3)
    GifTools.show_gif(gif_list, frame_rate=60)

    # 4. dvd_bounce_by_random_color；生成類似DVD反彈螢幕保護程式
    # gif_list = GenerateDVDBounceGif.dvd_bounce_by_random_color(example_shape, gif_sec=10)  # 舊版本；純文字版
    gif_list = GenerateDVDBounceGif.dvd_bounce_with_img(example_shape, gif_sec=10)  # 新版本；圖片碰撞版本
    GifTools.show_gif(gif_list, frame_rate=50)

    # 5. math_fantasy；數學幻想(?)，思考時背後運算的數學特效
    gif_list = GenerateMathFantasyGif.math_fantasy(img_shape=example_shape, gif_sec=2)
    GifTools.show_gif(gif_list, frame_rate=60)

    # 6. digital_text_mask；數位文字圖像，大文字由隨機不斷變換的小數字構成，亦可以替換成自己的剪影(蒙版)
    gif_list = GenerateDigitalTextGif.digital_text_mask(img_shape=(300, 300), few_frame_transform=2)
    GifTools.show_gif(gif_list, frame_rate=30)
