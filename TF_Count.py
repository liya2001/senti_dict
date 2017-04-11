#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
统计词频
"""
import os
import csv
import codecs
from collections import Counter, OrderedDict


def count_words(file_name):
    word_counter = Counter()
    stopwords = [u'的', u'地', u'得', u'了', u'在', u'是', u'我', u'有', u'和', u'他', u'她',
                 u'就', u'人', u'都', u'一', u'一个', u'也', u'很', u'到', u'说', u'要', u'它',
                 u'去', u'你', u'会', u'着', u'看', u'自己', u'这']
    # u'不', u'好', u'没有', u'而', u'上',
    # stopwords = []
    stopwords = set(stopwords)

    file = open(os.path.join(os.getcwd(), 'data', file_name), 'r', encoding='utf8')
    for line in file:
        for word in line.split():
            # 忽略停用词
            if word in stopwords:
                continue
            # 用词典存储出现次数
            elif word in word_counter:
                word_counter[word] += 1
            else:
                word_counter[word] = 1

    print(word_counter.most_common(20))
    return word_counter


def out2csv(word_counter, file_name):
    headers = ['Word', 'Count']
    word_dict = dict(word_counter)
    with open(os.path.join(os.getcwd(), 'data', file_name), 'w', encoding='utf8', newline='') as f:

        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for key, count in word_counter.most_common():
            f_csv.writerow([key, count])


if __name__ == '__main__':
    ReviewCounter = count_words('split_word2vec.csv')

    out2csv(ReviewCounter, 'ReviewCountNoStopWords.csv')
    # NegaDataCounter = count_words('NegativeShortSentence.csv')
    # PosiDataCounter = count_words('PositiveShortSentence.csv')
    # ReviewDataCounter = NegaDataCounter + PosiDataCounter

    # out2csv(NegaDataCounter, 'NegaDataCount.csv')
    # out2csv(PosiDataCounter, 'PosiDataCount.csv')
    # out2csv(ReviewDataCounter, 'ReviewDataCount.csv')
