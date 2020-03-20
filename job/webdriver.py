# _*_ coding:utf-8 _*_
# 作者:
# 时间:2019/11/19/19:02
from selenium import webdriver


class CtrlChrome(object):
    def __init__(self, url):
        self.browser = webdriver.Chrome(executable_path="./chromedriver.exe")
        self.browser.get(url)

    def __del__(self):
        self.browser.quit()


if __name__ == '__main__':
    obj = CtrlChrome("https://www.baidu.com/")
