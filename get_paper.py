# coding=utf-8
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import traceback
import re
import os

prefix = 'http://openaccess.thecvf.com/'
save_dir = 'ECCV2018'

def get_pdf(data):
    href, title = data
    name = re.sub(r'[\\/:*?"<>|]', ' ', title)
    if os.path.isfile("eccv2018/eccv18-%s.pdf" % name):
        print("File already exsists, skip %s" % name)
        return
    try:
        content = requests.get(prefix+href).content
        with open(save_dir+"/eccv18-%s.pdf" % name, 'wb') as f:  # You may change to "path/to/your/folder"
            f.write(content)
        print("Finish downloading %s" % title)
    except:
        print('Error when downloading %s' % href)
        print(traceback.format_exc())
        
pool = Pool(10)
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
html = requests.get(prefix+'/ECCV2018.py').content
soup = BeautifulSoup(html, "lxml")
a_list = soup.findAll('a')
title_list = soup.findAll("dt", {"class": "ptitle"})
title_list = [_.text for _ in title_list]
pdf_list = []
for everya in a_list:
    if everya.text.strip() == "pdf":
        href = everya.get("href").strip()
        pdf_list.append(href)
assert len(pdf_list) == len(title_list), "numbers of title and pdf not euqal"
print("Find %d papers" % len(pdf_list))
pool.map(get_pdf, zip(pdf_list, title_list))
