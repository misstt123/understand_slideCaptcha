# -*- coding: utf-8 -*-
# @Time    : 2020/4/22
# @Author  : lyh-god
# @FileName: changeMode.py
# @Software: PyCharm

from PIL import Image
import os
count=1

def convert_RGB(path):
    global count
    imgs=os.listdir(str(path))
    for img in imgs:

        img=Image.open(f"{path}/{img}")
        img=img.convert("RGB")

        img.save(f'pic/{count}.jpg')
        count+=1

if __name__ == '__main__':
    lis=["imageB","imageD"]
    for item in lis:
        convert_RGB(item)
