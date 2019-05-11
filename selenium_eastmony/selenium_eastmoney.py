'''
使用selenium爬取东方财富的数据
'''

import os, time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
# browser = webdriver.Chrome()
wait = WebDriverWait(browser, timeout=10)

def get_index():
    for table in table_setting():
        url = 'http://data.eastmoney.com/bbsj/{}{}/{}.html'.format(str(table['year']), str(table['m_1']), table['t_1'])
        browser.get(url)
        for page in range(table['start_page'], table['end_page'] + 1):
            page_frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#PageContgopage')))
            button_1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_link')))
            page_frame.clear()
            page_frame.send_keys(str(page))
            button_1.click()
            print('正在开始下载{}{}的{}第{}页...'.format(table['year'], table['quarterly'], table['type'], page))
            time.sleep(5)
            df_table = table_parse()
            write_table_file(df_table, '{}{}的{}第{}页'.format(table['year'], table['quarterly'], table['type'], page))

def table_parse():
    # 提取表格内容
    element = browser.find_element_by_css_selector('#dt_1')
    td_content = element.find_elements_by_tag_name('td')

    lst = []
    for td in td_content:
        lst.append(td.text)

    count = len(element.find_elements_by_css_selector('tr:nth-child(1) > td'))
    lst = [lst[i:i+count] for i in range(0,len(lst), count)]

    # 获取页面详细链接
    lst_link = []
    links = element.find_elements_by_css_selector('#dt_1 a.red')
    for link in links:
        lst_link.append(link.get_attribute('href'))

    lst_link = pd.Series(lst_link)
    df_table = pd.DataFrame(lst)
    df_table['url'] = lst_link

    return df_table

def write_table_file(df_table, category):
    path = '../datas/table'
    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(path)
    df_table.to_csv('{}.csv'.format(category), mode='a', encoding='utf-8', index=0, header=0)

# 对spider进行设置
def table_setting():
    print('\t\t\t\t\t\t\t\t\t\t东方财富数据中心')
    print('*****' * 20)
    try:
        year = int(input('请输入年份(2008-2018年):'))
        if year > 2018 or year < 2008:
            while True:
                print('请重新输入!')
                year = int(input('请重新输入请输入年份(2008-2018年):'))
                if year > 2008 or year <= 2018:
                    break
        q_dict = {
            1 : '一季度',
            2 : '中季度',
            3 : '三季度',
            4 : '年报',
        }

        m_dict = {
            1 : '03',
            2 : '06',
            3 : '09',
            4 : '12',
        }

        dict_print(q_dict)
        quarterly = int(input('\n请输入获取第几季度的数据(1-4):'))
        if quarterly < 1 or quarterly > 4:
            while True:
                print('请重新输入!')
                quarterly = int(input('请重新输入获取第几季度的数据(1-4):'))
                if quarterly > 0 or quarterly <= 4:
                    break

        type_dict = {
            1 : '业绩报表',
            2 : '业绩快报',
            3 : '业绩预告',
            4 : '预约披露时间',
            5 : '资产负债表',
            6 : '利润表',
            7 : '现金流量表'}
        t_dict = {
            1: 'yjbb',
            2: 'yjkb',
            3: 'yjyg',
            4: 'yysj',
            5: 'zcfz',
            6: 'lrb',
            7: 'xjll'
        }

        dict_print(type_dict)
        type1 = int(input('\n请输入您想要的报表类型(1-7):'))
        if type1 > 7 or type1 < 1:
            print('输入错误!请重新输入!')
            while True:
                type1 = int(input('请重新输入您想要的报表类型(1-7):'))
                if type1 > 0 or type1 <= 7:
                    break

        start_page = int(input('请输入您需要的起始页:'))
        end_page = int(input('请输入您需要的尾页:'))
        if start_page > end_page:
            print('起始页不能大于尾页!')
            print('输入错误，程序退出，请重启！')
            exit()

        if start_page < 0:
            print('起始页不能小于0')
            print('输入错误，程序退出，请重启！')
            exit()

        yield  {
            'year': year,
            'quarterly':q_dict[quarterly],
            'm_1' : m_dict[quarterly],
            'type': type_dict[type1],
            't_1' : t_dict[type1],
            'start_page': start_page,
            'end_page' : end_page,
        }

    except Exception as e:
        print(e.args)
        print('输入错误，程序退出，请重启！')
        exit()

def dict_print(dict1):
    for k, v in dict1.items():
        print(k, ";", v, end=' ')

# 主函数
def main():
    get_index()

if __name__ == '__main__':
    main()

