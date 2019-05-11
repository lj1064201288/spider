'''
解析网页数据
'''
import re
from lxml import etree
from bs4 import BeautifulSoup
from urllib import request

class HtmlParse(object):
    def __init__(self, html):
        self.html = html

    def parse_xpath(self, parameter):
        html = etree.HTML(self.html)
        info = html.xpath(parameter)

        return info

    def parase_css_selector(self, parameter):
        soup = BeautifulSoup(self.html, 'lxml', from_encoding='utf-8')
        info = soup.select(parameter)

        return info





