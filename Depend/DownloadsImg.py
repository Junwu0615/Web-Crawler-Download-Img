# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-11-24
"""

import os
import requests
from requests import Response
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

class DownloadsImg:
    def __init__(self, obj):
        self.type = obj.type
        self.url = obj.url
        self.path = obj.path
        self.todo_list = []
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        self.cookies = '' if self.type == 'unsplash' else {'over18': '1'}
        check_f =  sorted([int(i.split('.jpg')[0]) for i in os.listdir(self.path)]) if os.path.exists(self.path) else []
        self.num = 0 if len(check_f) == 0 else check_f[-1]+1

    @staticmethod
    def progress_bar(task):
        match task:
            case "args":
                print("Get Parameter... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%")
            case "web_state":
                print("Web Responded Successfully... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%")
            case "Get_Downloads_List":
                print("Get Downloads List... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%")
            case "ThreadPoolExecutor":
                print("Download Multiple Images... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%")

    def check_folder(self, path: str):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)

    def get_source(self, url) -> Response:
        res = requests.get(url, headers=self.headers, cookies=self.cookies)
        if 100 <= res.status_code <= 199:
            print("Web State : Informational Responses !")
        elif 200 <= res.status_code <= 299:
            # print("Web State : Successful Responses !")
            pass
        elif 300 <= res.status_code <= 399:
            print("Web State : Redirects !")
        elif 400 <= res.status_code <= 499:
            print("Web State : Client Errors !")
        elif 500 <= res.status_code <= 599:
            print("Web State : Server Errors !")
        return res

    def create_img(self, src):
        res = self.get_source(src)
        f = open(f"{self.path}/{self.num}.jpg", "wb")
        f.write(res.content)
        f.close()
        self.num += 1

    def get_todo_list(self):
        res = self.get_source(self.url)
        soup = BeautifulSoup(res.text, "html.parser")
        self.progress_bar('web_state')
        if self.type == "unsplash":
            for div in soup.find_all('div', {'class', 'wdUrX'}):
                for tag in div.find_all('img'):
                    if tag['src'][:8] == "https://" and 'images.unsplash.com/photo' in tag['src']:
                        if tag['src'] not in self.todo_list:
                            self.todo_list.append(tag['src'])
        else:
            for img in soup.find_all("img"):
                if img['src'][:8] == "https://":
                    if img['src'] not in self.todo_list:
                        self.todo_list.append(img['src'])

    def create_executor(self):
        # 建立非同步的多執行緒的啟動器 # 同時下載圖片
        with ThreadPoolExecutor() as executor:
            ret = list(tqdm(executor.map(self.create_img, self.todo_list),total=len(self.todo_list)))

    def main(self):
        self.progress_bar('args')
        self.check_folder(self.path)
        self.get_todo_list()
        self.progress_bar("Get_Downloads_List")
        self.create_executor()
        self.progress_bar("ThreadPoolExecutor")