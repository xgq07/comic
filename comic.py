import requests
import base64
import traceback
import os
import io
import shutil
from PIL import Image
from io import BytesIO
from pyquery import PyQuery as pq
import concurrent.futures
import threading
from fake_useragent import UserAgent

# ssl._create_default_https_context = ssl._create_unverified_context
dic_l = {} # 所有要下载的url与分卷名
host = "https://www.manhuadb.com/"
save_path = "Comics" # 保存的根目录
ua = UserAgent()
headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               "Cache-Control":"max-age=0",
               "Pramgma":"public",
               'User-Agent': ua.random}
# session = requests.Session()

def saveImage(index, url, path, book_title):
    i = 0
    while i < 3: 
        try:
            response = requests.get(url, headers=headers, timeout=10)
            image = Image.open(BytesIO(response.content))
            # image_name = f'{path}\{index}.jpg'
            image_name = os.path.join(path,index+ ".jpg")
            image.save(image_name)
            print(f"save:{image_name}")
            break
            # req = urllib.request.Request(url, headers = headers)
            # with urllib.request.urlopen(req) as f:
            #     b = io.BytesIO(f.read())
            #     im = Image.open(b)
            #     im.save(f'{path}\{index}.jpg')
            # requests.packages.urllib3.disable_warnings()

            # url = "https://i1.manhuadb.com/ccbaike/447/4937/10_qjzralyn.jpg"
            # context = ssl._create_unverified_context()
            # response = requests.get(url=url, headers=headers, timeout=8)
            # with open(f'{path}\{index}.jpg', 'wb') as file:
            #     file.write(response.content)
            # print(response.text
        # except ReadTimeoutError:
        #     down_image(index, url, path)
        except IOError as e:
            i += 1
            print("image ioerror : ", image_name, book_title)
            saveImage(index, url, path, book_title)
            # if i >= 3:
            #     image_name = f'{path}\{index}.jpg'
            #     writeToFile(f"./NoPic/{book_title}.txt", f"{index}.jpg\n")
            #     shutil.copy("./Nopic/nopic.jpg", image_name)
            # break
        except Exception as ex:
            i += 1
            print(ex)
            saveImage(index, url, path, book_title)

# 下载分卷中的所有页
def downPage(title, url):
    doc = getResponse(f"{url}_p1.html")
    total_page = getTotalPage(doc)
    p = os.path.join(save_path,title)
    createStorePath(p)
    down_page_args = getDownPageTask(p, total_page, url, title)
    print("need to down: " + str(len(down_page_args)))
    if len(down_page_args) == 0:
        return
    print(down_page_args[0])
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(downForThread, down_page_args)

    # with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
    #     executor.map(downForThread, down_page_args)


def downForThread(args):
    url, page, p , book_title = args[0], args[1], args[2], args[3]
    print(f"{url}_p{page}.html")
    link = getImagelink(f"{url}_p{page}.html")
    print(link)
    saveImage(page, link, p, book_title)



# 取得已下载的页面数量
def getDownPageCount(path):
    files = os.listdir(path)
    return len(files)


# take the second element for sort
def take_second(elem):
    # print(elem[1])
    return int(elem[1])


# 取得需下载的页面与图片url
def getDownPageTask(path, total_page, url, book_title):
    args = []
    files = os.listdir(path)
    p_all = set([str(i)+'.jpg' for i in range(1, int(total_page) + 1)])
    p_files = set(files) 
    p_neet_down = p_all - p_files
 
    for page in p_neet_down:
        arg = (url, page[:page.find(".")], path, book_title)
        args.append(arg)      

    # sort list with key
    args_sort = sorted(args, key=take_second)

    return args_sort


# 取得要图片src
def getImagelink(url):
    return getResponse(url).find(".img-fluid").attr('src')

# 取得页数
def getTotalPage(doc):
    breadcrumb = doc.find(".breadcrumb-item.active").text()
    temp = breadcrumb[breadcrumb.find('共'):]
    total_page = list(filter(str.isdigit,  temp))
    total_page = "".join(total_page)
    return  total_page


# 生成需下载的页面到dic_l中
def downloadTask(url):
    doc = getResponse(url)
    title = doc.find(".comic-title").text()
    global save_path
    save_path = "Comics"  # 保存的根目录
    save_path = os.path.join(save_path, title)
    createStorePath(save_path)
    books = doc.find(".links-of-books.num_div a").items()
    for b in books:
        sub_title = b.attr('title')
        if isDownloaded(doc, os.path.join(save_path,sub_title)):
            continue
        dic_l[sub_title] = host + b.attr('href')

# 检查是否已经完整下载过此分卷
def isDownloaded(doc, path):
    if not os.path.exists(path):
        return False

    total_page = getTotalPage(doc)
    downloaded_total_page = getDownPageCount(path)
    if total_page != downloaded_total_page:
        return False
    else:
        return True

def getResponse(url):
    resp = requests.get(url=url, headers=headers, timeout=10)
    html = resp.text
    doc = pq(html)  # 解析html字符串
    return doc

def createStorePath(image_save_path):
    if not os.path.exists(image_save_path):
        os.makedirs(image_save_path)

def writeToFile(path, content):
    with open(path, "a") as f:
        f.write(content)

def main(url):
    dic_l.clear()
    downloadTask(url)
    for title, url in dic_l.items():
        downPage(title, url[0:-5])



if __name__ == "__main__":
    # main("https://www.manhuadb.com/manhua/4405")
    # main("https://www.manhuadb.com/manhua/6566")
    # main("https://www.manhuadb.com/manhua/7217")
    # main("https://www.manhuadb.com/manhua/7122")
    # main("https://www.manhuadb.com/manhua/7065")
    
    
    
    
    
    # r = requests.get("https://www.baidu.com")
    # print(r)
