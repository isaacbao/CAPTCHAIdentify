#!/usr/bin/python3
# encoding=utf-8
__author__ = 'pc'

try:
    import pytesseract
    from PIL import Image
except ImportError:
    print('模块导入错误,请使用pip安装,pytesseract依赖：')
    raise SystemExit

# image = Image.open(r"E:/captchaImage/10.png")
# imgary = image.convert('L')
# vcode = pytesseract.image_to_string(image)
# print(vcode)

