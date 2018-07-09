import requests
from bs4 import BeautifulSoup
import time

header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
					AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 \
					Safari/537.36',
}
product_code = 'CJFD'  # catalogue number -> pcode
base_id = 'GZDI'


def get_year_list(base_id):
	print('====================== GET THE YEAR LIST ======================')
	url = 'http://wap.cnki.net/touch/web/Journal/Year/' + base_id + '.html'
	re = requests.get(url)
	re.encoding = 'utf-8'
	soup = BeautifulSoup(re.text, 'lxml')

	year_list = []
	soup_list = soup.find('section', class_='classify past').find_all('a')
	for x in soup_list:
		if int(x.get_text()) > 0:
			year_list.append(int(x.get_text()))
		print('\rYear list process : {0}/{1}'
		      .format(soup_list.index(x)+1, len(soup_list)), end='')
	print('\nThe length of year list is : ', len(year_list))
	print('====================== GOT THE YEAR LIST ======================')
	return year_list


def get_year_issue_list(year_list, base_id, time_sleep=2):
	print('====================== GET THE YEAR ISSUE LIST ======================')
	year_issue_list = []
	for year in year_list:
		time.sleep(time_sleep)
		url = 'http://wap.cnki.net/touch/web/Journal/Period/' + base_id + str(year) + '.html'
		re = requests.get(url)
		re.encoding = 'utf-8'
		soup = BeautifulSoup(re.text, 'lxml')
		soup_list = soup.find('section', class_='classify past').find_all('span')
		for x in soup_list:
			year_issue_temp = str(year) + x.get_text().strip()
			year_issue_list.append(year_issue_temp)
		print('\rProcess : Year: {0}/{1}'
		      .format(year_list.index(year)+1,len(year_list)),
		      end='')
	print('\nThe length of year issue list is : ', len(year_issue_list))
	print('====================== GOT THE YEAR ISSUE LIST ======================')
	return year_issue_list


def get_filename_list(year_issue_list, base_id, page_index=0, time_sleep=2):
	print('====================== GET THE FILENAME LIST ======================')
	filename_list = []
	for year_issue_temp in year_issue_list:
		time.sleep(time_sleep)
		year = year_issue_temp[0:4]
		issue = year_issue_temp[4:]
		url = 'http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=' + year + \
		      '&issue=' + issue + '&pykm=' + base_id + '&pageIdx=' + str(page_index)
		re = requests.get(url)
		soup = BeautifulSoup(re.text, 'lxml')
		ans = soup.select('dd.row > span.name > a')
		filename_list.extend([{'paper_number': an.get('href').split('&')[-3].split('=')[-1]} for an in ans])
		print('\rFilename list process : {0}/{1}'
		      .format(year_issue_list.index(year_issue_temp)+1,len(year_issue_list)), end='')
	print('\nThe length of filename list is : ', len(filename_list))
	print('====================== GOT THE FILENAME LIST ======================')
	return filename_list


def get_filename(base_id, time_sleep=2):
	year_list = get_year_list(base_id)
	year_issue_list = get_year_issue_list(year_list, base_id, time_sleep=time_sleep)
	filename_list = get_filename_list(year_issue_list, base_id, time_sleep=time_sleep)
	return filename_list

def main():
	filename_list = get_filename(base_id)
	print(filename_list)

if __name__ == '__main__':
	main()
