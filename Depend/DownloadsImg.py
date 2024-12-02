# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-01
"""
from tqdm import tqdm
import os, copy, requests
from bs4 import BeautifulSoup
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor, wait

class DownloadsImg:
    def __init__(self, obj):
        self.type = obj.type
        self.url = obj.url
        self.path = obj.path
        self.console = Console()
        self.todo_list = []
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
        self.cookies = '' if self.type == 'unsplash' else {'over18': '1'}
        check_list =  sorted([int(i.split('.jpg')[0]) for i in os.listdir(self.path)]) if os.path.exists(self.path) else []
        self.num = 0 if len(check_list) == 0 else check_list[-1]+1

    @staticmethod
    def check_folder(path: str):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)

    def get_source(self, url, headers, cookies) -> requests.Response:
        res = requests.get(url, headers=headers, cookies=cookies)
        state = res.status_code
        if 100 <= state <= 199:
            self.console.print(f"{state} : Informational Responses !")
        elif 200 <= state <= 299:
            # self.console.print(f"{state} : Successful Responses !")
            pass
        elif 300 <= state <= 399:
            self.console.print(f"{state} : Redirects !")
        elif 400 <= state <= 499:
            self.console.print(f"{state} : Client Errors !")
        elif 500 <= state <= 599:
            self.console.print(f"{state} : Server Errors !")

        return res

    def progress_bar(self, task):
        symbol = '━'
        match task:
            case "args":
                self.console.print(f"Get Parameter... {symbol * 46} 100%")
            case "Get_Downloads_List":
                self.console.print(f"Get Downloads List... {symbol * 41} 100%")
            case "ThreadPoolExecutor":
                self.console.print(f"ThreadPoolExecutor Done !")

    def create_img(self, url, headers, cookies) -> int:
        ret = -1
        try:
            res = self.get_source(url, headers, cookies)
            f = open(f"{self.path}/{self.num}.jpg", "wb")
            f.write(res.content)
            f.close()
            self.num += 1
            ret = 0
        except IOError as e:
            print(e)
        finally:
            return ret

    def get_todo_list(self):
        res = self.get_source(self.url, self.headers, self.cookies)
        soup = BeautifulSoup(res.text, "html.parser")
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
        # FIXME 建立非同步的多執行緒的啟動器 -> 同時下載圖片
        max_workers = 5
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            new_task = {}
            task = {executor.submit(self.create_img, url, self.headers, self.cookies):
                        (url, self.headers, self.cookies) for url in self.todo_list}

            schedule = tqdm(total=len(task), desc='Downloads Schedule: ')
            while len(task) > 0:
                callback, _ = wait(task, return_when='FIRST_COMPLETED')
                if callback != set():
                    for future in callback:
                        job = task[future]
                        del task[future]
                        if future.result() in [0]:
                            schedule.update(1)
                        else:
                            new_task[future] = job  # 先儲存[再submit需求]

                if len(task) == 0:
                    for future, job in new_task.items():
                        task[executor.submit(self.create_img, job[0], job[1], job[2])] = job
                    new_task = {}

    def main(self):
        DownloadsImg.check_folder(self.path)
        self.progress_bar('args')
        self.get_todo_list()
        self.progress_bar("Get_Downloads_List")
        self.create_executor()
        self.progress_bar("ThreadPoolExecutor")