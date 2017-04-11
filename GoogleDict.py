#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib.request
import random
from lxml import etree
import re
import csv
import time
import os


'''
基于互信息方法，将google可搜索到的中文网页作为语料库
统计潜在情感词+“手机”+“好”出现频率，和潜在情感词+“手机”+“差”出现频率
两相比较，依据规则判断该潜在情感词极性
实践中未采用，从少数几个词统计结果来看效果可能并不好
'''

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
               (KHTML, like Gecko) Element Browser 5.0',
               'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
               'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
               'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
               Version/6.0 Mobile/10A5355d Safari/8536.25',
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/28.0.1468.0 Safari/537.36',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']


def google_dict(key_words):

    time.sleep(60)
    url = 'https://www.google.com.hk/search?&hl=en&q=%s&*' % key_words.encode('utf8')
    req = urllib.request.Request(url)
    user_agent = user_agents[random.randint(0, 9)]
    req.add_header('User-agent', user_agent)
    response = urllib.request.urlopen(req, timeout=30)

    page = etree.parse(response, parser=etree.HTMLParser())
    result = page.xpath('//*[@id="resultStats"]/text()')
    key_value = page.xpath('//*[@id="sbhost"]/@value')
    # print(result)
    # print(key_value)
    num_list = re.findall('\d+', result[0])
    num = ''.join(num_list)
    print(num)
    return int(num)

def judge_polar(word):
    key_words_good = word+'手机'+'好'
    key_words_bad = word+'手机'+'差'
    good_num = google_dict(urllib.parse.quote(key_words_good))
    bad_num = google_dict(urllib.parse.quote(key_words_bad))
    if good_num > 2*bad_num:
        polar = 1
    elif bad_num > 2*good_num:
        polar = -1
    else:
        polar = 0
    return good_num, bad_num, polar


if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'data', 'WordUndefined.csv'), 'r', encoding='utf8') as in_f:
        with open(os.path.join(os.getcwd(), 'data', 'GoogleDefineDict.csv'), 'w', encoding='utf8', newline='') as out_f:
            headers = ['Word', 'Good_num', 'Bad_num', 'Polar']
            out_f_csv = csv.writer(out_f)
            out_f_csv.writerow(headers)
            reader = csv.DictReader(in_f)
            for row in reader:
                print(row['Word'])
                good_num, bad_num, polar = judge_polar(row['Word'])
                out_f_csv.writerow([row['Word'], good_num, bad_num, polar])