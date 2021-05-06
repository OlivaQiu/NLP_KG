
# 基于TF-IDF来做抽取式摘要
import pickle
import numpy as np
from pyhanlp import HanLP
from word_segment_viterbi import ViterbiSegment


class ExtractiveSummary():

    def __init__(self, mode='work'):
        if mode == "train":
            self.IDF = None
        else:
            self.IDF = pickle.load(open("IDF_model.pkl", 'rb'))

    # 加载人民日报语料https://pan.baidu.com/s/1gd6mslt,形成每个句子的词语列表，用于后面统计词语频数
    def load_corpus(self, default_corpus_size=None):
        documents = []
        words_in_doc = []
        with open('../../uavnews/news2.txt', 'r', encoding='utf8') as f:
            lines = f.readlines()
            if default_corpus_size != None: lines = lines[:default_corpus_size]  # 测试阶段截取较小的语料
            print("文档总行数是", len(lines))
            for line in lines:

                line = line.replace('\n', '').split("  ")[1:]
                words = list(map(lambda x: x.split('/')[0], line))
                words = list(filter(lambda x: len(x) > 0, words))
                words_in_doc += words
                if len(words) == 0:  # 原始语料用空行来将文档分隔开
                    documents.append(words_in_doc)
                    words_in_doc = []
        return documents

    def train(self):
        self.IDF = {}
        document_freq = {}  # 词语的文档频率，即包含特定词语的文档个数
        documents = self.load_corpus(default_corpus_size=None)
        for doc in documents:
            for word in set(doc):
                document_freq[word] = document_freq.get(word, 0) + 1

        corpus_size = len(documents)
        for word in document_freq:
            self.IDF[word] = np.log(corpus_size / (document_freq[word] + 1))
        pickle.dump(self.IDF, open("IDF_model.pkl", 'wb'))

    def summary(self, text):
        sentences = text.split("。")  # 将文本切分为句子。
        new_sentences = []
        sentence_score = {}
        words_in_sentences = []
        segmentor = ViterbiSegment(mode='work')  # 一个demo分词器，训练语料与IDF的训练语料相同(分词粒度统一)。
        word_weight = {}  # 存储本文档中各个词语的term freq
        print("计算次词语权重")
        for sentence in sentences:
            if len(sentence) > 100 or len(sentence) < 2: continue
            words = segmentor.segment(sentence)  # 对句子分词，得到词语list
            for word in words:
                word_weight[word] = word_weight.get(word, 0) + 1
            words_in_sentences.append(words)
            new_sentences.append(sentence)
        print("计算句子权重", word_weight)
        for i in range(len(new_sentences)):
            sentence_score[new_sentences[i]] = np.sum(
                [word_weight[word] * self.IDF.get(word, 0.01) for word in words_in_sentences[i]])
        print("对句子排序")
        sentence_sorted = sorted(sentence_score.items(), key=lambda x: x[1], reverse=True)[:2]
        summary = "。".join(map(lambda x: x[0], sentence_sorted))
        return summary


if __name__ == '__main__':
    S = ExtractiveSummary(mode="work")
    #     S.train()
    text = """在认真听取大家发言后，李鹏宇做了总结。
    他表示，今年是新中国成立70周年，也是全面建成小康社会、实现第一个百年奋斗目标的关键之年。
    今年以来，面对纷繁复杂的国际国内形势，我们要好好学习。
    贯彻新发展理念，统筹推进稳增长、促改革、调结构、惠民生、防风险、保稳定各项工作。经济运行总体平稳、稳中有进，经济高质量发展取得新的进展。"""
    S.summary(text)