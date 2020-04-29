import requests
import base64
import traceback
import os
import io
import urllib
from PIL import Image
from io import BytesIO
from pyquery import PyQuery as pq
import ssl

# ssl._create_default_https_context = ssl._create_unverified_context
dic_l = {} # 所有要下载的url与分卷名
host = "https://www.manhuadb.com/"
save_path = "" # 保存的根目录
headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               "Cache-Control":"max-age=0",
               "Pramgma":"public",
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}


def saveImage(index, url, path):
    try:
        # response = requests.get(url,headers=headers, timeout=8)
        # image = Image.open(BytesIO(response.content))
        # image_name = f'{path}\{index}.jpg'
        # print(image_name)
        # image.save(image_name)
        # print(f"save:{image_name}")
        
        # req = urllib.request.Request(url, headers = headers)
        # with urllib.request.urlopen(req) as f:
        #     b = io.BytesIO(f.read())
        #     im = Image.open(b)
        #     im.save(f'{path}\{index}.jpg')
        # requests.packages.urllib3.disable_warnings()
        url = "https://i1.manhuadb.com/ccbaike/447/4937/10_qjzralyn.jpg"
        context = ssl._create_unverified_context()
        response = requests.get(url=url,headers=headers, verify=False, timeout=8)
        # with open(f'{path}\{index}.jpg', 'wb') as file:
        #     file.write(response.content)
        print(response.text)
        exit()
    # except ReadTimeoutError:
    #     down_image(index, url, path)
    except Exception as ex:
        traceback.print_exc()
        exit()
        # saveImage(index,url,path)

# 下载分卷中的所有页
def downPage(title, url):   
    total_page = getTotalPage( f"{url}_p1.html")
    p = f'.\{save_path}\{title}'
    createStorePath(p)
    for page in range(1, int(total_page) + 1):
        print(f"{url}_p{page}.html")
        link = getImagelink(f"{url}_p{page}.html")
        print(link)
        saveImage(page,link,p)


def getImagelink(url):
    resp = requests.get(url)
    doc = pq(resp.text)  # 解析html字符串
    return doc.find(".img-fluid").attr('src')

def getTotalPage(info_url):
    print(info_url)
    resp = requests.get(info_url)
    doc = pq(resp.text)
    breadcrumb = doc.find(".breadcrumb-item.active").text()
    temp = breadcrumb[breadcrumb.find('共'):]
    total_page = list(filter(str.isdigit,  temp))
    total_page = "".join(total_page)
    # title = doc.find(".breadcrumb-item.active a").text()
    return  total_page


# 生成需下载的页面
def downloadTask (url):
    resp = requests.get(url)
    html = resp.text
    doc = pq(html)  # 解析html字符串
    title = doc.find(".comic-title").text()
    global save_path
    save_path = f".\{title}"
    createStorePath(save_path)
    books = doc.find(".links-of-books.num_div a").items()
    for b in books:
        sub_title = b.attr('title')
        dic_l[sub_title] = host + b.attr('href')

def createStorePath(image_save_path):
    if not os.path.exists(image_save_path):
        os.makedirs(image_save_path)

def main(url):
    downloadTask(url)
    i = 0
    for title, url in dic_l.items():
        i+=1
        if i > 1:
            return
        downPage(title, url[0:-5])



if __name__ == "__main__":
    main("https://www.manhuadb.com/manhua/449")