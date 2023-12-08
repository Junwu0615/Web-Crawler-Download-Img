import os
import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

#參數
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/111.25 (KHTML, like Gecko) Chrome/99.0.2345.81 Safari/123.36"}
cookies = {'over18':'1'}
num = 0

#檢查網址狀況
def web_state(url):
    res = requests.get(url, headers=headers, cookies=cookies)
    
    if 100 <= res.status_code <= 199:
        print ("Web State : Informational Responses !")
    elif 200 <= res.status_code <= 299:
        print ("Web State : Successful Responses !")
    elif 300 <= res.status_code <= 399:
        print ("Web State : Redirects !")
    elif 400 <= res.status_code <= 499:
        print ("Web State : Client Errors !")
    elif 500 <= res.status_code <= 599:
        print ("Web State : Server Errors !")
        
#下載圖片
def download(src):
    global path
    global num
    num += 1
    name = args.url.split("/")[::-1][0] + str(num)
    jpg = requests.get(src)    #取得圖片內容
    f = open(f"{path}/{name}.jpg", "wb")    #使用二進位方式開啟圖片準備寫入
    f.write(jpg.content)       #存入圖片
    f.close()
    
#判斷是否有資料夾
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        progress_bar("Folder_Created_Successfully")
    else:
        progress_bar("Confirmed_That_The_Folder_Exists")
        
def parse_args():
    parse = ArgumentParser()
    parse.add_argument("-t", "--type", help = "give a type of web | ex: 'unsplash / ptt / google picture'", default = "type", type = str)
    parse.add_argument("-u", "--url", help = "give a URL | ex: 'https://...'", default = "url", type = str)
    parse.add_argument("-p", "--path", help = "give a path | ex: './img/'", default = "path", type = str)
    args = parse.parse_args() #解析參數對象 獲得解析對象
    return args


def download_img(typE, url, path):
    web = requests.get(url, headers = headers, cookies = cookies) 
    soup = BeautifulSoup(web.text, "html.parser") 
    img_list = []
    if typE == "unsplash":
        tags = soup.find_all("img", {"class": 'tB6UZ a5VGX'})
        for tag in tags:
            if tag['src'][:8] != "https://":
                pass
            else:
                img_list.append(tag['src'])
    
    else:
        tags = soup.find_all("img")
        for tag in tags:
            if tag['src'][:8] != "https://":
                pass
            else:
                img_list.append(tag['src'])
               
    progress_bar("Get_Downloads_List")
    
    #開始下載
    mkdir(path)
    executor = ThreadPoolExecutor() #建立非同步的多執行緒的啟動器
    with ThreadPoolExecutor() as executor:
        executor.map(download, img_list) #同時下載圖片
    progress_bar("ThreadPoolExecutor")
    
def progress_bar (task):
    match task: 
        case "args":
            print("Get Parameter... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%")
            
        case "web_state":
            print("Web Responded Successfully... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%")
            
        case "Get_Downloads_List":
            print("Get Downloads List... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%")
               
        case "ThreadPoolExecutor":
            print("Download Multiple Images... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%")
            
        case "Folder_Created_Successfully":
            print("Folder Created Successfully.")
            
        case "Confirmed_That_The_Folder_Exists":
            print("Confirmed That The Folder Exists.")
    
    
if __name__ == "__main__":
    args = parse_args()
    progress_bar("args")
    web_state(args.url)
    progress_bar("web_state")
    path = args.path
    download_img(args.type, args.url, args.path)
    