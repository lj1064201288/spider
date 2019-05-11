'''
Url管理器
'''

class UrlManager(object):
    def __init__(self):
        self.new_url_list = set()
        self.old_url_list = set()

    # 添加一个url
    def add_url(self, url):
        if url != None:
            if url not in self.new_url_list and url not in self.old_url_list:
                self.new_url_list.add(url)
            else:
                print('这个链接已经爬取或者已经在将要爬取的列表中!')
        else:
            return

    # 添加一个url列表
    def add_urls(self, urls):
        if len(urls) > 0:
            for url in urls:
                if url not in self.new_url_list and url not in self.old_url_list:
                    self.new_url_list.add(url)
                else:
                    print('这个链接已经爬取或者已经在将要爬取的列表中!')
        if len(urls) == None:
            return

    # 获取一个url链接
    def get_url(self):
        if self.new_url_list != None:
            url = self.new_url_list.pop()
            self.old_url_list.add(url)
            return url
        else:
            return

    # 未使用的url链接数量
    def new_url_size(self):
        return len(self.new_url_list)

    # 已经使用过的链接数量
    def old_url_size(self):
        return len(self.old_url_list)