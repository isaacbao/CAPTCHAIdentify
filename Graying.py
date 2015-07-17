#!/usr/bin/python3
# encoding=utf-8

from PIL import Image

from Constant import ColorRatioType
import CustomDataStructureUtil

__author__ = 'pc'


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




def graying(image_uri):
    """灰度化一张图片 / Graying an image

    :param
        image_uri:要灰度化的图片uri / The uri of the image to be graying
    :return:
        无 / None
    """
    # 打开图片
    im = Image.open(image_uri)
    # 灰度化
    imgary = im.convert('RGB')  # L:灰度
    image_name = image_uri[:-4]  # 去除后缀名
    print(image_name)

    list_pixels = list(imgary.getdata())

    list_pixels_for_statistic = list_pixels.copy()  # 用于统计的像素list，接下来要将背景色像数去掉
    remove_background_pixels(list_pixels_for_statistic)

    print(list_pixels.count((255, 255, 255)))

    # pixels_statistic = {}
    pixels_statistic_largest_4 = {}  # 图中最多的的四种颜色 / The 4 colors with the largest area
    least_color_value = 0  # 四种颜色中，最小那种颜色的面积 / The area of the color with the minimal area
    for color in list_pixels_for_statistic:
        # if color not in pixels_statistic:
        area = list_pixels.count(color)
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

    #print(get_color_ration(pixels_statistic_largest_4))

    # Keep pixels in a certain range.
    # 处理图片，保留RGB值在特定范围内的像数
    # width, height = im.size
    # for i in range(0, width-1):
    #     print(list_pixels[i])
    #     list_pixels[i] = (0, 0, 0)
    #
    # imgary.putdata(list_pixels)

    # pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    # print(pixels[2][78])
    # del pixels
    # pixels = 0
    # print(pixels)

    # for i in (0, imgary.size[0]):
    #     for j in (0, imgary.size[1]):
    #         for k in (0, len(pixel_data(i, j))):
    #             print(pixel_data(i, j)[k])

    # imgary.save(image_name + "_gray.jpg")


image_to_graying = r"E:/captchaImage/image/1a6028e7-5f89-4b1b-acdb-22d2d75870b0.jpg"
# image_to_graying = r"E:/captchaImage/4.png"
graying(image_to_graying)
