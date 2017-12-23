# http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=2017&issue=04&pykm=GZDI&pageIdx=0
import requests
import pymongo
from bs4 import BeautifulSoup
re = requests.get('http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=2017&issue=04&pykm=GZDI&pageIdx=0')
soup = BeautifulSoup(re.text, 'lxml')
ans = soup.select('dd.row > span.name > a')
for an in ans:
	print(an.get_text().strip())

"""	
《代微积拾级》中的传统分析学思想
二维Kemmer谐振子在非对易平面下的精确解
乙烯利对烟草离体叶圆片衰老相关生理指标的影响
陕西榆林河谷区地下水特征分析
微型燃气轮机与天然气管网接口建模及联合仿真研究
风电与热网联合供能仿真研究
输配分离含微电网的电力市场中配电公司购电模型研究
云数据处理技术在特种设备监督管理平台中的应用研究
国有企业数据铁笼设计与安全保障方法研究
虚拟参考反馈校正控制在转台系统中的应用
基于下近似分布的变精度邻域粗糙集属性约简算法
基于层次结构的多分类算法研究
超高层钢网格混凝土核心筒盒式结构动力弹塑性分析
钢-混凝土组合空腹夹层板几种有限元模型的对比研究
加固加高边坡的支护设计及稳定性分析
多层大跨度蜂窝型钢网格盒式结构动力分析
新型盒式结构的振型和基频分析
榫卯式混凝土空心异型砌块砌体力学性能研究
玻璃纤维增强磷石膏复合材料力学性能研究
考虑机动车干扰下的人行横道处行人延误研究
基于交通形态的城市商业区车辆PM2.5排放模型研究
城市快速公路无控接入口与相邻大型信号路口接入间距分析
水产养殖废水中1株高营养价值栅藻的生长及氮磷去除特性的研究
贵州织金县农村缺水地区分散供水水质分析与评价
一种新型解钾菌的筛选及鉴定
基于时序TOPSIS法的遵义市土地利用效益综合评价
贵州大学学报(自然科学版)征稿简则
"""

for an in ans:
	print(an.get('href'))
"""
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704001&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704002&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704003&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704004&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704005&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704006&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704007&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704008&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704009&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704010&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704011&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704012&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704013&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704014&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704015&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704016&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704017&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704018&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704019&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704020&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704021&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704022&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704023&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704024&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704025&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704026&tableName=CJFDLAST2017&url=
Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=GZDI201704027&tableName=CJFDLAST2017&url=
"""

for an in ans:
	print(an.get('href').split('&')[-3])

"""	
filename=GZDI201704001
filename=GZDI201704002
filename=GZDI201704003
filename=GZDI201704004
filename=GZDI201704005
filename=GZDI201704006
filename=GZDI201704007
filename=GZDI201704008
filename=GZDI201704009
filename=GZDI201704010
filename=GZDI201704011
filename=GZDI201704012
filename=GZDI201704013
filename=GZDI201704014
filename=GZDI201704015
filename=GZDI201704016
filename=GZDI201704017
filename=GZDI201704018
filename=GZDI201704019
filename=GZDI201704020
filename=GZDI201704021
filename=GZDI201704022
filename=GZDI201704023
filename=GZDI201704024
filename=GZDI201704025
filename=GZDI201704026
filename=GZDI201704027
"""

# detail page:
# http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=GZDI201704001

# TODO: year and issue spider
# TODO: detailed page: title, name, unit, foundation, keywords, abstract
