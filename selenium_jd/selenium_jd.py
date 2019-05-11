import time
import tkinter
from lxml import etree
from Mysql_demo import MySqlDemo

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse_comm(html):
    html = etree.HTML(html)

    # 获取商品信息
    lis = html.xpath('//ul[@class="gl-warp clearfix"]/li')
    print(len(lis))

    for li in lis:
        # 创建一个存储数据的字典
        items = {}
        # 获取商品标题
        title = li.xpath('string(./div/div/a/em)')
        # 获取价格
        price = li.xpath('string(./div/div[@class="p-price"]/strong)')
        # 获取评价数量
        commit = li.xpath('string(./div/div[@class="p-commit"]/strong)')
        # 获取商店名称
        store = li.xpath('string(./div/div[@class="p-shop"]/span/a)')
        # 获取商品链接
        href = li.xpath('./div/div[@class="p-name p-name-type-2"]/a/@href')[0]
        https = 'https:'
        # 做一个判断，如果商品链接里面没有协议，手动连接一下
        if https in href:
            href = href
        else:
            href = https + href

        items['title'] = title
        items['price'] = price
        items['commit'] = commit
        items['store'] = store
        items['href'] = href
        print(items)

        yield items

def get_page():
    global num
    if num > 88:
        return None
    # 将页面拉到底部，把所有的商品信息加载出来
    browser.execute_script('window.scrollTo(2000, document.body.scrollHeight)')
    time.sleep(1)
    # 对页面的源码进行解析
    items = parse_comm(browser.page_source)
    mysql.insert_data(items)
    try:
        next_page = browser.find_element_by_class_name('pn-next')
        next_page.click()
        num += 1
        get_page()
    except Exception as e:
        print(e.args)

def get_comm(comm):
    browser.get(url)
    # 找到输入框的节点
    input_box1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#key')))
    # 找到搜索按钮的节点
    submit = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.button')))
    # 清除框内内容
    input_box1.clear()
    # 输入要搜索的商品
    input_box1.send_keys(comm)
    # 点击搜索按钮
    submit.click()
    time.sleep(2)
    # 获取到页面之后进行截屏
    browser.save_screenshot(comm + '.png')
    get_page()

def main():
    print('\t\t\t\t\t------京东商品爬取-------\t\t\t\t\t\t')
    comm = input('请输入您要的商品信息:')
    # comm = 'ipad'
    get_comm(comm)


if __name__ == '__main__':

    chromeoptions = webdriver.ChromeOptions()
    chromeoptions.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chromeoptions)
    wait = WebDriverWait(browser,timeout=10)
    url = 'https://www.jd.com/2019'
    mysql = MySqlDemo()
    num = 0

    main()
    time.sleep(2)
    mysql.close_db()
    browser.close()