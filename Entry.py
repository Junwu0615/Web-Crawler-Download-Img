# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-11-24
"""
from package.DownloadsImg import DownloadsImg
from package.ArgumentParser import AP

class Entry:
    def __init__(self):
        self.type = None
        self.url = None
        self.path = None

    def main(self):
        ap = AP(self)
        ap.config_once()
        di = DownloadsImg(self)
        di.main()

if __name__ == '__main__':
    entry = Entry()
    entry.main()