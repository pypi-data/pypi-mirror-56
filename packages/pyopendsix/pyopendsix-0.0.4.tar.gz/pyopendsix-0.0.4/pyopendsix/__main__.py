#!/usr/env/python
# coding: utf-8

"""
OpenD6 Flask API
"""

from . import define_api

if __name__ == '__main__':
    API = define_api()
    API.run(host="0.0.0.0", port=6000)
