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

#to obtain the url of each city
file_object = open('citylist2.txt')
list_all_city = file_object.readlines()
http = "https://en.wikipedia.org/wiki/"
for i in range(0,len(list_all_city)):
    list_all_city[i]=list_all_city[i].rstrip()
    list_all_city[i]=list_all_city[i].replace(' ','_')
    print(list_all_city[i])
    list_all_city[i]=http+list_all_city[i]
file_object.close()

#print(list_all_city)

# urls=list_all_city
# #urls=['https://en.wikipedia.org/wiki/Abbeville', 'https://en.wikipedia.org/wiki/Adamsville', 'https://en.wikipedia.org/wiki/Addison', 'https://en.wikipedia.org/wiki/Alabaster', 'https://en.wikipedia.org/wiki/Albertville', 'https://en.wikipedia.org/wiki/Alexander_City', 'https://en.wikipedia.org/wiki/Aliceville', 'https://en.wikipedia.org/wiki/Andalusia', 'https://en.wikipedia.org/wiki/Anniston', 'https://en.wikipedia.org/wiki/Arab', 'https://en.wikipedia.org/wiki/Ardmore', 'https://en.wikipedia.org/wiki/Argo', 'https://en.wikipedia.org/wiki/Ashford', 'https://en.wikipedia.org/wiki/Ashland', 'https://en.wikipedia.org/wiki/Ashville', 'https://en.wikipedia.org/wiki/Athens', 'https://en.wikipedia.org/wiki/Atmore', 'https://en.wikipedia.org/wiki/Attalla', 'https://en.wikipedia.org/wiki/Auburn', 'https://en.wikipedia.org/wiki/Bay_Minette', 'https://en.wikipedia.org/wiki/Bayou_La_Batre', 'https://en.wikipedia.org/wiki/Bessemer', 'https://en.wikipedia.org/wiki/Birmingham', 'https://en.wikipedia.org/wiki/Blountsville', 'https://en.wikipedia.org/wiki/Boaz', 'https://en.wikipedia.org/wiki/Brent', 'https://en.wikipedia.org/wiki/Brewton', 'https://en.wikipedia.org/wiki/Bridgeport', 'https://en.wikipedia.org/wiki/Brighton', 'https://en.wikipedia.org/wiki/Brookwood', 'https://en.wikipedia.org/wiki/Butler', 'https://en.wikipedia.org/wiki/Carbon_Hill', 'https://en.wikipedia.org/wiki/Carrollton', 'https://en.wikipedia.org/wiki/Cedar_Bluff']

# for line in urls:
#     url=line.strip()
#     landarea = getland_by_url(url)
#     print url.split('/')[-1],
#     print landarea
#     time.sleep(3)
