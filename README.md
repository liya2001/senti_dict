# senti_dict
Sentiment analysis system based on sentiment dictionary and rules

分别实验了极性词典（综合HowNet，NTUSD，清华褒贬义词典），极性和强度值词典（BosonNLP，大连理工大学情感词汇本体），BosonNLP词典效果最好。
实践了两种扩展词典算法，都是基于Word2vec计算语义距离，其中算法二通过计算词语与基准词余弦距离作为该词情感得分效果最好。不采用任何现有词典，将所有高频词作为情感词通过算法二计算情感倾向和强度值，正确率最高达到了83.4%。该方法优点是无监督学习，泛化性好。
