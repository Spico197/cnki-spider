from src.CNKISpider import MagazineSpider
import pymongo
import time
import random
# from multiprocessing import Pool


client = pymongo.MongoClient('localhost', 27017)
cnki_magazine_data = client['cnki_magazine_data']
cnki_magazine_list = cnki_magazine_data['cnki_magazine_list']
filename_table = cnki_magazine_data['filename_table']
detail_info_table = cnki_magazine_data['detail_info_table']

if __name__ == '__main__':
    cnt = 0
    length_all = cnki_magazine_list.find().count()
    for item in cnki_magazine_list.find():
        base_id = item['base_id']

        cnt += 1
        print("\nMagazine Total Process: {0}/{1}: {2}-{3}\n".format(cnt, length_all, base_id, item['journal_name']))

        journal = MagazineSpider(base_id, name=item['journal_name'])

        filename_list = journal.get_filename(time_sleep=random.randint(1, 5))
        filename_table.insert_many(filename_list)
        # pool = Pool()
        print('\n====================== GET DETAIL PAGE INFO ======================')
        for filename in filename_list:
            time.sleep(random.randint(1, 5))
            detail_info = journal.get_one_detail_info(filename['filename'], timeout=1)
            if isinstance(detail_info, dict):
                detail_info_table.insert_one(detail_info)
                # print(detail_info)
            print('\rDetail page process : {0}/{1}'.format(filename_list.index(filename) + 1, len(filename_list)), end='')
        print('\n====================== GOT DETAIL PAGE INFO ======================')



        # pool.close()
        # pool.join()