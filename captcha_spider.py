# -*- coding: utf-8 -*-
# @Time    : 2020/4/19
# @Author  : lyh-god
# @FileName: captcha_spider.py
# @Software: PyCharm

# -*- coding: utf-8 -*-
import random
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class CNBlogSelenium(object):
    def __init__(self):
        opt = webdriver.ChromeOptions()
        # 设置无头模式，调试的时候可以注释这句
        # opt.set_headless()
        self.driver = webdriver.Chrome(executable_path=r"chrome/chromedriver.exe", chrome_options=opt)
        self.driver.set_window_size(1440, 900)

    def visit_login(self):
        try:

            self.driver.get("https://passport.cnblogs.com/user/signin")

            WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="LoginName"]')))
            username = self.driver.find_element_by_xpath('//*[@id="LoginName"]')
            username.clear()
            username.send_keys("24364565")

            WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Password"]')))
            password = self.driver.find_element_by_xpath('//*[@id="Password"]')
            password.clear()
            password.send_keys("53647475475")

            WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitBtn"]')))
            signin = self.driver.find_element_by_xpath('//*[@id="submitBtn"]')
            signin.click()

            WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="geetest_refresh_1"]')))
            geetest = self.driver.find_element_by_xpath('//*[@class=geetest_refresh_1"]')
            geetest.click()

            #点击滑动验证码后加载图片需要时间
            time.sleep(3)

            self.analog_move()

        except :
            pass

        self.driver.quit()

    # 截图处理
    def screenshot_processing(self):
        WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable(
            (By.XPATH, '//canvas[@class="geetest_canvas_fullbg geetest_fade geetest_absolute"]')))
        element = self.driver.find_element_by_xpath(
            '//canvas[@class="geetest_canvas_fullbg geetest_fade geetest_absolute"]')

        # 保存登录页面截图
        self.driver.get_screenshot_as_file("login.png")
        image = Image.open("login.png")

        # 打开截图，获取element的坐标和大小
        left = element.location.get("x")
        top = element.location.get("y")
        right = left + element.size.get("width")
        bottom = top + element.size.get("height")

        # 对此区域进行截图，然后灰度处理
        cropImg = image.crop((left, top, right, bottom))
        full_Img = cropImg.convert("L")
        full_Img.save("fullimage.png")

        WebDriverWait(self.driver, 10, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="geetest_slider_button"]')))
        move_btn = self.driver.find_element_by_xpath('//*[@class="geetest_slider_button"]')

        ActionChains(self.driver).move_to_element(move_btn).click_and_hold(move_btn).perform()

        WebDriverWait(self.driver, 10, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, '//canvas[@class="geetest_canvas_slice geetest_absolute"]')))
        element = self.driver.find_element_by_xpath('//canvas[@class="geetest_canvas_slice geetest_absolute"]')

        self.driver.get_screenshot_as_file("login.png")
        image = Image.open("login.png")
        left = element.location.get("x")
        top = element.location.get("y")
        right = left + element.size.get("width")
        bottom = top + element.size.get("height")
        cropImg = image.crop((left, top, right, bottom))
        cut_Img = cropImg.convert("L")
        cut_Img.save("cutimage.png")


if __name__ == '__main__':
    print()