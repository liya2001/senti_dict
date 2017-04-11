#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
提取潜在情感词
"""

import os
import csv
import re
from Dictionaries import BosonDict, DegreeDict, NegativeDict, UserWords


if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'data', 'ReviewCount.csv'), 'r', encoding='utf8') as review_f:
        with open(os.path.join(os.getcwd(), 'data', 'WordUndefined_no_degree_5.csv'), 'w', encoding='utf8', newline='') as out_f:
            reader = csv.DictReader(review_f)
            headers = ['Word', 'Count']
            out_f_csv = csv.writer(out_f)
            out_f_csv.writerow(headers)
            i = 0
            for row in reader:
                if int(row['Count']) > 5:
                    # if row['Word'] not in BosonDict.keys():
                    # if row['Word'] not in DegreeDict.keys():
                    if row['Word'] in NegativeDict:
                        print(row['Word'])
                    else:
                        #     if row['Word'] in UserWords:
                        #         i += 1
                        if re.findall(u'[^a-zA-Z\d]+', row['Word']):
                                out_f_csv.writerow([row['Word'], row['Count']])
            print(i)
