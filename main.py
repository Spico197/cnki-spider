import requests
# import pymongo
from bs4 import BeautifulSoup
import time

# client = pymongo.MongoClient('localhost', 27017)
# cnki_spider = client['cnki_spider']
# year_issue_table = cnki_spider['year_issue_table']
# filename_number_table = cnki_spider['filename_table']
# detail_info_table = cnki_spider['detail_info_table']

param = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
	'Cookie': 'cnkiUserKey=b1d821c8-1e5e-90d8-33e4-1d0bc052623a; RsPerPage=20; Ecp_ClientId=1171205224100679211; ASP.NET_SessionId=tt3g42kw0arxumulgdtlmam1; SID_kcms=124113; SID_krsnew=125133; SID_kns=123122; Ecp_IpLoginFail=171223111.121.85.8; SID_klogin=125143; SID_knsdelivery=125122',
}
param_mobile = {
	'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36',
}
# url = 'http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=2017&issue=04&pykm=GZDI&pageIdx=0'

# re = requests.get(url, params=param)
# soup = BeautifulSoup(re.text, 'lxml')
# ans = soup.select('dd.row > span.name > a')

# http://navi.cnki.net/KNavi/JournalDetail?pcode=CJFD&pykm=GZDI

# year_issue_url = 'http://navi.cnki.net/KNavi/JournalDetail/GetJournalYearList?pcode=CJFD&pykm=GZDI&pIdx=0'
# year_issue = requests.get(year_issue_url, params=param)
# year_issue_soup = BeautifulSoup(year_issue.text, 'lxml')
#
# year_issue = [{'yearissue_data': x.get('id')[2:]} for x in year_issue_soup.find('div', class_='yearissuepage').find_all('a')]
# print(year_issue)
# year_issue_spider.insert_many(year_issue)

# http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=2017&issue=04&pykm=GZDI&pageIdx=0

# DONE: detailed paper list: the filename of each year and issue
re = requests.get('http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=2017&issue=04&pykm=GZDI&pageIdx=0')
soup = BeautifulSoup(re.text, 'lxml')
ans = soup.select('dd.row > span.name > a')
for an in ans:
	print(an.get('href').split('&')[-3])
"""
detail_page_url = 'http://navi.cnki.net/knavi/JournalDetail/GetArticleList?pykm=GZDI&pageIdx=0'
for year_and_issue in year_issue_table.find():
	year = str(year_and_issue['yearissue_data'])[0:4]
	issue = str(year_and_issue['yearissue_data'])[4:]
	url = detail_page_url + '&year=' + year + '&issue=' + issue

	time.sleep(60)
	detail_page = requests.get(url, params=param)
	detail_page_soup = BeautifulSoup(detail_page.text, 'lxml')

	title = detail_page_soup.select('div.c-card__title2')[0].get_text().strip()
	author = [x.get_text().strip() for x in detail_page_soup.find('div', class_='c-card__author').find_all('a')]
	organization = [x.get_text().strip() for x in detail_page_soup.select('div.c-card__paper-content')[0].find_all('a')]
	field = detail_page_soup.select('div.c-card__paper-content.c-card__paper-content-normal > a')[0].get_text().strip()
	abstract = detail_page_soup.select('div.c-card__aritcle')[0].get_text().strip()
	keyword =
	foundation = detail_page_soup.find('label', id="catalog_FUND").next_sibling.string
	detail_info = {
		'title': title,
		'author': author,
		'organization': organization,
		'field': field,
		'keyword': keyword,
		'abstract': abstract,
	}
	detail_info_table.insert_one(detail_info)
	print('\r' + str(year_and_issue['yearissue_data']), end='')
"""

# DONE: detailed page: title, name, unit, foundation, keywords, abstract use a new non-mobile page by non-css selector
# detail page:
# http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=GZDI201704001

"""
detail_page_url = 'http://wap.cnki.net/touch/web/Journal/Article/GZDI201705002.html'
detail_page = requests.get(detail_page_url, params=param_mobile)
detail_page_soup = BeautifulSoup(detail_page.text, 'lxml')

title = detail_page_soup.select('div.c-card__title2')[0].get_text().strip()
author = [x.get_text().strip() for x in detail_page_soup.find('div', class_='c-card__author').find_all('a')]
organization = [x.get_text().strip() for x in detail_page_soup.select('div.c-card__paper-content')[0].find_all('a')]
field = detail_page_soup.select('div.c-card__paper-content.c-card__paper-content-normal > a')[0].get_text().strip()
abstract = detail_page_soup.select('div.c-card__aritcle')[0].get_text().strip()
keyword = [x.get_text().strip() for x in detail_page_soup.find('div', class_='c-card__paper__info').find_all_next('div', class_='c-card__paper-item')[2].find_all('a')]
# foundation = detail_page_soup.find('label', id="catalog_FUND").next_sibling.string
detail_info = {
	'title': title,
	'author': author,
	'organization': organization,
	'field': field,
	'keyword': keyword,
	'abstract': abstract,
}
print(detail_info)
"""

'''Right Code'''
# url = 'http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=GZDI201704007'
# # url = 'http://kns.cnki.net/kcms/detail/detail.aspx?filename=JYSB201709012&dbcode=CJFQ&dbname=CJFD2017'
# detail_page = requests.get(url, params=param)
# detail_page_soup = BeautifulSoup(detail_page.text, 'lxml')
#
# title = detail_page_soup.find('div', class_='wxTitle').h2.string.strip()
# author = [x.get_text().strip() for x in detail_page_soup.find('div', class_='author').find_all('a')]
# organization = [x.get_text().strip() for x in detail_page_soup.find('div', class_='orgn').find_all('a')]
# abstract = detail_page_soup.find('span', id='ChDivSummary').string.strip()
# keyword = [x.get_text().strip().split(';')[0] for x in detail_page_soup.find('label', id='catalog_KEYWORD').next_siblings]
# foundation = [x.string.strip().split('；')[0] for x in detail_page_soup.find('label', id="catalog_FUND").next_siblings]
# doi = detail_page_soup.find('label', id='catalog_ZCDOI').next_sibling.string
# catalogue_number = detail_page_soup.find('label', id='catalog_ZTCLS').next_sibling.string
# download = detail_page_soup.find('div', class_='total').find_all_next('b')[0].string
# page = detail_page_soup.find('div', class_='total').find_all_next('b')[1].string
# page_number = detail_page_soup.find('div', class_='total').find_all_next('b')[2].string
# size = detail_page_soup.find('div', class_='total').find_all_next('b')[3].string
#
# detail_info = {
# 	'title': title,
# 	'author': author,
# 	'organization': organization,
# 	'keyword': keyword,
# 	'foundation': foundation,
# 	'doi': doi,
# 	'catalogue_number': catalogue_number,
# 	'download_number': download,
# 	'page': page,
# 	'page_number': page_number,
# 	'size': size,
# 	'abstract': abstract,
# }
# print(detail_info)

# TODO: Encapsulation to def of getyearissuelist(pcode, pykm)
# TODO: Encapsulation to def of getfilelist(year, issue)
# TODO: Encapsulation to def of getdetail(filename)
