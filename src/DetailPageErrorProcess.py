from .CNKISpider import MagazineSpider
import time
import pymongo
import codecs

client = pymongo.MongoClient('localhost', 27017)
cnki_gzdi_data = client['cnki_gzdi_data']
filename_table = cnki_gzdi_data['filename_table']
detail_info_table = cnki_gzdi_data['detail_info_table']

base_id = 'GZDI'
gzdi = MagazineSpider(base_id)

# with open('errorProcess.txt', 'r', encoding='utf-8') as f:
# 	lines = f.readlines()
#
# for line in lines:
# 	filename = line.split()[-1]
# 	if 'NONE' in line:
# 		detail_info = gzdi.get_one_detail_info(filename)
# 		if isinstance(detail_info, dict):
# 			detail_info_table.insert_one(detail_info)
# 	elif 'field' in line:
# 		field = gzdi.get_field(filename)
# 		year = filename[4:8]
# 		issue = filename[8:10]
# 		num = filename[10:]
# 		less_field = detail_info_table.update({'year':year, 'issue': issue, 'number': num},
# 		                                      {'$set': {'field': field}})
# 	else:
# 		with open('errorProcess.log', 'a') as f:
# 			f.writelines(filename)
#
# with open('errorProcess.log', 'r', encoding='utf-8') as f:
# 	lines = f.readlines()
#
# for filename in lines:
# 	detail_info = gzdi.get_one_detail_info(filename)
# 	if isinstance(detail_info, dict):
# 		detail_info_table.insert_one(detail_info)

# with open('errorProcess.txt', 'r', encoding='utf-8') as f:
# 	lines = f.readlines()

# for line in lines:
# 	if line == '\n':
# 		continue
# 	filename = line.split()[-1]
# 	if 'field' in line:
# 		field = gzdi.get_field(filename)
# 		year = filename[4:8]
# 		issue = filename[8:10]
# 		num = filename[10:]
# 		temp = detail_info_table.find_one({'year': year, 'issue': issue, 'number': num  + '\n'})
# 		less_field = detail_info_table.update_one({'_id': temp['_id']},
# 		                                      {'$set': {'field': field}}, upsert=False)
# 		# print([x['title'] for x in temp])
# 		print('{0}/{1}'.format(lines.index(line), len(lines)))
# 	else:
# 		with open('errorProcess.log', 'a') as f:
# 			f.writelines(filename)
