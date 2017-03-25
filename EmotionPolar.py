#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

'''
导入HowNet情感词典，暂不考虑程度副词
'''
NegativeWordsFile = open(os.path.join(os.getcwd(), 'dict', 'HowNet', 'NegativeWords.txt'), 'r')
NegativeEmotionFile = open(os.path.join(os.getcwd(), 'dict', 'HowNet', 'NegativeEmotion.txt'), 'r')
NegativeCommentaryFile = open(os.path.join(os.getcwd(), 'dict', 'HowNet', 'NegativeCommentary.txt'), 'r')
PositiveEmotionFile = open(os.path.join(os.getcwd(), 'dict', 'HowNet', 'PositiveEmotion.txt'), 'r')
PositiveCommentaryFile = open(os.path.join(os.getcwd(), 'dict', 'HowNet', 'PositiveCommentary.txt'), 'r')

# 在集合中查找更快
NegativeWords = set(NegativeWordsFile.readline().split())
NegativeEmotion = set(NegativeEmotionFile.readline().split())
NegativeCommentary = set(NegativeCommentaryFile.readline().split())
PositiveEmotion = set(PositiveEmotionFile.readline().split())
PositiveCommentary = set(PositiveCommentaryFile.readline().split())

# 合并情感词和评价词
NegativeEmotion = NegativeEmotion | NegativeCommentary
PositiveEmotion = PositiveEmotion | PositiveCommentary

print(len(PositiveEmotion))
print(len(NegativeEmotion))

# 计算情感值
def ScoreSent(sentence):
    score = 0
    for word in sentence.split():
        if word in PositiveEmotion:
            score += 1
        if word in NegativeEmotion:
            score -= 1
        if word in NegativeWords:
            score *= -1
    return score

NegaDataFile = open(os.path.join(os.getcwd(), 'data', 'NegativeShortSentence.csv'), 'r', encoding='utf8')
PosiDataFile = open(os.path.join(os.getcwd(), 'data', 'PositiveShortSentence.csv'), 'r', encoding='utf8')

NegaData = NegaDataFile.readlines()
PosiData = PosiDataFile.readlines()

PosiNum = len(PosiData)
NegaNum = len(NegaData)

print('PosiNum:', PosiNum)
print('NegaNum:', NegaNum)


TP, FP, TN, FN = 0, 0, 0, 0
N_not_included = 0
P_not_included = 0

# 判断极性
for sentence in NegaData:
    score = ScoreSent(sentence)
    if score > 0:
        FP += 1
    if score == 0:
        N_not_included +=1
    if score < 0:
        TN += 1

for sentence in PosiData:
    score = ScoreSent(sentence)
    if score > 0:
        TP += 1
    if score == 0:
        P_not_included += 1
    if score < 0:
        FN += 1

print('P_not_included:', P_not_included)
print('N_not_included:', N_not_included)

not_included = N_not_included + P_not_included
print('not_included:', not_included)

# 结果展示
print('TP:', TP)
print('FP:', FP)
print('TN:', TN)
print('FN:', FN)

precision = (TP+1)/(TP+FP+1)
recall = (TP+1)/(TP+FN+1)
print('precision:', precision)
print('recall:', recall)

F = precision*recall*2/(precision+recall)
print('F:', F)