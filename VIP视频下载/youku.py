import requests
from multiprocessing import Pool

'''
先在网站上得到视频的播放地址，然后将url地址复制到解析网站进行解析，查看newwork里面的请求，获取到相关的片段视频，然后进行拼接下载！
'''

# URL: https://baidu.com-l-baidu.com/20190809/14558_2176c576/1000k/hls/61e73f03a93001255.ts

def demo(page):
    # 解析到每个视频片段的url
    url = 'https://baidu.com-l-baidu.com/20190809/14558_2176c576/1000k/hls/61e73f03a93%06d.ts'%(page)
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    # 对网站进行请求
    response = requests.get(url, headers=headers)
    with open('../video/{}'.format(url[-8:]), 'ab+') as file:
        print('开始下载:{}'.format(url))
        file.write(response.content)

if __name__ == '__main__':
    pool = Pool(20)

    for page in range(1255):
        pool.apply_async(demo, (page, ))
    pool.close()
    pool.join()
