# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-11-24
"""
from argparse import ArgumentParser, Namespace

class AP:
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def parse_args() -> Namespace:
        parse = ArgumentParser()
        parse.add_argument("-t", "--type",
                           help="give a type of web | ex: 'unsplash / ptt / google picture'",
                           default="ptt", type=str)

        parse.add_argument("-u", "--url",
                           help="give a URL | ex: 'https://...'",
                           default="https://www.ptt.cc/bbs/Beauty/M.1702040877.A.239.html", type=str)

        parse.add_argument("-p", "--path",
                           help="give a path | ex: './img/'",
                           default="./Downloads/", type=str)

        return parse.parse_args()

    def config_once(self):
        args = AP.parse_args()
        self.obj.type = args.type
        self.obj.url = args.url
        self.obj.path = args.path