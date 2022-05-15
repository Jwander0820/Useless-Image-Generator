import numpy as np
import cv2
from utils.img_tools import ImgTools

example_shape = (300, 300, 3)
mask = np.full(example_shape, (0, 0, 0), dtype=np.uint8)  # 生成蒙版

# cv2.putText(mask, "123456", (100, 25), cv2.FONT_HERSHEY_DUPLEX,
#             1, (63, 218, 109), 2, cv2.LINE_AA)
# cv2.putText(mask, "123456", (100, 75), cv2.FONT_HERSHEY_DUPLEX,
#             1, (50, 200, 100), 2, cv2.LINE_AA)
# cv2.putText(mask, "123456", (100, 100), cv2.FONT_HERSHEY_DUPLEX,
#             1, (100, 225, 150), 2, cv2.LINE_AA)
cv2.putText(mask, "123456", (100, 125), cv2.FONT_HERSHEY_DUPLEX,
            2, (200, 255, 250), 2, cv2.LINE_AA)

ImgTools.show_img(mask)

print(1000//10)


