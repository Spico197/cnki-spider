from bs4 import BeautifulSoup
import codecs
import pymongo

client = pymongo.MongoClient('localhost', 27017)
cnki_magazine_data = client["cnki_magazine_data"]
cnki_magazine_list = cnki_magazine_data["cnki_magazine_list"]

"""
if u'd like to crawl it urself, the url is shown as below
    url = "http://navi.cnki.net/knavi/Common/Search/Journal?displaymode=2&pageindex=1&pagecount=20000&index=1&random=0.0001&SearchStateJson={%22StateID%22:%22%22,%22Platfrom%22:%22%22,%22QueryTime%22:%22%22,%22Account%22:%22knavi%22,%22ClientToken%22:%22%22,%22Language%22:%22%22,%22CNode%22:{%22PCode%22:%22CJFD%22,%22SMode%22:%22%22,%22OperateT%22:%22%22},%22QNode%22:{%22SelectT%22:%22%22,%22Select_Fields%22:%22%22,%22S_DBCodes%22:%22%22,%22QGroup%22:[{%22Key%22:%22group%22,%22Logic%22:1,%22Items%22:[],%22ChildItems%22:[]}],%22OrderBy%22:%22OTA|DESC%22,%22GroupBy%22:%22%22,%22Additon%22:%22%22}}"
"""
def get_magazine_list_page(url=False, from_file=True, path=""):
    """
    get the magazine list page from file or from url
    :param url: take False as default, function updating
    :param from_file: if from_file, the BeautifulSoup will load a native html page, take True as default
    :param path: file or url path
    :return: the page text
    """
    if from_file:
        with codecs.open(path, "r", encoding="utf-8") as f:
            html = "".join(f.readlines())
            # print(html)
            return html
    elif url:
        # re = requests.get(path)
        # re.encoding = 'utf-8'
        # return re.text
        pass


def get_data(soup):
    """
    get the detailed magazine list data
    :param soup: the BeautifulSoup's data type, as soup = BeautifulSoup(html, 'lxml')
    :return: a iterator as "yield" returns
    """
    journals = soup.find_all("span", class_="tab_1")[1:]
    sponsors = soup.find_all("span", class_="tab_2")[1:]
    compound_influence_factors = soup.find_all("span", class_="tab_3")[1:]
    integrated_influence_factors = soup.find_all("span", class_="tab_4")[1:]
    cited_numbers = soup.find_all("span", class_="tab_5")[1:]

    for journal, sponsor, compound_influence_factor, integrated_influence_factor, cited_number \
            in zip(journals, sponsors, compound_influence_factors, integrated_influence_factors, cited_numbers):
        journal_name = journal.h2.a.string
        journal_baseid = journal.h2.a.get("href").split("=")[-1]
        data = {
            "journal_name": journal_name,
            "base_id": journal_baseid,
            "sponsor": sponsor.string,
            "compound_influence_factor": compound_influence_factor.string,
            "integrated_influence_factors": integrated_influence_factor.string,
            "cited_numbers": cited_number.string,
        }
        yield data

if __name__ == '__main__':
    html = get_magazine_list_page(path="../data/html_preload/JournalList.html")
    soup = BeautifulSoup(html, "lxml")
    length = len(list(soup.find_all("span", class_="tab_1")[1:]))
    cnt = 1
    for item in get_data(soup):
        # cnki_magazine_list.insert_one(item)   # switch to activate the database operation
        print("\rProcess: {0}/{1}, Name={2:50}".format(cnt, length, item['journal_name']), end="")
        cnt += 1
