# -*- coding: utf-8 -*-

import datetime
import json

__author__ = 'sobolevn'
__author__ = 'alex-px'


class Storage(object):
    items = None
    _obj = None
    JSON_FILE = 'data.json'

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._obj is None:
            cls._obj = object.__new__(cls)
            try:
                with open(cls.JSON_FILE, 'r+') as fh:
                    cls.items = json.load(fh)
            except (IOError, FileNotFoundError):
                cls.items = []
        return cls._obj

    @classmethod
    def append(cls, item):
        def default(obj):
            if hasattr(obj, '__json__'):
                return obj.__json__()
            return json.JSONEncoder.default(obj)
        cls.items.append(item)
        with open(cls.JSON_FILE, 'w+') as fh:
            json.dump(cls.items, fh, default=default)


class BlogPostModel(object):
    def __init__(self, form_data):
        self.title = form_data['title']
        self.text = form_data['text']
        self.time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.author = form_data['author']

    def __json__(self):
        return {'title': self.title,
                'text': self.text,
                'time_stamp': self.time_stamp,
                'author': self.author}
