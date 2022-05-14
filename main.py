import cv2
import numpy as np
import random
from PIL import Image, ImageSequence
from utils.img_tools import ImgTools
from utils.generator_data import *
from core.generate_digital_map import GenerateDigitalMap


def main():
    img_shape1080 = (1920, 1080)
    img_shape720 = (1280, 720)
    GenerateDigitalMap.random_number_map()


if __name__ == '__main__':
    # Example
    example_shape = (300, 300)
    # 1. random_number_map
    # GenerateDigitalMap.random_number_map(example_shape,
    #                                      numbers_of_numbers=100,
    #                                      save_gif_name="300x300_same_range_random_number_map.gif")
    # 2. full_random_number_map
    # GenerateDigitalMap.full_random_number_map(example_shape,
    #                                           step=25,
    #                                           save_gif_name="300x300_full_range_random_number_map.gif")

    # main()

    path = "./data/300x300_full_range_random_number_map.gif"
    ImgTools.read_and_show_gif(path, frame_rate=10)

