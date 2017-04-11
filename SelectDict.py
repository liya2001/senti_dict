#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import csv
import re

"""
分析词频统计结果，以扩充词典
比较词语在消极句子和积极句子中出现频率，尝试以此直接判断词性

这算是一种有监督的词典构建方法，实践未采用
"""


# 从csv文件中读取词语和出现次数，并转换为dict类型
def word2dict(filename, big=False):
    word_dict = {}
    with open(os.path.join(os.getcwd(), 'data', filename), 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # if big 这句写在外面会不会效率高一点
            if big:
                if int(row['Count']) > 4:
                    if re.findall(u'[^\d]+', row['Word']):
                        word_dict[row['Word']] = int(row['Count'])
            else:
                word_dict[row['Word']] = int(row['Count'])
    return word_dict


# 输出函数
def out2txt(word_list, filename):
    with open(os.path.join(os.getcwd(), 'data', filename), 'w') as f:
        for word in word_list:
            f.write(word+'\n')

review_dict = word2dict('ReviewDataCount.csv', True)
nega_dict = word2dict('NegaDataCount.csv')
posi_dict = word2dict('PosiDataCount.csv')

nega_words = []
posi_words = []
neutral_words = []
review_words = []

# 比较词频，如果在某一情感类型评论中出现次数显著高于另一种，则将词性设置为该类型
# 问题：准确率不够高，“过度学习”，很多中性词由于出现的偶然性被判断为极性情感词
for key, value in review_dict.items():
    nega_count = nega_dict.get(key, 0)
    posi_count = posi_dict.get(key, 0)
    polar = 0
    if nega_count > posi_count:
        if nega_count - posi_count > (nega_count + posi_count) / 4:
            polar = -1
            nega_words.append(key)
        else:
            neutral_words.append(key)
    if nega_count < posi_count:
        if posi_count - nega_count > (nega_count + posi_count) / 4:
            polar = 1
            posi_words.append(key)
        else:
            neutral_words.append(key)
    review_words.append((key, value, posi_count, nega_count, polar))

out2txt(nega_words, 'NegaWords.txt')
out2txt(posi_words, 'PosiWords.txt')
out2txt(neutral_words, 'NeutralWords.txt')

with open(os.path.join(os.getcwd(), 'data', 'ReviewWords.csv'), 'w', encoding='utf8', newline='') as f:
    headers = ['Word', 'Sum', 'Negative', 'Positive', 'Polar']
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(review_words)



