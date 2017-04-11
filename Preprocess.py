#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文本预处理的一些工具
"""

import jieba
import codecs
import re
import os

stopwords = {u'的', u'地', u'得', u'了', u'在', u'是', u'我', u'有', u'和',
             u'就', u'人', u'都', u'一', u'一个', u'也', u'很', u'到', u'说', u'要',
             u'去', u'你', u'会', u'着', u'看', u'自己', u'这'}
# u'不', u'好', u'没有', u'而', u'上',


class TextPreprocessUtility(object):
    """A utility class for processing raw HTML text"""

    """
    分词
    """

    @staticmethod
    def sentence2words(sentence, remove_stopwords=False):
        """
        Segment a sentence to words
        """
        assert isinstance(sentence, str)
        seg_list = list(jieba.cut(sentence))
        if remove_stopwords:
            stops = set(stopwords)
            seg_list = [w for w in seg_list if w not in stops]
        # Return a list of words
        return seg_list

    """
    分句
    """

    @staticmethod
    def review2sentences(review):
        """
        Segment a long sentence to short sentence
        """
        sentences = []
        try:
            new_sent = re.sub(u'[！|,|，|。|...|？|?|!|；|~|～|。||▽|“|"|【|】|;|^|(&hellip;)|:|\'|\\|●|￣|+|．| \
            *|@|(/:strong)|-|——|{|}|、|↖|：：]+', u' ', review)
            for s in new_sent.split():
                if re.findall(u'[^a-zA-Z\d]+', s):
                    sentences.append(s)
        except UnicodeDecodeError:
            print('Decode Error')
        return sentences


if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'data', 'word2vecClean.csv'), 'r', encoding="utf8") as in_file:
        with open(os.path.join(os.getcwd(), 'data', 'split_word2vec.csv'), 'w', encoding="utf8") as out_file:
            # 考虑编码错误
            line = in_file.readline()
            reviews = set()
            while line:
                reviews.add(line)
                try:
                    line = in_file.readline()
                except UnicodeDecodeError:
                    print('Decode Error')
            # reviews = in_file.readlines()
            # reviews = set(reviews)
            sentences = []
            for review in reviews:
                sentences += TextPreprocessUtility.review2sentences(review)
            sentences = set(sentences)
            for sentence in sentences:
                words_list = TextPreprocessUtility.sentence2words(sentence)
                words = ' '.join(words_list)
                out_file.write(words+'\n')
