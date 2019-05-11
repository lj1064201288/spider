import random
import requests
import telnetlib
from bs4 import BeautifulSoup

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

agent = random.choice(agents)

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflateAccept-Language:zh-CN,zh;q=0.9Cache-Control:max-age=0",
    "Connection": "keep-alive",
    "Host": "www.xicidaili.com",
    "Upgrade-Insecure-Requests": '1',
    "User-Agent": agent
}

def get_proxys():

    base_url = "http://www.xicidaili.com/nn/"
    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            html = response.text
            return html
    except Exception as e:
        print(e)

def parse_proxys():
    content = get_proxys()
    try:
        soup = BeautifulSoup(content, features='lxml')
        trs = soup.select('tr')

        for tr in trs[1:]:
            if tr.select('td')[5].string == 'HTTPS':
                ip = tr.select('td')[1].string
                port = tr.select('td')[2].string
                yield ip, port

    except Exception as e:
        print(e.args)

# def write_proxy():
#     for proxy in parse_proxys():
#         true = test_ip(proxy)
#         if true:
#             print(proxy)
#             proxies.append(proxy)
#     return proxies

def test_ip():
    proxies = []
    for proxy in parse_proxys():
        try:
            tn = telnetlib.Telnet(proxy[0], port=proxy[1], timeout=3)
        except Exception as e:
            print("{0}:{1} 测试失败...".format(proxy[0], proxy[1],e.args))
        else:
            print('{0}:{1} 测试通过,可以使用...'.format(proxy[0], proxy[1]))
            proxie = proxy[0] + ":" + proxy[1]
            proxies.append(proxie)
    return proxies

#def proxys_list():
# proxies = test_ip()
# print(proxies)
# print(len(proxies))
    #proxys = write_proxy()
    #return proxys

#proxys1 = test_ip()
#for proxy in proxys1:
#    print(proxy)
