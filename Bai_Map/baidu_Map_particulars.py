'''
获取全国公园的详细信息
地点详细检索链接:
http://api.map.baidu.com/place/v2/detail?uid=435d7aea036e54355abbbcc8&output=json&scope=2&ak=您的密钥 //GET请求
'''
import requests, json
from My_Sql import Mysql_API

def get_json(uid):
    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }

    data = {
        'uid':uid,
        'output':'json',
        'scope': 2,
        'ak': 'futZzaYuiPwbInIcjA9vTLwlnkoGuTg5'
    }

    url = "http://api.map.baidu.com/place/v2/detail?"
    try:
        res = requests.get(url, params=data, headers=headers)
        return res.json()
    except Exception as e:
        print(e.args)
        get_json(uid)


uids = Mysql_API()
results = uids.read_uid()
# print(type(results))
for result in results:
    items = get_json(result[0])['result']
    # uid
    try:
        uid = items['uid']
    except:
        uid = None
    # 街道id
    try:
        street_id = items['street_id']
    except:
        street_id = None
    # 名称
    try:
        name = items['name']
    except:
        name = None
    # 地址
    try:
        address = items['address']
    except:
        address = None
    # 开放时间
    try:
        shop_hours = items['detail_info']['shop_hours']
    except:
        shop_hours = None
    # 详细链接
    try:
        detail_url = items['detail_info']['detail_url']
    except:
        detail_url = None
    # 价格
    try:
        price = items['detail_info']['price']
    except:
        price = None
    # 经典类型
    try:
        scope_type = items['detail_info']['scop_type']
    except:
        scope_type = None
    # 景点等级
    try:
        scope_grade = items['detail_info']['scope_grade']
    except:
        scope_grade = None
    # 景点说明
    try:
        content_tag = items['detail_info']['content_tag']
    except:
        content_tag = None

    # print(uid, street_id, name, address, shop_hours, detail_url, price, scope_type, scope_grade,content_tag)

    infos = {
        'uid': uid,
        'street_id': street_id,
        'name': name,
        'address': address,
        'shop_hours': shop_hours,
        'detail_url': detail_url,
        'price': price,
        'scope_type':scope_type,
        'scope_grade': scope_grade,
        'content_tag': content_tag
    }
    uids.insert_data('park', 'particular', infos)