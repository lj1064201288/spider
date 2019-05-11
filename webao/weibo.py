'''
爬取微博用户扇子NO_FAN_NO_FUN的信息,信息点包括：转、评、赞、播放量、文字内容、视频时长
打开该用户的微博之后，得到
url:  https://m.weibo.cn/api/container/getIndex?
该请求是是一个post请求方式,需要传入的数据有
# 固定的信息
containerid: 2304131944603171_-_WEIBO_SECOND_PROFILE_WEIBO
# 固定的信息
page_type: 03
# 表示页数
page: 5


containerid: 2304131944603171_-_WEIBO_SECOND_PROFILE_WEIBO
luicode: 10000011
lfid: 2302831944603171
page_type: 03
page: 4

打开url发现是传过来的数据都是json类型的，需要获取的数据都是在data下的cards下面
'''
import time, random
import requests
from openpyxl import Workbook


agents = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
]

# 获取页面的数据
def get_page(page):
    # 设置data
    data = {
        "containerid": "2304131944603171_-_WEIBO_SECOND_PROFILE_WEIBO",
        "luicode": '10000011',
        "lfid": '2302831944603171',
        "page_type": '03',
        "page": page,
    }
    # 设置headers头部信息
    headers = {
        "Accept": "application/json,text/plain,*/*",
        "Referer": "https://m.weibo.cn/p/index?containerid=2304131944603171_-_WEIBO_SECOND_PROFILE_WEIBO&luicode=10000011&lfid=2302831944603171",
        "User-Agent": random.choice(agents),
        "X-Requested-With": "XMLHttpRequest",
    }
    url = 'https://m.weibo.cn/api/container/getIndex?'
    #https: // m.weibo.cn / api / container / getIndex?containerid = 2304131944603171
    # _ - _WEIBO_SECOND_PROFILE_WEIBO & luicode = 10000011 & lfid = 2302831944603171 & page_type = 03 & page = 1
    try:
        response = requests.post(url, headers=headers, data=data)
        # 如果遭遇反爬，休息一分钟秒,然后重新开始爬取
        if response.status_code == 418:
            return response.status_code
        # 否则返回相应的数据
        else:
            return response.json()
    except Exception as e:
        print(e)

# 解析函数
def parse_data(data):
    # 得到每条微博的信息
    if data:
        items = data.get('data')['cards']

        for item in items:
            weibo = {}
            if item['card_type'] == 31:
                pass
            else:
                try:
                    # 获取正文链接
                    scheme = item.get('scheme')
                    item = item.get('mblog')
                    # 获取转发数
                    reposts_count = item.get('reposts_count')
                    # 获取评论数
                    comments_count = item.get('comments_count')
                    # 获取点赞数量
                    attitudes_count = item.get('attitudes_count')
                    # 获取播放量
                    online_users_number = item.get('page_info').get('media_info').get('online_users_number')
                    # 获取文字内容信息
                    text = item.get('page_info').get('content2').replace('\n', ',')
                    # 获取视频长度（以秒为单位）
                    duration = item.get('page_info').get('media_info').get('duration')

                    weibo = {
                        'reposts_count': reposts_count,
                        'comments_count': comments_count,
                        'attitudes_count': attitudes_count,
                        'online_users_number': online_users_number,
                        'text': text,
                        'duration': duration,
                        'scheme': scheme,
                    }

                    yield weibo

                except Exception as e:
                    pass
        #reposts_count = item.get('mblog').get('reposts_count')
        #print(reposts_count)

def write_data(data):
    line = list(data.values())
    print(line)
    weibo_info.append(line)
    weibo_data.save('weibo.xlsx')



def main():
    # 管理需要爬取的url
    for page in range(1, 140):
        data = get_page(page)
        while data == 418:
            time.sleep(60)
            data = get_page(page)
        result = parse_data(data)
        for re in result:
            write_data(re)
        time.sleep(1)

        # result = parse_data(data)


if __name__ == '__main__':
    weibo_data = Workbook()
    weibo_info = weibo_data.active
    weibo_info.append(['转发数量', '评论数', '点赞数', '播放', '文字', '视频长度(以秒为单位)', '正文链接'])
    main()