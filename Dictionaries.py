# -*- coding: utf-8 -*-

"""
导入多个词典
"""

import csv
import os
import re
from openpyxl import load_workbook


EmotionDict = {}
DegreeDict = {}
BosonDict = {}
ExtMostSimilar = {}
ExtSimilarity = {}
ExtSeedValueDict = {}
ExtMostValueDict = {}
Word2vecDict = {}
UserWords = set()

# 极性情感词典 EmotionDict
with open(os.path.join(os.getcwd(), 'dict', 'PolarDict.csv'), 'r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        EmotionDict[row['Word']] = int(row['Polar'])

# 否定词词典 NegativeDict
with open(os.path.join(os.getcwd(), 'dict', 'NegativeDict.txt'), 'r') as not_f:
    NegativeDict = set(not_f.readline().split())

# 评价对象 UserWords
with open(os.path.join(os.getcwd(), 'dict', 'userword.csv'), 'r', encoding='utf8') as user_f:
    reader = csv.reader(user_f)
    for row in reader:
        UserWords.add(row[0])

# Boson情感词典 BosonDict
with open(os.path.join(os.getcwd(), 'dict', 'BosonNLP_sentiment_score.txt'), 'r', encoding='utf8') as f:
    for row in f.readlines():
        try:
            BosonDict[row.split(' ')[0]] = float(row.split(' ')[1])
        except IndexError:
            print(row)

# 扩展极性词
# 中心词相似度方法
with open(os.path.join(os.getcwd(), 'dict', 'PolarDict', 'NewSeedDefinePosi.txt'), 'r') as Posi_f:
    with open(os.path.join(os.getcwd(), 'dict', 'PolarDict', 'NewSeedDefineNega.txt'), 'r') as Nega_f:
        for line in Posi_f:
            word = line.strip('\n')
            ExtSimilarity[word] = 1.0
        for line in Nega_f:
            word = line.strip('\n')
            ExtSimilarity[word] = -1.0

# 最相似20词方法
with open(os.path.join(os.getcwd(), 'dict', 'PolarDict', 'NewDefinePosi_05.txt'), 'r') as Posi_f:
    with open(os.path.join(os.getcwd(), 'dict', 'PolarDict', 'NewDefineNega_05.txt'), 'r') as Nega_f:
        for line in Posi_f:
            word = line.strip('\n')
            ExtMostSimilar[word] = 1.0
        for line in Nega_f:
            word = line.strip('\n')
            ExtMostSimilar[word] = -1.0


# 从csv文件读取词典
def csv_dict(file_path, coefficient):
    value_dict = {}
    with open(os.path.join(os.getcwd(), 'dict', file_path), 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            value_dict[row['Word']] = float(row['Value']) * coefficient
    return value_dict

# 程度副词词典 DegreeDict
DegreeDict = csv_dict('DegreeDict.csv', 1.0)

# 扩展有极值情感词
# 中心词相似度方法
# BosonSeedWordsDefine.csv
ExtSeedValueDict = csv_dict('SeedWords_3_Define_5.csv', 7.0)
# 最相似20词方法
ExtMostValueDict = csv_dict('BosonMostSimilarDefine.csv', 1.0)

# 不采用现有词典
# 所有词频大于10的词都作为情感词 Word2vecDict
Word2vecDict = csv_dict('NewAllSeedWords_5_Define_no_rules_5.csv', 10.0)
'''
DalianDict = {}
wb = load_workbook(filename='dalian.xlsx', read_only=True)
sheets = wb.get_sheet_names()
sheet_zero = sheets[0]
ws = wb.get_sheet_by_name(sheet_zero)
for row in ws.rows:
    if row[6].value == 1:
        DalianDict[row[0].value] = row[5].value
    elif row[6].value == 2:
        DalianDict[row[0].value] = row[5].value*-1
    else:
        pass
'''


if __name__ == '__main__':
    for word in UserWords:
        if word not in BosonDict.keys():
            print(word)

