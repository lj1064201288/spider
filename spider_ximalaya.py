'''
爬取喜马拉雅音乐
url:https://www.ximalaya.com/yinyue/
'''

import requests, json
from urllib import request
from lxml import etree
from pypinyin import lazy_pinyin


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
# 获取歌单id
def get_albumId(music_type):
    '''
    接收要下载的音乐类型
    :param music_type:音乐类型
    :return: 歌单id
    '''
    url = 'https://www.ximalaya.com/yinyue/{}'.format(music_type)
    res = requests.get(url, headers=headers)
    # 找到albumId歌单的编号
    html = etree.HTML(res.text)
    albumIds = html.xpath('//a[@class="album-cover false lg needhover _sr"]/@href')
    return albumIds
# 获取歌单中的歌曲列表
def get_music_list(albumIds):
    '''
    对接收到的歌单id进行解析
    :param albumIds: 歌单id
    :return: 歌曲名称以及链接
    '''
    for albumId in albumIds:
        url = 'https://www.ximalaya.com/revision/play/album?albumId={}&pageNum=1&sort=-1&pageSize=30'.format(albumId.split('/')[-2])
        res = requests.get(url, headers=headers)
        json_music = json.loads(res.text)
        music_infos = json_music['data']['tracksAudioPlay']
        for music_info in music_infos:
            yield music_info['src'], music_info['trackName']
# 存储歌曲
def write_music(musics):
    '''
    接收歌曲名与链接
    :param musics:歌曲名与链接
    :return: None
    '''
    for music in musics:
        filename = 'C:/python/music/' + music[1] + '.mp3'
        try:
            print('正在下载{}...'.format(music[1]))
            request.urlretrieve(music[0], filename)
            print('{}下载完成...'.format(music[1]))
        except Exception as e:
            print('下载失败!!!' + '\n', e.args)

# 转换拼音
def fanyi(str):
    '''
    接收音乐类型转换成拼音
    :param str: 音乐类型
    :return: 拼音
    '''
    value = lazy_pinyin(str)
    str = ''.join(value)
    return str

if __name__ == '__main__':
    '''
    主函数:执行函数
    '''
    while True:
        type_song = input('Please input your music type(quit):')
        if type_song == 'quit':
            break
        music_type = fanyi(type_song)
        music_list = get_albumId(music_type)
        musics = get_music_list(music_list)
        write_music(musics)