import pandas as pd
import pymongo

client = pymongo.MongoClient('localhost', 27017)
cnki_gzdi_data = client['cnki_gzdi_data']
detail_info_table = cnki_gzdi_data['detail_info_table']

df = pd.DataFrame(list(detail_info_table.find()))
del df['_id']
df.to_csv('data.csv')
