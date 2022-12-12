#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
import openpyxl
from fake_useragent import UserAgent

# 如果设置setenv("openfake")
useheaders = {}
useheaders.update({'User-Agent': UserAgent().random})
useProxy = ""

r = requests.get(
    url="https://www.baidu.com/",
    proxies=useProxy,
    headers=useheaders,
)

soup = BeautifulSoup(r.text, "lxml")

allImgs = [i.attrs["src"] for i in soup.find_all("img")]

print(allImgs)

wb = openpyxl.Workbook()
ws = wb.active
[ws.append([i]) for i in allImgs]
wb.save("123.xlsx")
