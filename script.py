#-*- coding:utf-8 –*-
import re
import os
#高度相关的结论

#AD XD XR 位点
#即 该样本分析到XXXX有一个杂合突变
#context_1 为高度相关表格内容
context_1 = {'基因': 'TSC1', '染色体位置': 'chr19-40900984', '转录本编号': 'NM_181882', '外显子': 'exon7',
             '核苷酸变化': 'c.3275A>T', '氨基酸变化': 'p.V1092X', '纯合/杂合': 'het', '正常人中频率': '-', '致病性分析': 'uncertain'
            , '遗传方式' : '1.AR 2.AD/AR', '疾病/表型' :'1.腓骨肌萎缩症4F型 2.Dejerine-Sottas疾病', '变异来源': '父亲'}
#氨基酸字母对应中文
animo = {'A':'丙氨酸', 'R':'精氨酸','D':'天冬氨酸','C':'半胱氨酸','Q':'谷氨酰胺','E':'谷氨酸','H':'组氨酸'
       ,'I':'异亮氨酸','G':'甘氨酸','N':'天冬酰胺','L':'亮氨酸','K':'赖氨酸','M':'甲硫氨酸','F':'苯丙氨酸',
       'P':'脯氨酸','S':'丝氨酸','T':'苏氨酸','W':'色氨酸','Y':'酪氨酸','V':'缬氨酸'}
#核苷酸字母对应中文
nucleotide = {'A':'腺嘌呤','G':'鸟嘌呤', 'C':'胞嘧啶','T':'胸腺嘧啶'}






#句子整体
string_1 = '该样本分析到{0}基因有1个杂合突变:\n'.format(context_1['基因'])
string_2 = ''
string_3 = ''
string_4 = ''
if context_1['核苷酸变化'].__contains__('del'):
    pattern = re.compile(r'\d+')
    result_1 = pattern.findall(context_1['核苷酸变化'])
    result_2 = pattern.findall(context_1['氨基酸变化'])
    string_2 = '{0}(编码区第{1}号核苷酸缺失)，'.format(context_1['核苷酸变化'],result_1[0])
    string_3 = '导致氨基酸改变{0}(第{1}号氨基酸缺失)，'.format(context_1['氨基酸变化'], result_2[0])
    string_4 = ''
elif context_1['核苷酸变化'].__contains__('ins'):
    pattern = re.compile(r'\d+')
    result_1 = pattern.findall(context_1['核苷酸变化'])
    result_2 = pattern.findall(context_1['氨基酸变化'])
    string_2 = '{0}(编码区第{1}号核苷酸插入)，'.format(context_1['核苷酸变化'], result_1[0])
    string_3 = '导致氨基酸改变{0}(第{1}号氨基酸插入)，'.format(context_1['氨基酸变化'], result_2[0])
    string_4 = ''
elif context_1['核苷酸变化'].__contains__('+') or context_1['核苷酸变化'].__contains__('-'):
    # 初始核苷酸
    a = nucleotide[context_1['核苷酸变化'][-3]]
    # 变化核苷酸
    b = nucleotide[context_1['核苷酸变化'][-1]]
    # 核苷酸编号
    c = context_1['核苷酸变化'][2:-3]
    string_2 = '{0}(编码区第{3}号核苷酸由{1}变异为{2})，'.format(context_1['核苷酸变化'],a,b,c)
    string_3 = '导致氨基酸改变(剪接突变)。'
    string_4 = ''
elif context_1['氨基酸变化'][-1] == 'X':
    # 初始核苷酸
    a = nucleotide[context_1['核苷酸变化'][-3]]
    # 变化核苷酸
    b = nucleotide[context_1['核苷酸变化'][-1]]
    pattern = re.compile(r'\d+')
    result_1 = pattern.findall(context_1['核苷酸变化'])
    string_2 = '{0}(编码区第{3}号核苷酸由{1}变异为{2})，'.format(context_1['核苷酸变化'], a, b, result_1[0])
    string_3 = '导致氨基酸改变{0}(为无义突变)，'.format(context_1['氨基酸变化'])
    string_4 = ''
else:
    # 初始核苷酸
    a = nucleotide[context_1['核苷酸变化'][-3]]
    # 变化核苷酸
    b = nucleotide[context_1['核苷酸变化'][-1]]
    # 核苷酸编号
    c = context_1['核苷酸变化'][2:-3]
    # 初始氨基酸
    a_1 = animo[context_1['氨基酸变化'][2]]
    # 变化氨基酸
    b_1 = animo[context_1['氨基酸变化'][-1]]
    # 氨基酸编号
    c_1 = context_1['氨基酸变化'][3:-1]
    string_2 = '{0}(编码区第{3}号核苷酸由{1}变异为{2})，'.format(context_1['核苷酸变化'], a, b, c)
    string_3 = '导致氨基酸改变{0}(第{1}号氨基酸由{2}变异为{3})，'.format(context_1['氨基酸变化'], c_1, a_1, b_1)
    string_4 = '为错义突变。'

#加入致病性中英文对照字典
dic = {'uncertain':'临床意义未明','likely_pathogenic':'疑似致病性变异','pathogenic':'致病性'}

string_5 = '该变异在正常人群数据库1000 genomes、ESP6500、InHouse、EXAC和EXAC-EAS中的频率分别为-、-、-、-、-。蛋白功能预测软件REVEL无预测结果。'
string_6 = '在HGMD专业版数据库中未见报道。'
string_7 = '经家系验证分析，受检人之父该位点无变异，受检人之母该位点无变异。'
string_8 = '为自发突变，该位点为{0}'.format(dic[context_1['致病性分析']])
string_9 = '请结合受检者的临床表现、家族史及其他检测结果综合分析。'
string = string_1+string_2+string_3+string_4+string_5+string_6+string_7+string_8+string_9


#AR 位点
#即 该样本分析到XXXX有2个杂合突变

string__1 = '该样本分析到{0}基因有2个杂合突变:\n'.format(context_1['基因'])
#string__2 = '(1).{0}(编码区第{3}号核苷酸由{1}变异为{2})，'.format(context_1['核苷酸变化'],a,b,c)
#string__3 = '导致氨基酸改变{0}(第{1}号氨基酸由{2}变异为{3})，'.format(context_1['氨基酸变化'],c_1,a_1,b_1)
string__4 = '为错义突变。'
string__5 = '该变异不属于多态性位点，在人群中发生频率极低。'
string__6 = '在HGMD专业版数据库中未见报道。'
string__7 = '经家系验证分析，受检人之父该位点无变异，受检人之母该位点无变异。'

conclusion = '结论：此基因变异为复合杂合变异，该基因变异为疑似致病性变异。请结合受检者的临床表现、家族史及其他检测结果综合分析。'

#String = string__1+string__2+string__3+string__4+string__5+string__6+string__7

path = os.path.dirname(os.path.abspath('__file__'))

print(path)
file = open(path+r'\file.txt', 'w')

file.write('{0}\n'.format(string))


file.close()