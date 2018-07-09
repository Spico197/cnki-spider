import requests
from bs4 import BeautifulSoup
import time
import random

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
}

proxy_list = [
    "http://119.28.50.37:82",
    "http://218.107.137.197:8080",
    "http://39.134.68.25:80",
    "http://39.108.97.146:8888",
    "http://39.134.68.24:80",
]

class MagazineSpider(object):
    def __init__(self, base_id, product_code='CJFD', name=""):
        self.base_id = base_id
        self.name = name
        self.product_code = product_code
        self.year_list = []
        self.year_issue_list = []
        self.filename_list = []

    def get_year_list(self):
        print('====================== GET THE YEAR LIST ======================')
        url = 'http://wap.cnki.net/touch/web/Journal/Year/' + self.base_id + '.html'
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': proxy_ip}
        re = requests.get(url, proxies=proxies)
        re.encoding = 'utf-8'
        soup = BeautifulSoup(re.text, 'lxml')

        year_list = []
        soup_list = soup.find('section', class_='classify past').find_all('a')
        for x in soup_list:
            if x.get_text() != "网络首发" and int(x.get_text()) > 0:
                year_list.append(int(x.get_text()))
            print('\rYear list process : {0}/{1}'
                  .format(soup_list.index(x) + 1, len(soup_list)), end='')
        print('\nThe length of year list is : ', len(year_list))
        print('====================== GOT THE YEAR LIST ======================')
        return year_list

    def get_year_issue_list(self, year_list, time_sleep=2):
        print('====================== GET THE YEAR ISSUE LIST ======================')
        year_issue_list = []
        for year in year_list:
            time.sleep(time_sleep)
            url = 'http://wap.cnki.net/touch/web/Journal/Period/' + self.base_id + str(year) + '.html'
            proxy_ip = random.choice(proxy_list)
            proxies = {'http': proxy_ip}
            re = requests.get(url, proxies=proxies)
            re.encoding = 'utf-8'
            soup = BeautifulSoup(re.text, 'lxml')
            soup_list = soup.find('section', class_='classify past').find_all('span')
            for x in soup_list:
                year_issue_temp = str(year) + x.get_text().strip()
                year_issue_list.append(year_issue_temp)
            print('\rProcess : Year: {0}/{1}'
                  .format(year_list.index(year) + 1, len(year_list)),
                  end='')
        print('\nThe length of year issue list is : ', len(year_issue_list))
        print('====================== GOT THE YEAR ISSUE LIST ======================')
        return year_issue_list

    def get_filename_list(self, year_issue_list, page_index=0, time_sleep=2):
        print('====================== GET THE FILENAME LIST ======================')
        filename_list = []
        for year_issue_temp in year_issue_list:
            time.sleep(time_sleep)
            year = year_issue_temp[0:4]
            issue = year_issue_temp[4:]
            url = 'http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=' + year + \
                  '&issue=' + issue + '&pykm=' + self.base_id + '&pageIdx=' + str(page_index)
            proxy_ip = random.choice(proxy_list)
            proxies = {'http': proxy_ip}
            re = requests.get(url, headers=headers, proxies=proxies)
            soup = BeautifulSoup(re.text, 'lxml')
            ans = soup.select('dd.row > span.name > a')
            filename_list.extend([{'filename': an.get('href').split('&')[-3].split('=')[-1]} for an in ans])
            print('\rFilename list process : {0}/{1}'
                  .format(year_issue_list.index(year_issue_temp) + 1, len(year_issue_list)), end='')
        print('\nThe length of filename list is : ', len(filename_list))
        print('====================== GOT THE FILENAME LIST ======================')
        return filename_list

    def get_filename(self, time_sleep=2):
        self.year_list = self.get_year_list()
        self.year_issue_list = self.get_year_issue_list(self.year_list, time_sleep=time_sleep)
        self.filename_list = self.get_filename_list(self.year_issue_list, time_sleep=time_sleep)
        return self.filename_list

    def write_log(self, title, string):
        try:
            with open('error.log', 'a') as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                        ' ' + title.encode('gbk', 'ignore').decode('gbk') + ' ERROR: ' + string.encode('gbk',
                                                                                                       'ignore').decode(
                    'gbk') + '\n')
        except:
            print(title.encode('gbk', 'ignore').decode('gbk'), 'ERROR', string.encode('gbk', 'ignore').decode('gbk'))

    def get_cited_number(self, title, year, issue):
        cited_number = -1
        try:
            url = 'http://search.cnki.com.cn/Search.aspx?q=' + title
            proxy_ip = random.choice(proxy_list)
            proxies = {'http': proxy_ip}
            re = requests.get(url, headers=headers, proxies=proxies)
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
            self.write_log(title, 'Cited Number Fetch Failed!')
        # TODO: Check the cited number's validity
        # check_str = soup.find('span', class_='year-count').find('span').string.split()
        # print(check_str)

        return cited_number

    def get_field(self, filename, timeout=3):
        url = 'http://wap.cnki.net/touch/web/Journal/Article/' + filename + '.html'
        field = []
        try:
            proxy_ip = random.choice(proxy_list)
            proxies = {'http': proxy_ip}
            re = requests.get(url, proxies=proxies, timeout=timeout)
            re.encoding = 'utf-8'
            soup = BeautifulSoup(re.text, 'lxml')
            field = [child.get_text().strip() for child in
                     soup.find('div', class_='c-card__paper-content c-card__paper-content-normal').find_all('a')]
        except:
            self.write_log('Get field failed', filename)
        return field

    def get_detail_page_info(self, filename_list, time_sleep=2, dict_flag=False):
        print('====================== GET DETAIL PAGE INFO ======================')
        detail_infos = []
        for filename in filename_list:
            time.sleep(time_sleep)
            if dict_flag:
                filename = filename['filename']
            url = 'http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=' + filename
            proxy_ip = random.choice(proxy_list)
            proxies = {'http': proxy_ip}
            detail_page = requests.get(url, headers=headers, proxies=proxies)
            detail_page_soup = BeautifulSoup(detail_page.text, 'lxml')
            title = ' NONE '
            try:
                title = "".join([child.string for child in detail_page_soup.find('div', class_='wxTitle').h2.children])
                author = [x.get_text().strip() for x in detail_page_soup.find('div', class_='author').find_all('a')]
                organization = [x.get_text().strip() for x in detail_page_soup.find('div', class_='orgn').find_all('a')]
                abstract = "".join(
                    [child.string for child in detail_page_soup.find('span', id='ChDivSummary').children])
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
                self.write_log(title, filename)
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
                'field': self.get_field(filename),
                'cited_number': self.get_cited_number(title, year, issue),
                'abstract': abstract,
            }
            detail_infos.append(detail_info)
            print('\rDetail page process : {0}/{1}'.format(filename_list.index(filename) + 1, len(filename_list)),
                  end='')
        print('\n====================== GOT DETAIL PAGE INFO ======================')
        return detail_infos

    def get_one_detail_info(self, filename, timeout=3):
        url = 'http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=' + filename
        title = ' NONE '
        try:
            proxy_ip = random.choice(proxy_list)
            proxies = {'http': proxy_ip}
            detail_page = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            detail_page_soup = BeautifulSoup(detail_page.text, 'lxml')
            title = "".join([child.string for child in detail_page_soup.find('div', class_='wxTitle').h2.children])
            author = [x.get_text().strip() for x in detail_page_soup.find('div', class_='author').find_all('a')]
            organization = [x.get_text().strip() for x in detail_page_soup.find('div', class_='orgn').find_all('a')]
            temp = [child.string for child in detail_page_soup.find('span', id='ChDivSummary').children]
            if None in temp:
                temp.remove(None)
            abstract = "".join(temp)
            try:
                keyword = [x.get_text().split(';')[0].strip() for x in
                           [child for child in detail_page_soup.find('label', id='catalog_KEYWORD').next_siblings]]
            except:
                keyword = []
            try:
                foundation = [x.string.strip().split('；')[0] for x in
                              detail_page_soup.find('label', id="catalog_FUND").next_siblings]
            except:
                foundation = []

            # doi = detail_page_soup.find('label', id='catalog_ZCDOI').next_sibling.string
            # catalogue_number = detail_page_soup.find('label', id='catalog_ZTCLS').next_sibling.string

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
            self.write_log(title, filename)
            return None

        year = filename[4:8]
        issue = filename[8:10]
        number = filename[10:]

        detail_info = {
            'base_id': self.base_id,
            'name': self.name,
            'year': year,
            'issue': issue,
            'number': number,
            'title': title,
            'author': author,
            'organization': organization,
            'keyword': keyword,
            'foundation': foundation,
            # 'doi': doi,
            # 'catalogue_number': catalogue_number,
            'download_number': download,
            'page': page,
            'page_number': page_number,
            'size': size,
            'field': self.get_field(filename, timeout=timeout),
            # 'cited_number': self.get_cited_number(title, year, issue),
            'abstract': abstract,
        }
        return detail_info
