import jieba
document1 = ''.join(open('news6.txt', 'r', encoding='utf8').readline())
#全模式
seg_list1 = jieba.cut(document1,cut_all=True)
print("full mode全模式：")
full_mode = "/".join(seg_list1)
print(full_mode)

input_file = open('jieba全模式分词１.txt','a+',encoding='utf-8')
for word in full_mode:
    input_file.write(word)

#精确模式=默认模式
seg_list2 = jieba.cut(document1,cut_all=False)
print("Default mode精确模式：")
default_mode = "/".join(seg_list2)
print(default_mode)

input_file = open('jieba精确模式分词2.txt','a+',encoding='utf-8')
for word in default_mode:
    input_file.write(word)

#搜索引擎模式
seg_list3 = jieba.cut_for_search(document1)
print("Search mode搜索引擎模式：")
search_mode = "/".join(seg_list3)
print(search_mode)

input_file = open('jieba搜索引擎模式分词3.txt','a+',encoding='utf-8')
for word in search_mode:
    input_file.write(word)