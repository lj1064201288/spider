'''
获取全国公园信息保存至MySQL数据库当中
地点检索详情链接
http://api.map.baidu.com/place/v2/detail?uid=435d7aea036e54355abbbcc8&output=json&scope=2&ak=您的密钥 //GET请求
基础地址
http://api.map.baidu.com/place/v2/search?
参数
    query:公园
    region: 成都市
    scope: 2
    page_size: 20
    output:json
    ak:TLkSqB53Mwap6mRvNiHbNBkL7HiGmwcu
'''

import requests
from lxml import etree
from My_Sql import Mysql_API

# 百度地图API
def get_json(loc, page_num=0):
    '''
    :param loc: 城市地址
    :param page_num: 页数
    :return:
    '''
    data = {
        'query':'公园',
        'region': loc,
        'scope': '2',
        'page_size':20,
        'page_num': page_num,
        'output': 'json',
        'ak':'futZzaYuiPwbInIcjA9vTLwlnkoGuTg5'
    }

    url = "http://api.map.baidu.com/place/v2/search?"
    res = requests.get(url, params=data, headers=headers)
     # print(res.url)
    decodejson = res.json()
    # page_num += 1

    return decodejson

# 获取中国省份列表
def province_spider():
    url = "http://www.tcmap.com.cn/list/jiancheng_list.html"
    res = requests.get(url)
    # 网页的字体编码为gb2312所以在此转码
    response = res.content.decode('GB2312')
    # print(response)
    html = etree.HTML(response)
    provinces = html.xpath('//tr/td/a/text()')
    return  provinces

# 提取信息
def parse_data(datas):
    # 增加判定信息
    for data in datas:
        try:
            name = data['name']
        except:
            name = None
        try :
            lat = data['location']['lat']
        except:
            lat = None
        try:
            lng = data['location']['lng']
        except:
            lng = None
        try:
            address = data['address']
        except:
            address = None
        try:
            area = data['area']
        except:
            area = None
        try:
            uid = data['uid']
        except:
            uid = None
        try:
            city = data['city']
        except:
            city = None

        items = {
            'name': name,
            'locatlat':lat,
            'locatlng': lng,
            'address': address,
            'area': area,
            'uid': uid,
            'city': city
        }
        # print(items)
        yield items

# 提取所有市区
def city_spider(citys):
    for city in citys['results']:
        page_num = 0
        while True:
            datas = get_json(city['name'], page_num)['results']
            if datas:
                items = parse_data(datas)
                # print(list(items))
                down_sql(items)
                page_num += 1
            else:
                break

# 存储数据
def down_sql(items):
    sql = Mysql_API()
    for item in items:
        try:
            print(item)
            sql.insert_data('park', 'park', item)
        except Exception as e:
            print(e.args)
    sql.db_close()

# 启动函数
def main():
    province_list = province_spider()
    municipality = ['北京', '天津', '上海', '重庆', '香港特别行政区', '澳门', '台湾', '吉林' ]
    # print(province_list)
    for province in province_list:
        page_num = 0
        # 如果地区为直辖市,则直接提取数据
        if  province in municipality:
            while True:
                datas = get_json(province, page_num)['results']
                print(page_num)
                if datas:
                    items = parse_data(datas)
                    # print(list(items))
                    down_sql(items)
                    page_num += 1
                else:
                    break
        else:
            citys = get_json(province)
            city_spider(citys)

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # 爬取的页数统计
    main()
