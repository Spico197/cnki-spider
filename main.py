import requests
import pymongo
from bs4 import BeautifulSoup
import time

client = pymongo.MongoClient('localhost', 27017)
cnki_spider = client['cnki_spider']
year_issue_table = cnki_spider['year_issue_table']
paper_number_table = cnki_spider['filename_table']
detail_info_table = cnki_spider['detail_info_table']


class MagazineSpider(object):
	def __init__(self, pcode, pykm, year_issue_table, paper_number_table, detail_info_table):
		self.pcode = pcode
		self.pykm = pykm
		# self.year_issue_data = {}
		# self.paper_number_data = {}
		self.param = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
			'Cookie': 'cnkiUserKey=b1d821c8-1e5e-90d8-33e4-1d0bc052623a; RsPerPage=20; Ecp_ClientId=1171205224100679211; ASP.NET_SessionId=tt3g42kw0arxumulgdtlmam1; SID_kcms=124113; SID_krsnew=125133; SID_kns=123122; Ecp_IpLoginFail=171223111.121.85.8; SID_klogin=125143; SID_knsdelivery=125122',
		}
		self.param_mobile = {
			'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36',
		}

	def get_detail_page_info(self, paper_number):
		url = 'http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=' + paper_number
		detail_page = requests.get(url, params=self.param)
		detail_page_soup = BeautifulSoup(detail_page.text, 'lxml')
		title = ' NONE '
		try:
			title = "".join([child.string for child in detail_page_soup.find('div', class_='wxTitle').h2.children])
			author = [x.get_text().strip() for x in detail_page_soup.find('div', class_='author').find_all('a')]
			organization = [x.get_text().strip() for x in detail_page_soup.find('div', class_='orgn').find_all('a')]
			abstract = "".join([child.string for child in detail_page_soup.find('span', id='ChDivSummary').children])
			keyword = [x.get_text().split(';')[0].strip() for x in [child for child in detail_page_soup.find('label', id='catalog_KEYWORD').next_siblings]]

			try:
				foundation = [x.string.strip().split('；')[0] for x in detail_page_soup.find('label', id="catalog_FUND").next_siblings]
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
			print(paper_number)
			with open('log.txt', 'a') as f:
				f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + title + ' ERROR: ' + paper_number + '\n')
			return

		year = paper_number[4:8]
		issue = paper_number[8:10]
		number = paper_number[10:]

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
			'abstract': abstract,
		}
		# print(detail_info)
		detail_info_table.insert_one(detail_info)

	def get_paper_number_list(self, yearissue, pageIdx=0):
		year = yearissue[0:4]
		issue = yearissue[4:]
		url = 'http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=' + year + '&issue=' + issue + '&pykm=' + str(self.pykm) + '&pageIdx=' + str(pageIdx)
		re = requests.get(url, params=self.param)
		soup = BeautifulSoup(re.text, 'lxml')
		ans = soup.select('dd.row > span.name > a')
		paper_number = [{'paper_number': an.get('href').split('&')[-3].split('=')[-1]} for an in ans]
		# print(paper_number)
		paper_number_table.insert_many(paper_number)
		# self.paper_number_data = paper_number

	def get_year_issue_list(self, pageIdx=0):
		year_issue_url = 'http://navi.cnki.net/KNavi/JournalDetail/GetJournalYearList?pcode=' + self.pcode + '&pykm=' + self.pykm + '&pIdx=' + str(pageIdx)
		year_issue = requests.get(year_issue_url, params=self.param)
		year_issue_soup = BeautifulSoup(year_issue.text, 'lxml')

		year_issue = [{'yearissue': str(x.get('id')[2:])} for x in year_issue_soup.find('div', class_='yearissuepage').find_all('a')]
		# print(year_issue)
		year_issue_table.insert_many(year_issue)
		# self.year_issue_data = year_issue


def main():
	spider = MagazineSpider('CJFD', 'GZDI', year_issue_table, paper_number_table, detail_info_table)
	"""
	spider.get_year_issue_list()
	# get all the paper number through year and issue
	yearissue = [yearissue['yearissue'] for yearissue in year_issue_table.find()]
	for yearissue_temp in yearissue:
		time.sleep(5)
		spider.get_paper_number_list(yearissue_temp)
		print('\r' + str(yearissue.index(yearissue_temp)+1) + '/' + str(len(yearissue)), end='')
	"""

	# TODO: get all the detail info
	filename_list = [filename_table['paper_number'] for filename_table in paper_number_table.find()]
	for filename in filename_list:
		# time.sleep(5)
		spider.get_detail_page_info(filename)
		print('\r' + str(filename_list.index(filename) + 1) + '/' + str(len(filename_list)), end='')


if __name__ == '__main__':
	main()
