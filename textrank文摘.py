#-*- encdoing:utf-8 -*-
import codecs
from textrank4zh import TextRank4Keyword,TextRank4Sentence
text = codecs.open('/news1.txt', 'r', 'utf-8').read()
tr4w = TextRank4Keyword(stop_words_file='/home/nlp/PycharmProjects/NLP文摘/uavnews/stopwords.txt') #导入停用词

#使用词性过滤，文本小写，窗口为2
tr4w.train(text=text,speech_tag_filter=Ture,lower=Ture,window=2)

print('关键词：')
#20个关键词且每个长度最小为1
print('/'.join(tr4w.get_keywords(20,word_min_len=1)))

print('关键词短语：')
#20个关键词去构造短语，短语在原文本中出现次数最少为2
print('/'.join(tr4w.get_keyphrases(keywords_num=20,min_occur_num=2)))

tr4s = TextRank4Sentence(stop_words_file='/home/nlp/PycharmProjects/NLP文摘/uavnews/stopwords.txt')

#使用词性过滤，文本小写，使用word_all_filters生成句子之间的相似性
tr4s.train(text=text,speech_tag_filter=Ture,lower=Ture,source = 'all_filters')

print('摘要：')
print('\n'.join(tr4s.get_key_sentences(num=5)))#重要性最高的5个句子