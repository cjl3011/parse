#!/usr/bin/env python
# coding=utf-8

import urllib
from bs4 import BeautifulSoup
url = 'http://tieba.baidu.com/p/3634581074'

# 下载网页
html = urllib.urlopen(url)
content = html.read()
html.close()

# 使用BeautifulSoup匹配图片
html_soup = BeautifulSoup(content)
all_img_links = html_soup.findAll('img', class_= 'BDE_Image')

# 下载图片
img_counter = 1
for img_link in all_img_links:
    img_name = '%s.jpg' % img_counter
    urllib.urlretrieve(img_link['src'], img_name)
    img_counter += 1

