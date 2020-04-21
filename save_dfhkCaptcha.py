# -*- coding: utf-8 -*-
# @Time    : 2020/4/21
# @Author  : lyh-god
# @FileName: save_dfhkCaptcha.py
# @Software: PyCharm

# -*- coding: utf-8 -*-
# @Time    : 2020/4/21
# @Author  : lyh-god
# @FileName: sava_bilibiliCaptcha.py
# @Software: PyCharm

import random
import time, re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import sys
import base64
import configparser

'''
极验验证滑块3.0版本
'''

file = 'config.ini'
# 创建配置文件对象
config_parse = configparser.ConfigParser()
config_parse.read(file, encoding='utf-8')
count = config_parse.getint("captcha", "count")  # 滑动验证码数数
type=config_parse.getint("captcha","type")#网站类型

class Binance(object):
    def __init__(self):
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(executable_path=r"chrome/chromedriver.exe",chrome_options=chrome_option)
        self.driver.set_window_size(1440, 900)
        self.type=type
    def visit_index(self):
        # 输入邮箱和密码
        self.driver.get("http://www.ceair.com/aoc/#/flightNo/2020-05-29/MU2170")
        # email = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'login-username')))
        # email.clear()
        # email.send_keys("13542012479")
        # pwd = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        # pwd.clear()
        # pwd.send_keys("54475686778")
        # time.sleep(1)
        # 点击登录，弹出滑块验证码
        # login_btn = WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-login')))
        # login_btn.click()
        # time.sleep(0.2)
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_fullbg')))
        except:
            pass

        # 进入模拟拖动流程
        finally:
            while(time.sleep(0.5),True):
                try:
                    self.analog_drag()
                except:
                    retry_but = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_panel_error_content')))
                    retry_but.click()
                    time.sleep(0.2)
                    # login_btn.click()
                    # time.sleep(0.2)


    def analog_drag(self):

        # 刷新一下极验图片
        element = self.driver.find_element_by_xpath('//a[@class="geetest_refresh_1"]')
        element.click()
        time.sleep(1)

        # 保存两张图片
        # self.save_img('full.jpg', 'geetest_canvas_fullbg')
        self.save_img('geetest_canvas_bg')
        '''
        full_image = Image.open('full.jpg')
        cut_image = Image.open('cut.jpg')

        # 根据两个图片计算距离
        distance = self.get_offset_distance(cut_image, full_image)

        # 开始移动
        self.start_move(distance)

        # 如果出现error
        try:
            WebDriverWait(self.driver, 5, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_slider geetest_error"]')))
            print("验证失败")
            return
        except TimeoutException as e:
            pass

        # 判断是否验证成功
        try:
            WebDriverWait(self.driver, 10, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_slider geetest_success"]')))
        except TimeoutException:
            print("again times")
            self.analog_drag()
        else:
            print("验证成功")

    '''
    def save_img(self,class_name):
        global count
        getImgJS = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/png");'
        img = self.driver.execute_script(getImgJS)
        base64_data_img = img[img.find(',') + 1:]
        image_base = base64.b64decode(base64_data_img)
        count+=1
        file = open(f'./imageD/{count}.jpg', 'wb')
        config_parse.set("captcha", "count", str(count))
        with open("config.ini", "w+") as f:
            config_parse.write(f)
        file.write(image_base)
        file.close()
        while(count>50):
            sys.exit(0)

    # 判断颜色是否相近
    def is_similar_color(self, x_pixel, y_pixel):
        for i, pixel in enumerate(x_pixel):
            if abs(y_pixel[i] - pixel) > 50:
                return False
        return True

    # 计算距离
    def get_offset_distance(self, cut_image, full_image):
        for x in range(cut_image.width):
            for y in range(cut_image.height):
                cpx = cut_image.getpixel((x, y))
                fpx = full_image.getpixel((x, y))
                if not self.is_similar_color(cpx, fpx):
                    img = cut_image.crop((x, y, x + 50, y + 40))
                    # 保存一下计算出来位置图片，看看是不是缺口部分
                    img.save("1.png")
                    return x

    # 开始移动
    def start_move(self, distance):
        element = self.driver.find_element_by_xpath('//div[@class="geetest_slider_button"]')

        # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
        distance -= element.size.get('width') / 2
        distance += 25

        # 按下鼠标左键
        ActionChains(self.driver).click_and_hold(element).perform()
        time.sleep(0.5)
        while distance > 0:
            if distance > 10:
                # 如果距离大于10，就让他移动快一点
                span = random.randint(5, 8)
            else:
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            distance -= span
            time.sleep(random.randint(10, 50) / 100)

        ActionChains(self.driver).move_by_offset(distance, 1).perform()
        ActionChains(self.driver).release(on_element=element).perform()

if __name__ == "__main__":
    b = Binance()
    b.visit_index()
