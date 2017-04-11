#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
判断并统计评论情感极性
"""

import os
import codecs
import csv
import logging


'''
导入情感词典
'''
from Dictionaries import EmotionDict, DegreeDict, NegativeDict, BosonDict, ExtSeedValueDict, ExtMostValueDict,\
    ExtMostSimilar, ExtSimilarity, Word2vecDict


print('EmotionDict:', len(EmotionDict))
print('NegativeDict:', len(NegativeDict))
print('DegreeDict:', len(DegreeDict))
print('BosonDict:', len(BosonDict))
print('ExtSeedValueDict:', len(ExtSeedValueDict))
print('ExtMostValueDict:', len(ExtMostValueDict))
print('ExtMostSimilar:', len(ExtMostSimilar))
print('ExtSimilarity:', len(ExtSimilarity))
print('Word2vecDict:', len(Word2vecDict))
# ExtEmotionDict = {**EmotionDict, **ExtMostSimilar}
# print('ExtValueDict:', len(ExtValueDict))


# 计算情感词组情感值
def score_senti_group(senti_group, emotion_dict):

    group_score = 0.0
    for i in range(len(senti_group)-1, -1, -1):
        if senti_group[i] in emotion_dict:
            group_score += emotion_dict[senti_group[i]]
        elif senti_group[i] in NegativeDict:
            # 如果程度副词在否定词之后，如“不很好”，情感变为情感正面，否定词系数变为正0.2
            if senti_group[i+1] in DegreeDict:
                group_score *= 0.2
            else:
                group_score *= -1.0
        elif senti_group[i] in DegreeDict:
            group_score *= DegreeDict[senti_group[i]]
    return group_score


# logging
def log_score_review(review, emotion_dict, rules=True):
    logging.info(review)
    review_list = review.split()
    last_senti_word_position = 0
    review_score = 0
    for i in range(len(review_list)):
        if review_list[i] in emotion_dict.keys():
            # logging 显示每个评论得分，及评论的每个情感词组得分
            logging.info(review_list[i])
            if rules == True:
                senti_group_score = score_senti_group(review_list[last_senti_word_position:i+1], emotion_dict)
            else:
                senti_group_score = emotion_dict[review_list[i]]
            logging.info(review_list[last_senti_word_position:i+1])
            logging.info('senti_group_score: '+str(senti_group_score))
            review_score += senti_group_score
            last_senti_word_position = i + 1
    logging.info('review_score: '+str(review_score)+'\n')
    return review_score


# 计算评论情感值
# 线性叠加情感词组情感值
def score_review(review, emotion_dict, rules=True):

    review_list = review.split()
    last_senti_word_position = 0
    review_score = 0
    for i in range(len(review_list)):
        if review_list[i] in emotion_dict.keys():
            if rules == True:
                senti_group_score = score_senti_group(review_list[last_senti_word_position:i+1], emotion_dict)
            else:
                senti_group_score = emotion_dict[review_list[i]]
            review_score += senti_group_score
            last_senti_word_position = i + 1
    return review_score


# 判断评论情感极性
def judge_reviews(posi_reviews, nega_reiews, emotion_dict, rules=True):

    review_num = len(posi_reviews) + len(nega_reiews)
    TP, FP, TN, FN = 0, 0, 0, 0
    N_not_included = 0
    P_not_included = 0

    # 判断极性
    for review in nega_reiews:
        # logging.info('N: '+review)
        score = score_review(review, emotion_dict, rules=True)
        if score > 0:
            FP += 1
            log_score = log_score_review(review, emotion_dict, rules=True)
        elif score == 0:
            N_not_included += 1
        else:
            TN += 1

    for review in posi_reviews:
        # logging.info('P: '+review)
        score = score_review(review, emotion_dict, rules=True)
        if score > 0:
            TP += 1
        if score == 0:
            P_not_included += 1
        if score < 0:
            FN += 1
            # log_score = log_score_review(review, emotion_dict, rules=True)

    print('P_not_included:', P_not_included)
    print('N_not_included:', N_not_included)

    not_included = N_not_included + P_not_included
    print('not_included:', not_included)

    # 结果展示
    print('TP:', TP)
    print('FP:', FP)
    print('TN:', TN)
    print('FN:', FN)

    accuracy = (TP + TN) / review_num
    accuracy2 = (TP + TN) / (review_num - not_included + 1)
    precision = (TP + 1) / (TP + FP + 1)
    recall = (TP + 1) / (TP + FN + 1)
    print('accuracy:', accuracy)
    print('accuracy2:', accuracy2)
    print('precision:', precision)
    print('recall:', recall)

    F = precision * recall * 2 / (precision + recall)
    print('F:', F)

if __name__ == '__main__':

    NegaDataFile = open(os.path.join(os.getcwd(), 'data', 'New_NegativeShortSentence.csv'), 'r', encoding='utf8')
    PosiDataFile = open(os.path.join(os.getcwd(), 'data', 'New_PositiveShortSentence.csv'), 'r', encoding='utf8')

    NegaData = NegaDataFile.readlines()
    PosiData = PosiDataFile.readlines()

    print('PositiveReviewNum:', len(PosiData))
    print('NegativeReviewNum:', len(NegaData))

    logging.basicConfig(filename='NegativeMistake.log', level=logging.INFO)

    # ExtEmotionDict = {**BosonDict, **ExtSeedValueDict}
    ExtEmotionDict = Word2vecDict
    print('ExtEmotionDict:', len(ExtEmotionDict))

    #print(ExtEmotionDict['不'])
    #print(ExtEmotionDict['不用'])

    judge_reviews(PosiData, NegaData, ExtEmotionDict)
