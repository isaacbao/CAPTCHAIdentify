#!/usr/bin/python3
# encoding=utf-8

from PIL import Image
import os

from Constant import ColorRatioType
import CustomDataStructureUtil

__author__ = 'pc'


def pretreate_image(im, image_name):
    """对图像进行预处理

    :param im:
        需要预处理的图像
    :return:
        无
    """
    threshold = 180

    image_binary = image_binaryzation(im, threshold)
    image_binary_pixels = list(image_binary.getdata())

    im_rgb = im.convert('RGB')

    list_rgb_pixels = list(im_rgb.getdata())

    image_rgb_pixels = list_rgb_pixels.copy()
    width, height = im.size
    remove_noise(image_rgb_pixels, image_binary_pixels, width, height)
    im_rgb.putdata(image_rgb_pixels)
    im_rgb.save(image_name + "_without_noise.jpg")

    list_pixels_for_statistic = image_rgb_pixels.copy()  # 用于统计的像素list，接下来要将背景色像数去掉
    remove_background_pixels(list_pixels_for_statistic)

    # pixels_statistic = {}
    pixels_statistic_largest_4 = {}  # 图中最多的的四种颜色 / The 4 colors with the largest area
    least_color_value = 0  # 四种颜色中，最小那种颜色的面积 / The area of the color with the minimal area
    for color in list_pixels_for_statistic:
        # if color not in pixels_statistic:
        area = list_pixels_for_statistic.count(color)
        # pixels_statistic.setdefault(color, area)

        if len(pixels_statistic_largest_4) < 4:
            pixels_statistic_largest_4.setdefault(color, area)
            least_color_key, least_color_value = CustomDataStructureUtil.get_min(pixels_statistic_largest_4)
        else:
            if color not in pixels_statistic_largest_4:
                if area > least_color_value:
                    pixels_statistic_largest_4.pop(least_color_key)
                    pixels_statistic_largest_4.setdefault(color, area)
                    least_color_key, least_color_value = CustomDataStructureUtil.get_min(pixels_statistic_largest_4)
                    print(CustomDataStructureUtil.get_min(pixels_statistic_largest_4)[1])

    print(pixels_statistic_largest_4)
    largest_colors = list(pixels_statistic_largest_4.keys())
    image_pixels = image_rgb_pixels.copy()
    for large_color in largest_colors:
        get_single_color_image(im_rgb.copy(), image_pixels.copy(), large_color, width, height)
    # print(image_pixels)
    # print(get_color_ration(pixels_statistic_largest_4))
    # Keep pixels in a certain range.
    # 处理图片，保留RGB值在特定范围内的像数

    # pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    # print(pixels[2][78])
    # del pixels
    # pixels = 0
    # print(pixels)

    # for i in (0, im_rgb.size[0]):
    #     for j in (0, im_rgb.size[1]):
    #         for k in (0, len(pixel_data(i, j))):
    #             print(pixel_data(i, j)[k])



def image_binaryzation(im, threshold):
    # 灰度化
    im_gray = im.convert("L")
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(255)
            # table.append(1)
    # convert to binary image by the table
    im_binary = im_gray.point(table, '1')
    # print(list(im_binary.getdata()))
    return im_binary


def remove_background_pixels(list_pixels_for_statistic):
    """移除背景像数 / Remove the pixels with background color

    :param list_pixels_for_statistic: 像数list / pixels list
    :return:
    """
    while 0 != list_pixels_for_statistic.count((255, 255, 255)):
        list_pixels_for_statistic.remove((255, 255, 255))


