import requests
from bs4 import BeautifulSoup

header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
					AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 \
					Safari/537.36',
}
product_code = 'CJFD'  # catalogue number -> pcode

# base_id = input('The BaseID of the Magazine:\n')
# url = 'http://navi.cnki.net/knavi/JournalDetail?pcode=CJFD&pykm=' + url
base_id = 'GZDI'
url = 'http://wap.cnki.net/touch/web/Journal/Year/' + base_id + '.html'

re = requests.get(url)
re.encoding = 'utf-8'
soup = BeautifulSoup(re.text, 'lxml')

year_list = []
for x in soup.find('section', class_='classify past').find_all('a'):
	if int(x.get_text()) > 0:
		year_list.append(int(x.get_text()))

print(year_list)

issue_list = []
issue_urls = ['http://wap.cnki.net/touch/web/Journal/Period/GZDI' + str(x) + '.html' for x in year_list]
for issue_url in issue_urls[0:1]:
	re = requests.get(url)
	re.encoding = 'utf-8'
	soup = BeautifulSoup(re.text, 'lxml')
	for x in soup.find('section', class_='classify past').find_all('span'):
		print(x)

print(issue_list)

