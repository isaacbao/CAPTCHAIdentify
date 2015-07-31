#!/usr/bin/python3
# encoding=utf-8
__author__ = 'pc'

try:
    import pytesseract
    from PIL import Image
except ImportError:
    print('模块导入错误,请使用pip安装,pytesseract依赖：')
    raise SystemExit

path = r"E:\captchaImage\code.jpg"
image = Image.open(path)
imgary = image.convert('L')
vcode = pytesseract.image_to_string(image)
print(vcode)

