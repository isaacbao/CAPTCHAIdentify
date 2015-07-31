#!/usr/bin/python3
# encoding=utf-8
__author__ = 'pc'

try:
    import pytesseract
    from PIL import Image
except ImportError:
    print('模块导入错误,请使用pip安装,pytesseract依赖：')
    raise SystemExit


def simple_identify(path):
    """通过直接调用Pytesseract识别简单的验证码
       Identify simple captcha with pytesseract

    :param path: 验证码存储的地址
    :return:验证码
    """
    image = Image.open(path)
    vcode = pytesseract.image_to_string(image)
    return vcode
