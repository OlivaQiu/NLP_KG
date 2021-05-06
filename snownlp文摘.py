from snownlp import SnowNLP
text1 = "优势二：体积小、重量轻此次蜂鸟微型无人机LiDAR搭载于M600无人机平台。关注我们的朋友应该有了解，升级后的蜂鸟系统总重量仅有1.168kg，其中扫描仪的重量仅有738g，可以轻松搭载在大疆M200/M210无人机平台。而换成了新的无人机平台M600，蜂鸟一样可以方便接驳其间。除了兼容性强以外，这也与蜂鸟LiDAR系统轻便的身躯有直接关系。"
text2 = "优势三：模块化集成设计蜂鸟Genius-32线激光雷达，同样来自北科天绘自主研发，Applanix公司MEMS高精度惯导测量系统，配合地面静态基准站数据最终可解算得到具有绝对坐标的轨迹情况。包括相机和光谱传感器方面，都可以根据项目具体需求进行搭配调整."
#1分词
seg1 = SnowNLP(text1)
print("/".join(seg1.words))
seg2 = SnowNLP(text2)
print("/".join(seg2.words))

#2词性标注
tags1 =[x for x in text1]
print(tags1)
tags2 =[x for x in text2]
print(tags2)

#3断句
print(seg1.sentences)
print(seg2.sentences)

#4情感分析:返回值为正面情绪的概率，越接近1越表示积极情绪，越接近0越表示负面情绪
s1=SnowNLP(text1)
print(s1.sentiments)
s2=SnowNLP(text2)
print(s2.sentiments)

#5拼音
print(seg1.pinyin)

#6繁体转简体
print(seg2.han)

#7关键词提取 limit
text3 = "优势四：测程远、高点频、高精度蜂鸟最远测距为250m，测量速度64万点/秒，系统测距精度2cm，绝对精度优于10cm，可以满足最大比例尺1:500的地形测绘工作。蜂鸟32线激光雷达系统参数表"
seg4 = SnowNLP(text3)

print(seg1.keywords(limit=5))
print(seg2.keywords(limit=5))
print(seg4.keywords(limit=8))

#8关键句提取
print(seg4.summary(limit=5))
print(seg1.summary(limit=5))
print(seg2.summary(limit=5))


document = "航摄飞行时，先将笔记本连接通讯电台，在eMotion2中设计飞行路线。"\
            "实验区东部为低矮丘陵山脚，中西部较为平坦，是建筑集中区。该区域东西长150m，南北长120m，测区内高差约25m，飞行前预先设计航线航向重叠度、旁向重叠度、飞行高度、基高比、分辨率等重要技术参数。"\
            "根据规范要求，此次飞行航高300m，航向重叠度70%，旁向重叠度65%，基高比0.39，影像对地分辨率GSD为0.05m，共拍摄404张航片，航线及曝光点影像如图"
seg4 = SnowNLP(document)
print(seg4.keywords(limit=6))
print(seg4.summary(limit=6))

#9信息衡量:TF词频越大越重要 IDF若包含词条t的文档越少（n越少）IDF越大则说明词条t越重要
print(seg1.tf)
print(seg1.idf)
print(seg2.tf)
print(seg2.idf)
#print(seg3.tf)
#print(seg3.idf)
print(seg4.tf)
print(seg4.idf)

#10文本相似性
print(seg4.sim(['好']))
print(seg4.sim(['不']))

#实验
document = ''.join(open('news4.txt', 'r', encoding='utf8').readline())
seg = SnowNLP(document)
print('news4.txt的分词结果是：')
print("/".join(seg.words))

tags3 =[x for x in document]
print('news4.txt的词性标注结果是：')
print(tags3)

print('news4.txt的断句结果是：')
print(seg.sentences)

#print('news4.txt的情感分析结果是：')
#s3=SnowNLP(document)
#print(seg.sentiments)

#seg5 = SnowNLP(document)
print('news4.txt的关键词提取结果是：')
outwords = seg.keywords(limit=5)
print(outwords)
outfile1 = open('摘要２.txt','a+',encoding='utf-8')
for word in outwords:
    outfile1.write(word)
    outfile1.write('\n')
outfile1.close()

print('news4.txt的关键句提取结果是：')
abstract =seg.summary(limit=8)
print(abstract)
outfile2 = open('摘要２.txt','a+',encoding='utf-8')
for word in abstract:
    outfile2.write(word)
outfile1.close()