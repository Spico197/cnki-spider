import pymongo
import matplotlib.pyplot as plt
import matplotlib as mpl

font_msyh = mpl.font_manager.FontProperties(fname="msyh.ttc")
mpl.rcParams['axes.unicode_minus'] = False

client = pymongo.MongoClient('localhost', 27017)
cnki_gzdi_data = client['cnki_gzdi_data']
detail_info_table = cnki_gzdi_data['detail_info_table']

download_number = [x['download_number'] for x in detail_info_table.find()]
for i in range(len(download_number)):
	if isinstance(download_number[i], str):
		download_number[i] = int(download_number[i])
	else:
		download_number[i] = 0
# print(download_number)
total_download_number = sum(download_number)
print('Total download number: ', total_download_number)
print('Max download number: ', max(download_number))
x = detail_info_table.find_one({'download_number': str(max(download_number))})
max_download_title = x['title']
print(max_download_title)

page_number = [x['page_number'] for x in detail_info_table.find()]
for i in range(len(page_number)):
	if isinstance(page_number[i], str):
		page_number[i] = int(page_number[i])
	else:
		page_number[i] = 0
# print(page_number)
total_page_number = sum(page_number)
print('Total page number: ', total_page_number)
print('Max page number: ', max(page_number))
x = detail_info_table.find_one({'page_number': str(max(page_number))})
max_page_title = x['title']
print(max_page_title)


new_download_number = []
for x in download_number:
	if x > 500:
		x = 3
	elif x > 100 and x <= 500:
		x = 2
	elif x > 50 and x <= 100:
		x = 1
	else:
		x = 0
	new_download_number.append(x)

plt.style.use('ggplot')
fig = plt.figure()
# plt.hist(new_download_number, bins=4)
plt.pie([new_download_number.count(0), new_download_number.count(1),
         new_download_number.count(2), new_download_number.count(3)],
        explode=(0.05, 0, 0, 0), labels=('<= 50', '50~100', '100~500', '> 500'),
        autopct='%.2f%%', shadow=False)
plt.axis('equal')
plt.title('Download Number Distribution', fontsize=14, fontweight='bold')
plt.savefig('pics/download.png', transparent=True)
plt.show()

new_page_number = []
for x in page_number:
	if x > 10:
		x = 3
	elif x > 5 and x <= 10:
		x = 2
	elif x > 3 and x <= 5:
		x = 1
	else:
		x = 0
	new_page_number.append(x)

plt.style.use('ggplot')
fig = plt.figure()
# plt.hist(new_download_number, bins=4)
plt.pie([new_page_number.count(0), new_page_number.count(1),
         new_page_number.count(2), new_page_number.count(3)],
        explode=(0, 0.05, 0, 0), labels=('<= 3', '3~5', '5~10', '> 10'),
        autopct='%.2f%%', shadow=False)
plt.axis('equal')
plt.title('Page Number Distribution', fontsize=14, fontweight='bold')
plt.savefig('pics/page.png', transparent=True)
plt.show()