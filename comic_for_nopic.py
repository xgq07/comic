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

# ssl._create_default_https_context = ssl._create_unverified_context
dic_l = {} # 所有要下载的url与分卷名
host = "https://www.manhuadb.com/"
save_path = "Comics" # 保存的根目录
headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               "Cache-Control":"max-age=0",
               "Pramgma":"public",
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

def deletefile(f_needdpic, path):
    # if f_needdpic in ("./nopic/[爱生事家庭][浜冈贤次][玉皇朝][C.C]Vol_13.txt", 
    #                   "./nopic/[爱生事家庭][浜冈贤次][玉皇朝][C.C]Vol_14.txt"
    #                   "./nopic/[爱生事家庭][浜冈贤次][玉皇朝][C.C]Vol_15.txt"
    # ):
    #     return

    with open(f_needdpic,  'r') as f:
        for page in f:
            page = page[:-1]
            dele_file = f"{path}/{page}"
            if os.path.exists(dele_file):
                print("delete file", dele_file)
                os.remove(dele_file)

def main():
    pic_files = os.listdir("./NoPic")
    # for file in files:
    #     print(file)

    collector = []
    
    for root, dirs, files in os.walk("./Comics"):
        collector.extend(os.path.join(root, d) for d in dirs)
    
    # print(collector)
    for f in pic_files:
        for c in collector:
            if c.find(f[:-4]) >= 0:
                # print(c)
                # print(f"./nopic/{f}")
                deletefile(f"./nopic/{f}", c)



if __name__ == "__main__":
    main()
