'''
下载bilibili的视频
URL:https://search.bilibili.com/all?keyword=%E8%A7%86%E9%A2%91&from_source=banner_search
下载连接:

'''
import requests, os
from tkinter import *
from lxml import etree

# 视频列表页面
def getdecode(key, page):
    data = {
        'keyword': key,
        'page': str(page)
    }
    url = 'https://api.bilibili.com/x/web-interface/search/type?jsonp=jsonp&search_type=video&highlight=1'
    res = requests.get(url, params=data)
    parse_bilibili(res.json())

# 解析网页数据
def parse_bilibili(html):
    datas = []
    items = html['data']['result']
    for item in items:
        arcurl = item['arcurl']
        title = item['tag']
        datas.append([arcurl, title])
    down_video(datas)
# 使用you-get进行视频下载
def down_video(datas):
    for data in datas:
        path = '../datas/videos/' + data[1]
        if not os.path.exists(path):
            os.makedirs(path)
        print('正在下载{}'.format(data[1]))
        #list_1.insert(END, '正在下载{}'.format(title))
        os.system('you-get -i {} {} --debug'.format(path, data[0]))
        #list_1.see(END)
        # list_1.update()
# 主函数
def main():
    # 得到输出框entry_1的内容
    key = input('Plase input type:')
    page = int(input('Plase input page:'))
    # key = entry_1.get()
    # 得到输出框entry_2的内容
    # page = int(entry_2.get())
    for i in range(1, page+1):
        getdecode(key, i)

if __name__ == '__main__':
    main()
    # 图形界面
    root = Tk()
    # 设置标题
    root.title('bilibili视频下载')
    # 设置窗口大小
    root.geometry('690x500')
    # 设置窗口位置
    root.geometry('+400+180')
    # 提示语
    labal_1 = Label(root, text='请输入你要下载的视频类型:', font=('楷体', '15'), width=30)
    labal_2 = Label(root, text='请输入你要下载的页数:', font=('楷体', '15'), width=30)
    # 输入框
    entry_1 = Entry(root, font=('仿宋', '15'), width=30)
    entry_2 = Entry(root, font=('仿宋', '15'), width=30)
    # 设置按钮
    button_1 = Button(root, text='搜索', font=('楷体', '15'), background='red', command=main)
    # 显示窗口
    list_1 = Listbox(root, font=('仿宋', 8), width=110, height=30)
    # 封装
    labal_1.config(fg='red')
    labal_1.grid(row=0, column=0)
    labal_2.config(fg='red')
    labal_2.grid(row=1, column=0)
    entry_1.grid(row=0, column=1)
    entry_2.grid(row=1,column=1)
    button_1.config(fg='white')
    button_1.grid(row=1, column=2)
    list_1.grid(row=2, columnspan=3)
    root.mainloop()



