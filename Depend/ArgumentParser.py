# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-11-24
"""

from argparse import ArgumentParser, Namespace

class AP:
    def __init__(self, obj):
        self.obj = obj

    def parse_args(self) -> Namespace:
        parse = ArgumentParser()
        parse.add_argument("-t", "--type",
                           help="give a type of web | ex: 'unsplash / ptt / google picture'",
                           default="unsplash", type=str)

        parse.add_argument("-u", "--url",
                           help="give a URL | ex: 'https://...'",
                           default="https://unsplash.com/s/photos/japan", type=str)

        parse.add_argument("-p", "--path",
                           help="give a path | ex: './img/'",
                           default="./Downloads/", type=str)

        return parse.parse_args()

    def config_once(self):
        args = self.parse_args()
        self.obj.type = args.type
        self.obj.url = args.url
        self.obj.path = args.path