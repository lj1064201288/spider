'''
下载Html源码
'''
import requests


class HtmlDownload(object):
    # 下载网页
    def get_url(self, url):
        if url in None:
            return

        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                res.encoding = 'utf-8'
                return res.text

        except Exception as e:
            print('下载失败!', e.args)
