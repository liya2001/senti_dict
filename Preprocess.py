#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba
import codecs
import  re

"""
分词
"""


def sent2word(sentence):
    """
    Segment a sentence to words
    """
    assert isinstance(sentence, str)
    seg_list = jieba.cut(sentence)
    seg_result = []
    for w in seg_list:
        seg_result.append(w)
        
    new_sent = ' '.join(seg_result)
    return new_sent

"""
分句
"""


def sentence_split(sentence):
    """
    Segment a long sentence to short sentence
    """
    sentences = []
    try:
        #sentence = sentence.decode('utf-8')
        new_sent = re.sub(u"[！|,|，|。|...|？|?|!|；|~|～|。||▽|“|\"|【|】|;|^|(&hellip;)|:|'|\\|●|￣|+|．| \
        *|@|(/:strong)|-|一|{|}|、|↖|：：]+", u' ', sentence)
        for s in new_sent.split():
            if re.findall(u'[^a-zA-Z\d]+', s):
                sentences.append(s)
    except UnicodeDecodeError:
        print('Decode Error')
    return sentences

r_file = open(r'newhonor7.csv', 'r', encoding="utf8")
w_file = open(r'split_honor7.csv', 'w', encoding="utf8")

line = r_file.readline()
tmpset = set()
while line:
    tmpset.add(line)
    try:
        line = r_file.readline()
    except UnicodeDecodeError:
        print('Decode Error')

r_file.close()
"""
去重
"""
sentences = []
for line in tmpset:
    sentences += sentence_split(line)

sentences = set(sentences)

for sentence in sentences:
    s = sent2word(sentence)
    try:
        w_file.write(s+'\n')
    except UnicodeEncodeError:
        print('Encode Error')
w_file.close()
