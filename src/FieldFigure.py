import pymongo
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib as mpl
from PIL import Image

font_msyh = mpl.font_manager.FontProperties(fname="../font/msyh.ttc")
mpl.rcParams['axes.unicode_minus'] = False

client = pymongo.MongoClient('localhost', 27017)
cnki_gzdi_data = client['cnki_gzdi_data']
detail_info_table = cnki_gzdi_data['detail_info_table']

all_x = []
keywords = [all_x.append(x['field']) for x in detail_info_table.find()]
# print(len(all_x))
all_temp = ""
all_dict = {}
for temp in all_x:
	all_temp += "\n".join(temp)
	for temptemp in temp:
		if temptemp in all_dict:
			all_dict[temptemp] += 1
		else:
			all_dict[temptemp] = 1

# print(all_temp)
# with open("keywords.txt", 'w') as temp_f:
# 	temp_f.write(all_temp.encode("gbk", 'ignore').decode("gbk"))
# keywords_stopwords = set([x.strip() for x in codecs.open(".txt", 'r', "utf-8").read().split('\n')])
wc = WordCloud(background_color=(255, 0, 0, 0), #背景颜色
               max_words=500,# 词云显示的最大词数
               # stopwords=keywords_stopwords,
               mode='RGBA',
               width=1024,
               height=768,
			   max_font_size=300, #字体最大值
               font_path='msyh.ttc',
			   random_state=50)
# wc.generate(all_temp)
wc.generate_from_frequencies(all_dict)
# print(sorted(all_dict.items(), key=lambda kv: (-kv[1], kv[0])))
#
# print(words)

plt.imshow(wc)
plt.axis('off')
plt.show()
wc.to_file("pics/field-cloud.png")

all_dict_sorted = sorted(all_dict.items(), key=lambda kv: (-kv[1], kv[0]))
former_10_keys = []
former_10_values = []
i = 0
for temp in all_dict_sorted:
	if i >= 10:
		break
	former_10_keys.append(all_dict_sorted[i][0])
	former_10_values.append(all_dict_sorted[i][1])
	i += 1

x = list(range(1, len(former_10_values) + 1, 1))
print(x)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
x.reverse()
#former_10_values.reverse()
ax.barh(x, former_10_values)
#plt.grid('on')
plt.title('学科领域分布', fontproperties=font_msyh)
#plt.ylabel('篇目', fontproperties=font_msyh)
plt.yticks(x, former_10_keys, fontproperties=font_msyh)
plt.savefig('pics/field-bar.png', dpi=300, format='png', bbox_inches='tight', transparent=True)
plt.show()
