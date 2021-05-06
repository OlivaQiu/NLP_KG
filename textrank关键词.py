from pyhanlp import HanLP
import networkx as nx
from matplotlib import pyplot as plt

class GraphPlot():

    def __init__(self):
        self.fig = plt.figure()
        plt.ion()  # 允许更新画布
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.rcParams['figure.figsize'] = (18.0, 14.0)  # 设置figure_size尺寸

    def graph_plot(self, link_weight_list):
        plt.cla()  # 清除画布上原来的图像
        G = nx.Graph()
        for node1, node2, weight in link_weight_list:  # 添加节点以及边的权重
            G.add_edge(str(node1), str(node2), weight=weight)

        weights = [d['weight'] for u, v, d in G.edges(data=True)]
        pos = nx.circular_layout(G)  # 借点我围成一个圈，便于展示边的情况
        nx.draw_networkx_edges(G, pos, font_size=14, width=weights)  # 绘制图中边的权重
        nx.draw_networkx(G, pos, node_size=400)
        plt.pause(2)  # 展示出来定格2秒


# 用于存储图
class Graph():
    def __init__(self):
        self.linked_node_map = {}  # 邻接表，
        self.PR_map = {}  # 存储每个节点的入度
        self.stop_words = set({'我'})

    def clean(self):
        self.linked_node_map = {}  # 邻接表，
        self.PR_map = {}  # 存储每个节点的入度

    # 添加节点
    def add_node(self, node_id):
        if node_id not in self.linked_node_map:
            self.linked_node_map[node_id] = set({})
            self.PR_map[node_id] = 0
        else:
            print("这个节点已经存在")

    # 增加一个从Node1指向node2的边。允许添加新节点
    def add_link(self, node1, node2):
        if node1 not in self.linked_node_map:
            self.add_node(node1)
        if node2 not in self.linked_node_map:
            self.add_node(node2)
        self.linked_node_map[node1].add(node2)  # 为node1添加一个邻接节点，表示ndoe2引用了node1

    # 计算pr
    def get_PR(self, epoch_num=5, d=0.8, if_show=False):  # 配置迭代轮数，以及阻尼系数
        if if_show:
            GP = GraphPlot()  # 用于plot网络的实例
        for i in range(epoch_num):
            for node in self.PR_map:  # 遍历每一个节点
                self.PR_map[node] = (1 - d) + d * sum(
                    [self.PR_map[temp_node] for temp_node in self.linked_node_map[node]])  # 原始版公式
            #             print(self.PR_map)

            # 展示节点之间的链接权重
            if if_show:
                link_weight_list = []
                topN_nodes = set(list(map(lambda x: x[0], self.get_topN(10))))
                for source, targets in self.linked_node_map.items():
                    if source not in topN_nodes: continue
                    for t in targets:
                        link_weight_list.append([source, t, self.PR_map[source]])
                GP.graph_plot(link_weight_list)
            # 展示节点之间的链接权重

    def get_topN(self, top_n):
        topN = sorted(self.PR_map.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return topN


class TextRankKeyword(Graph):

    def segment(self, text):
        word_tag_list = HanLP.segment(text)
        word_tag_list = list(map(lambda x: str(x).split('/'), word_tag_list))
        return word_tag_list

    # 对文本分词和磁性标注，取名词，删除停用词，得到候选关键词，并构建词语关系
    def get_word_links(self, text, window_size=5):
        word_tag_list = self.segment(text)
        word_keyword_1 = list(
            map(lambda x: [x[0], True] if 'n' == x[1] and x[0] not in self.stop_words else [x[0], False],
                word_tag_list))
        word_link_list = []
        for i in range(len(word_keyword_1)):
            current_word, current_flag = word_keyword_1[i][0], word_keyword_1[i][1]
            if current_flag:
                for j in range(i + 1, min(i + 1 + window_size, len(word_keyword_1))):
                    temp_word, temp_flag = word_keyword_1[j][0], word_keyword_1[j][1]
                    if temp_flag and current_word != temp_word:
                        word_link_list.append(tuple(sorted([current_word, temp_word])))
        return word_link_list

    def get_keyword_with_textrank(self, text):
        self.clean()
        word_links = self.get_word_links(text)
        for word_pair in word_links:
            self.add_link(word_pair[1], word_pair[0])
        self.get_PR(if_show=True)
        keyword_weight_list = self.get_topN(5)
        return keyword_weight_list


if __name__ == '__main__':
    text = ''.join(list(open('news4.txt', 'r', encoding='utf8').readlines()))
    keyword_extractor = TextRankKeyword()
    keyword_weight_list = keyword_extractor.get_keyword_with_textrank(text)
    print("关键词是:")
    print(keyword_weight_list)