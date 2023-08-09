import pytesseract
import cv2
import numpy
import os
import re
from PIL import Image

#imgs = ['123.jpg','456.jpg','789.jpg']

src_folder = 'img'#文件夹名称
filelist = os.listdir(src_folder)

for filename in filelist:
    
    # 跳过非图片文件
    if not filename.endswith('.jpg') and not filename.endswith('.png'):
        continue
    #获取图片

    img = Image.open(os.path.join(src_folder, filename))
    #裁切图片
    crop_img = img.crop((330, 1500, 580, 1600))#左边、左上、右边、右下
    # 转换成OpenCV格式
    cv_img = cv2.cvtColor(numpy.array(crop_img), cv2.COLOR_BGR2GRAY)
    #ref = cv2.threshold(cv_img, 120, 255,cv2.THRESH_BINARY)
    
    # 执行OCR，获取文字
    text = pytesseract.image_to_string(cv_img, lang='eng')
    #print(text)

    #正则表达式筛选
    ll = re.findall("LL\d\d\d",text)
    #数组转字符串
    ll1 = ''.join(ll)
    #调试print(ll)

    if ll1:
        # 文件夹不存在则新建文件夹
        dst_folder = f'{ll1}'
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        # 复制文件到目标文件夹
        dst_path = os.path.join(dst_folder, filename)
        img.save(dst_path)
    else:
        print(filename," 未识别成功，返回信息：",text)
        with open('反馈.txt', 'a', encoding='utf-8') as f:
            f.write(f"{filename}需手动放置，返回信息{text}\n")

        