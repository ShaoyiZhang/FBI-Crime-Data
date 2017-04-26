import requests
import lxml.etree as etree
import time

def strip_detail(txt_list):
    new_txt = []
    for txt in txt_list:
        if txt.strip() != "":
            new_txt.append(txt.strip())
    return new_txt


def getland_by_url(url):
    headers={
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, sdch',
        'accept-language':'zh-CN,zh;q=0.8',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER',
    }

    html = requests.get(url,headers=headers).content
    root = etree.HTML(html)
    all_tr = root.xpath('//tr[@class="mergedrow"]')
    for tr in all_tr:
        label =  ''.join(strip_detail(tr.xpath('./th//text()')))
        if label.find('Land')!=-1:
            value = ' '.join(strip_detail(tr.xpath('./td//text()')))
            return value


urls=['https://en.wikipedia.org/wiki/Los_Angeles',
      'https://en.wikipedia.org/wiki/San_Francisco',
      'https://en.wikipedia.org/wiki/San_Diego',
      'https://en.wikipedia.org/wiki/Santa_Barbara,_California']

for line in urls:
    url=line.strip()
    landarea = getland_by_url(url)
    print url.split('/')[-1],
    print landarea
    time.sleep(3)
