#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
训练词向量模型 & 扩展情感词典的不同方法
"""

from gensim.models import Word2Vec
import logging
import csv
import os
from Dictionaries import EmotionDict, BosonDict

# 训练词向量模型
def word2vec_train(file_name, model_name):
    # Train word2vec model
    #
    # Read data
    sentences = []
    with open(os.path.join(os.getcwd(), 'data', file_name), 'r', encoding="utf8") as in_file:
        reader = csv.reader(in_file)
        for row in reader:
            sentences.append(row[0].split())

    # Print the number of reviews
    print('Read %d reviews' % len(sentences))

    # Logging nice output messages
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    model = Word2Vec(sentences, size=300)
    model.save(model_name)


# 基于极性情感词典
# 查找潜在情感词与其最相似的20个词的极性与相似度，计算并判断情感词的极性
def score_word_most_similar20(model, word, threshold):
    # Calculate word score and judge the polar of word by the similarity and polar of 20 most similar words
    #
    most_similar_20 = model.most_similar(word)
    relate_emotion_words = 0
    word_score = 0

    # Calculate word score
    for word_tuple in most_similar_20:
        if word_tuple[0] in EmotionDict.keys():
            relate_emotion_words += 1
            word_score += EmotionDict[word_tuple[0]] * word_tuple[1]
    word_score /= 20

    # Judge Emotion polar
    if word_score > threshold:
        polar = 1
    elif word_score < -threshold:
        polar = -1
    else:
        polar = 0
    return relate_emotion_words, word_score, polar


# 计算潜在情感词与“好”“差”两个种子词的向量距离
# 可以直接判断并返回潜在情感词极性，也可以依据返回的向量距离给潜在情感词“打分”
def score_word_similarity_seed_words(model, word, seed_words):

    Posi_seed_words = seed_words[0]
    Nega_seed_words = seed_words[1]
    similarity_good = 0
    similarity_bad = 0
    for posi_seed_word in Posi_seed_words:
        similarity_good += model.similarity(word, posi_seed_word)
    for nega_seed_word in Nega_seed_words:
        similarity_bad += model.similarity(word, nega_seed_word)

    if similarity_good > 0 and similarity_bad < 0:
        polar = 1
    elif similarity_good < 0 and similarity_bad > 0:
        polar = -1
    else:
        polar = 0
    return similarity_good, similarity_bad, polar


# 基于Boson情感词典
# 查找潜在情感词与其最相似的20个词的极性与相似度，计算潜在情感词的情感得分
def boson_most_similar20(model, word):
    # 基于Boson情感词典，计算潜在情感词的情感极值
    # 返回情感极值
    most_similar_20 = model.most_similar(word)
    relate_emotion_words = 0
    word_score = 0

    # Calculate word score
    for word_tuple in most_similar_20:
        if word_tuple[0] in BosonDict.keys():
            relate_emotion_words += 1
            word_score += BosonDict[word_tuple[0]] * word_tuple[1]
    if relate_emotion_words == 0:
        pass
    else:
        word_score /= relate_emotion_words
    return relate_emotion_words, word_score




if __name__ == '__main__':
    # word2vec_train('split_word2vec.csv', 'cellphone_review_300features')

    model_name = 'cellphone_review_300features'
    model = Word2Vec.load(model_name)

    print(model.most_similar('小米'))
    print(model.most_similar('屏幕'))
    print(model.most_similar('反应'))
    print(model.most_similar('外观'))

    with open(os.path.join(os.getcwd(), 'data', 'WordUndefined_no_degree_5.csv'), 'r', encoding='utf8') as in_f:
        with open(os.path.join(os.getcwd(), 'dict', 'NewAllSeedWords_5_Define_no_degree_5.csv'), 'w', encoding='utf8', newline='') \
                as out_f:
            # with open(os.path.join(os.getcwd(), 'data', 'NewSeedDefinePosi.txt'), 'w') as out_posi_f:
            #   with open(os.path.join(os.getcwd(), 'data', 'NewSeedDefineNega.txt'), 'w') as out_nega_f:
            headers = ['Word', 'Sim_good', 'Sim_bad', 'Value']
            reader = csv.DictReader(in_f)
            out_f_csv = csv.writer(out_f)
            out_f_csv.writerow(headers)
            posi_num, nega_num = 0, 0
            for row in reader:
                # print(row['Word'])
                # seed_words = [['好'], ['差']]
                seed_words = [['好', '不错', '喜欢', '满意', '好用'],['差', '不好', '垃圾', '失望', '坏']]
                similarity_good, similarity_bad, word_polar = score_word_similarity_seed_words(model,
                                                                                         row['Word'], seed_words)
                emotion_value = similarity_good - similarity_bad

                # if word_polar == 1:
                #     posi_num += 1
                #     #out_posi_f.write(row['Word']+'\n')
                # elif word_polar == -1:
                #     nega_num += 1
                #     #out_nega_f.write(row['Word'] + '\n')
                # relate_words, emotion_value = boson_most_similar20(model, row['Word'])
                out_f_csv.writerow([row['Word'], similarity_good, similarity_bad, emotion_value])
            print('Positive:', posi_num)
            print('Negative:', nega_num)




