from pyhanlp import HanLP
import networkx as nx
from matplotlib import pyplot as plt
from textrank关键词 import Graph

class TextRankSummary(Graph):

    #切分句子。simple模式：基于句号分割
    def text2words(self, text):
        sentences = text.replace('\n', '').replace(' ', '').split("。")
        sentences = list(filter(lambda x: len(x) > 1, sentences))
        words_list = list(map(lambda x: self.word_segment(x), sentences))
        new_sentences, new_words_list = [], []
        for i in range(len(sentences)):
            if len(words_list[i]) > 0:
                new_sentences.append(sentences[i])
                new_words_list.append(words_list[i])
        return new_sentences, new_words_list

    def word_segment(self, sentence):
        word_tag_list = HanLP.segment(sentence)
        words = []
        for word_tag in word_tag_list:
            word_tag = str(word_tag).split('/')
            if len(word_tag) == 2:
                word, tag = word_tag
                if 'n' == tag and word not in self.stop_words:
                    words.append(word)
        return set(words)

    # 基于字，计算杰卡德相似度
    def sentence_simlarity(self, words1, words2):
        word_set1, word_set2 = set(words1), set(words2)
        simlarity = len(word_set1 & word_set2) / len(word_set2 | word_set2)
        return simlarity

    def get_sentence_links(self, sentences):
        sentence_link_list = []
        for s_id in range(len(sentences)):
            for s_jd in range(1, len(sentences)):
                if self.sentence_simlarity(sentences[s_id], sentences[s_jd]) > 0.5:
                    sentence_link_list.append([s_id, s_jd])
        return sentence_link_list

    def get_summary_with_textrank(self, text):
        self.clean()
        sentences, words_list = self.text2words(text)
        sentence_link_list = self.get_sentence_links(words_list)
        for link in sentence_link_list:
            self.add_link(link[0], link[1])
        self.get_PR()
        result = self.get_topN(8)
        summary_sentences = [sentences[i] for i, _ in result]
        return summary_sentences

if __name__ == '__main__':
    text = ''.join(list(open('news4.txt', 'r', encoding='utf8').readlines()))
    summary = TextRankSummary()
    summary_sentences = summary.get_summary_with_textrank(text)
    print("文章摘要是：")
    print('\n'.join(summary_sentences))