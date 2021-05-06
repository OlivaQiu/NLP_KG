from pyhanlp import *
import xlwt#写入excel的库
#coding=utf-8
#hanlp分词
words = '基于无人机测绘技术，文章进行了无人机地籍测绘及其精度分析。在精度方面，将无人机地籍测绘精度分为明显界址点测绘精度、隐蔽界址点测绘精度与地物点平面位置精度。通过对佛山某地区进行1∶500地籍图测绘，发现明显界址点精度达到二级要求，隐蔽界址点精度达到三级要求，总体上满足三级要求，地物点平面位置精度完全符合精度要求。通过精度稳定性评价，发现明显界址点和地物点精度稳定性达到84%，而隐蔽界址点精度稳定性只有75%，因此无人机地籍测绘存在一定的局限性，它仅适用于包含明显界址点区域的低等级地籍测绘，而不适用于隐蔽界址点较多区域的地籍测绘，目前无人机地籍测绘尚无法独立实施。'
print(HanLP.segment(words).toString())

#读取文件
document = ''.join(open('news3.txt', 'r', encoding='utf8').readline())
outwords = HanLP.segment(document).toString()
print(outwords)
#写入文件，保存到本地
outfile1 = open('uav-words3.txt','a+',encoding='utf-8')
for word in outwords:
    outfile1.write(word)
outfile1.close()


for term in HanLP.segment('随着无人机应用的纵深发展，近年来无人机在地籍测绘中的应用也逐渐增多，宋亮利用无人机影像制作了调查底图[7]，宋光浩等基于UX5无人机进行了地籍测绘初探，结果证明无人机测绘满足1∶500农村不动产测绘要求[8]。由于界址点是地籍测量的核心，因此地籍测绘中只要满足界址点的精度，地籍图的精度亦随之满足。在界址点精度方面，1994年国家测绘局颁布的《地籍测绘规范》设立一、二、三3个等级[9]，对应的中误差要求分别为±0.05m，±0.10m和±0.15m，2007年二调时国土资源部颁发的《第二次全土地调查技术规程》，将界址点精度定位一、二2个等级[10]，相应的中误差要求为±5cm和±7.5cm，精度有所提高，随后2012年国土资源部颁布的《地籍调查规程》又将界址点恢复3个级别，其中误差要求分别是±5cm、±7.5cm和±10.0cm[11]，这是综合了《地籍测绘规范》和《第二次全国土地调查技术规程》而制定的新标准。'):
    print('{}\t{}'.format(term.word,term.nature))#获取单词与词性


text = '随着无人机飞控系统的提升，目前市面测绘型无人机技术逐步走向成熟[1]，基于各种类型的无人机大比例尺测绘项目也如火如荼地展开[2]，取得了令人满意的成果。凭借其快速高效、机动灵活、成本低、周期短、适应性强、信息真实、质量可靠等优点[3]，无人机测绘应用范围越来越广。在大比例尺地形图测绘方面，吕立蕾利用固定翼无人机分别测绘了1∶1000和1∶500地形图，最终得出无人机可满足1∶1000比例尺测图精度，而不满足1∶500测图精度[4]，刘聪等人利用无人机获取了某铝土矿1∶2000数字线划图、数字高程模型和数字正射影像[5]，李玉成等人通过空三测量精度与SDCORS对比、地物点精度与GPSRTK精度对比，得出了与吕立蕾相似的结论[6]，因此，无人机测绘1∶1000地形图精度可以满足要求。'

CRFLexicalAnalyzer = JClass("com.hankcs.hanlp.model.crf.CRFLexicalAnalyzer")
analyzer = CRFLexicalAnalyzer()
han_word_pos1 = analyzer.analyze(text).toString()
print(han_word_pos1)#text 测试　输出到控制台
#document为 news3.txt
han_word_pos2 = analyzer.analyze(document).toString()
print('##########')
print(han_word_pos2)

for term in HanLP.segment(document):
    print('{}\t{}'.format(term.word,term.nature))#获取单词与词性)
print('########')

#写入文件，保存到本地
outfile2 = open('uav-words4.txt','a+',encoding='utf-8')
for word in han_word_pos2:
    outfile2.write(word)
outfile2.close()


testCases=[
    "本文基于新版《地籍调查规程》对界址点的要求，",
    "通过统计界址点中误差和地物平面位置精度，对无人机地籍测绘精度做出评价。",
    "利用无人机进行了佛山某区地籍图测绘，"]
for sentence in testCases:
    print(HanLP.segment(sentence))
