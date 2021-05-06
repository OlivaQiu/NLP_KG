"""
将句中识别的实体与知识库中实体进行匹配，解决实体歧义问题。 可利用上下文本相似度进行识别。
在data/entity_disambiguation目录中，entity_list.csv是50个实体，valid_data.csv是需要消歧的语句。
答案提交在submit目录中，命名为entity_disambiguation_submit.csv。格式为：第一列是需要消歧的语句序号，第二列为多个“实体起始位坐标-实体结束位坐标：实体序号”以“|”分隔的字符串。
"""
import os
import jieba
import pandas  as pd
import collections
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

work_dir = os.path.abspath('.')
entity_csv = os.path.join(work_dir,'data/entity_disambiguation/entity_list.csv')
#todo:将entity_list.csv中已知的实体名称导入分词词典
entity_data = pd.read_csv(entity_csv,encoding='utf-8')
valid_csv = os.path.join(work_dir,'data/entity_disambiguation/valid_data.csv')
#todo:对句子进行识别并匹配实体
valid_data = pd.read_csv(valid_csv,encoding='utf-8')

#建立关键词组
s = ''
keyword_list = []
for i in entity_data['entity_name'].values.tolist():
    s += i + '|'
for k,v in collections.Counter(s.split('|')).items():
    if v > 1:
        keyword_list.append(k)

#生成tf-idf矩阵
train_sentence = []
for i in entity_data['desc'].values:
    train_sentence.append(' '.join(jieba.cut(i)))

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(train_sentence)

#获取包含关键字的句子中关键词所属的entity_id
def get_entityid(sentence):
    id_start = 1001
    a_list = [' '.join(jieba.cut(sentence))]
    res = cosine_similarity(vectorizer.transform(a_list),X)[0]
    top_idx = np.argsort(res)[-1]
    return  id_start + top_idx

#todo:将计算结果保存到文件
row = 0
result_data = []
neighbor_sentence = ''
print("valid_data['sentence']:",valid_data['sentence'])
for sentence in valid_data['sentence']:
    res = [row]
    for keyword in keyword_list:
        #查询关键词在句子中的索引
        k_len = len(keyword)
        ss = ''
        for i in range(len(sentence) - k_len + 1):
            if sentence[i:i + k_len] == keyword:
                s = str(i) + '-' + str(i + k_len) + ':' #拿到 x-x
                if i > 10 and i + k_len < len(sentence) - 9:
                    neighbor_sentence = sentence[i - 10:i + k_len + 9]
                elif i < 10:
                    neighbor_sentence = sentence[:20]
                s += str(get_entityid(neighbor_sentence))#拿到 x-x:id
                ss += s + '|' #拿到 x-x:id | x-x:id
        res.append(ss[:-1]) #拼接成[0,'x-x:id | x-x:id']
    result_data.append(res)
    row += 1
output = os.path.join(work_dir,'submit/entity_disambiguation_submit.csv')
pd.DataFrame(result_data).to_csv(output,index=False)
