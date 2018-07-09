import pymongo
import matplotlib.pyplot as plt
import matplotlib as mpl

font_msyh = mpl.font_manager.FontProperties(fname="../font/msyh.ttc")
mpl.rcParams['axes.unicode_minus'] = False

client = pymongo.MongoClient('localhost', 27017)
cnki_gzdi_data = client['cnki_gzdi_data']
detail_info_table = cnki_gzdi_data['detail_info_table']

total_year = [line['year'] for line in detail_info_table.find()]

frequency = {}
for year in total_year:
	if year in frequency:
		frequency[year] += 1
	else:
		frequency[year] = 1

print(frequency)

plt.style.use('ggplot')
fig = plt.figure(figsize=(8, 4.5))
ax = fig.add_subplot(111)
x = list(range(1, len(frequency)+1, 1))
y = list(frequency.values())
y.reverse()
ax.plot(x, y)
xticks = list(frequency.keys())
xticks.reverse()
ax.set_xticks(x)
ax.set_xticklabels(xticks, rotation=60)
avg = sum(y)/len(y)
print('Average: ', avg)
ax.axhline(y=avg, linestyle='--', linewidth=1, color='b')
plt.text(25, avg+1, 'Average: ' + str(avg)[:4], fontsize=10)
ax.set_title('Number of Papers per Year', fontsize=14, fontweight='bold')
plt.savefig('pics/PaperNumberPerYear.png', transparent=True)
plt.show()


print('Year: ', list(frequency.keys())[list(frequency.values()).index(max(y))])
print('Max Paper Number: ', max(y))