def get_color_ration(pixels_statistic):
    """计算图中最主要的四种颜色的分布 / Get the 4 main colors' ratio in image
    一幅4字的彩色验证码中，我们把占图片比例最多的四种颜色，根据面积由大到小排列为：first, second, third, fourth
    考虑到噪点和干扰线，四个字颜色分布可能为
    Type_A - 4个字分为4种不同颜色：first : second ∈ [1, 1.5) && second : third ∈ [1,1.5)
    Type_B - 4个字分为3种不同颜色，其中2个字颜色一样： first : second ∈ [1.5, 2.5) && second : third ∈ [1, 1.5)
    Type_C - 4个字分为2种不同颜色，每种颜色2个字： first:second ∈ [1, 1.5) && second : third ∈ [3.5, ∞)
    Type_D - 4个字分为2种不同颜色，其中1种颜色3个字，1种颜色1个字： first : second  ∈ [2.5, 3.5)
    Type_E - 4个字颜色相同： first : second ∈ [3.5, ∞)


    :param
        pixels_statistic: 像数统计结果 / The result of the statistic of pixel
    :return:
        string color_ratio_type:
    """

    if isinstance(pixels_statistic, dict):
        pixels_statistic_temp = pixels_statistic.copy()

        first = CustomDataStructureUtil.get_max(pixels_statistic_temp)
        pixels_statistic_temp.pop(first[0])

        second = CustomDataStructureUtil.get_max(pixels_statistic_temp)
        pixels_statistic_temp.pop(second[0])

        rotia_first_second = first[1] / second[1]

        if 1 <= rotia_first_second < 1.5:
            third = CustomDataStructureUtil.get_max(pixels_statistic_temp)
            pixels_statistic_temp.pop(third[0])
            rotia_second_third = second[1] / third[1]
            if 1 <= rotia_second_third < 1.5:
                return ColorRatioType.__TYPE_A__
            elif rotia_second_third > 3.5:
                return ColorRatioType.__TYPE_C__
        elif 1.5 <= rotia_first_second < 2.5:
            return ColorRatioType.__TYPE_B__
        elif 2.5 <= rotia_first_second < 3.5:
            return ColorRatioType.__TYPE_D__
        elif 3.5 <= rotia_first_second:
            return ColorRatioType.__TYPE_E__


def get_distance(point_a, point_b):
    """获得两点间的距离 / Get distance between two point

    :param point_a:
        第一个点 / The first point
    :param point_b:
        第二个点 / The second point
    :return:
        int 距离的平方 / distance ^ 2
    """

    return pow((point_a[0] - point_b[0]) * 0.3, 2) + pow((point_a[1] - point_b[1]) * 0.59, 2) + pow(
        (point_a[1] - point_b[1]) * 0.1, 2)


def get_single_color_image(image, image_pixels, color, width, height):
    """获得单色图片

    :param image_pixels:
        单色图片中的像数 / Pixels in the single color image
    :param color:
        图片的颜色
    :return:
        无
    """

    for y in range(height):
        for x in range(width):
            # print(image_pixels[y * width + x])
            # print(color)
            if image_pixels[y * width + x] != color:

                image_pixels[y * width + x] = (255, 255, 255)

    image.putdata(image_pixels)
    i = 0
    image_path = image_name + "_single_color_" + str(i) + ".jpg"
    while os.path.exists(image_path):
        i += 1
        image_path = image_name + "_single_color_" + str(i) + ".jpg"
    image.save(image_path)

def remove_noise(image_pixels, binary_pixels, width, height):
    """去除噪点

    :param image_pixels:
        图片像数
    :param image_pixels:
        二值化图片像数
    :param width:
        图片宽度
    :param height:
        图片长度
    :return:
    """

    for y in range(height):
        for x in range(width):
            color = binary_pixels[y * width + x]

            if color == 255:
                continue

            weight = 0
            up = y - 1
            down = y + 1
            left = x - 1
            right = x + 1

            position_up_left = up * width + left
            if 0 < position_up_left < 2800:
                if binary_pixels[position_up_left] == 0:
                    weight += 1

            position_up = up * width + x
            if 0 < position_up < 2800:
                if binary_pixels[position_up_left] == 0:
                    weight += 1

            position_up_right = up * width + right
            if 0 <position_up_right < 2800:
                if binary_pixels[position_up_right] == 0:
                    weight += 1

            position_left = y * width + left
            if 0 < position_left < 2800:
                if binary_pixels[position_left] == 0:
                    weight += 1

            position_right = y * width + right
            if 0 < position_right < 2800:
                if binary_pixels[position_right] == 0:
                    weight += 1

            position_down_left = down * width + left
            if 0 < position_down_left < 2800:
                if binary_pixels[position_down_left] == 0:
                    weight += 1

            position_down = down * width + x
            if 0 < position_down < 2800:
                if binary_pixels[position_down] == 0:
                    weight += 1

            position_down_right = down * width + right
            if 0 < position_down_right < 2800:
                if binary_pixels[position_down_right] == 0:
                    weight += 1

            if weight <= 3:
                binary_pixels[y * width + x] = 255

    for i in range(width * height):
        if binary_pixels[i] == 255:
            image_pixels[i] = (255, 255, 255)


def graying(image_uri):
    """灰度化一张图片 / Graying an image

    :param
        image_uri:要灰度化的图片uri / The uri of the image to be graying
    :return:
        无 / None
    """


image_uri = r"E:/captchaImage/image/1f6cf12c-2ee0-4c6e-866d-c32ed653f0fe.jpg"
# image_to_graying = r"E:/captchaImage/4.png"

# 打开图片
im = Image.open(image_uri)
image_name = image_uri[:-4]  # 去除后缀名
print(image_name)
pretreate_image(im, image_name)
graying(im)
