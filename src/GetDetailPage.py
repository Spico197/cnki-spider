import requests
from bs4 import BeautifulSoup
import time
# import codecs


def write_log(title, string):
	with open('error.log', 'a') as f:
		f.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) +
		        ' ' + title + ' ERROR: ' + string + '\n')


def get_cited_number(title, year, issue):
	cited_number = -1
	try:
		url = 'http://search.cnki.com.cn/Search.aspx?q=' + title
		re = requests.get(url)
		re.encoding = 'utf-8'
		soup = BeautifulSoup(re.text, 'lxml')
		temp_str = soup.find('span', class_='count').string
		cited_string = temp_str.split('|')[1].strip().split('（')[1]
		if cited_string == '）':
			cited_number = -1
		elif len(cited_string) >= 2:
			cited_number = cited_string.split('）')[0]
		else:
			cited_number = 0
	except:
		write_log(title, 'Cited Number Fetch Failed!')
	# TODO: Check the cited number's validity
	# check_str = soup.find('span', class_='year-count').find('span').string.split()
	# print(check_str)

	return cited_number

def get_field(filename):
	url = 'http://wap.cnki.net/touch/web/Journal/Article/' + filename + '.html'
	field = []
	re = requests.get(url)
	re.encoding = 'utf-8'
	soup = BeautifulSoup(re.text, 'lxml')
	try:
		field = [child.get_text().strip() for child in
		         soup.find('div', class_='c-card__paper-content c-card__paper-content-normal').find_all('a')]
	except:
		write_log(filename, 'Get field failed')
	return field

def get_detail_page_info(filename_list, time_sleep=2):
	print('====================== GET DETAIL PAGE INFO ======================')
	detail_infos = []
	for filename in filename_list:
		time.sleep(time_sleep)
		url = 'http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=' + filename
		detail_page = requests.get(url)
		detail_page_soup = BeautifulSoup(detail_page.text, 'lxml')
		title = ' NONE '
		try:
			title = "".join([child.string for child in detail_page_soup.find('div', class_='wxTitle').h2.children])
			author = [x.get_text().strip() for x in detail_page_soup.find('div', class_='author').find_all('a')]
			organization = [x.get_text().strip() for x in detail_page_soup.find('div', class_='orgn').find_all('a')]
			abstract = "".join([child.string for child in detail_page_soup.find('span', id='ChDivSummary').children])
			keyword = [x.get_text().split(';')[0].strip() for x in
			           [child for child in detail_page_soup.find('label', id='catalog_KEYWORD').next_siblings]]

			try:
				foundation = [x.string.strip().split('；')[0] for x in
				              detail_page_soup.find('label', id="catalog_FUND").next_siblings]
			except:
				foundation = []

			doi = detail_page_soup.find('label', id='catalog_ZCDOI').next_sibling.string
			catalogue_number = detail_page_soup.find('label', id='catalog_ZTCLS').next_sibling.string

			try:
				download = detail_page_soup.find('span', class_='a').find('b').string
				page = detail_page_soup.find('div', class_='total').find_all_next('b')[1].string
				page_number = detail_page_soup.find('div', class_='total').find_all_next('b')[2].string
				size = detail_page_soup.find('div', class_='total').find_all_next('b')[3].string
			except:
				download = []
				page = detail_page_soup.find('div', class_='total').find_all_next('b')[0].string
				page_number = detail_page_soup.find('div', class_='total').find_all_next('b')[1].string
				size = detail_page_soup.find('div', class_='total').find_all_next('b')[2].string

		except:
			write_log(title, filename)
			continue

		year = filename[4:8]
		issue = filename[8:10]
		number = filename[10:]

		detail_info = {
			'year': year,
			'issue': issue,
			'number': number,
			'title': title,
			'author': author,
			'organization': organization,
			'keyword': keyword,
			'foundation': foundation,
			'doi': doi,
			'catalogue_number': catalogue_number,
			'download_number': download,
			'page': page,
			'page_number': page_number,
			'size': size,
			'field': get_field(filename),
			'cited_number': get_cited_number(title, year, issue),
			'abstract': abstract,
		}
		detail_infos.append(detail_info)
		print('\rDetail page process : {0}/{1}'.format(filename_list.index(filename) + 1, len(filename_list)), end='')
	print('\n====================== GOT DETAIL PAGE INFO ======================')
	return detail_infos


def main():
	# filename_list = ['GZDI201706001', 'GZDI201706002']
	# details = get_detail_page_info(filename_list)
	# print(details)
	# cited_number = get_cited_number('国外电磁场教材评论', '2017', '07')
	# print(cited_number)
	# print(get_field('GZDI201706001'))
	pass


if __name__ == '__main__':
	main()
