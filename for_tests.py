import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///instance/test_flat.db', echo=False)
#df1 = pd.read_csv('datasets/db_waw_flats.csv', parse_dates = ['today', 'publication_date'])
#df2 = pd.read_csv('datasets/db_waw_flats_17_06.csv', parse_dates = ['today', 'publication_date'])
#df3 = pd.read_csv('datasets/db_waw_flats_27_6.csv', parse_dates = ['today', 'publication_date'])
#df4 = pd.read_csv('datasets/db_waw_flats_10_7.csv', parse_dates = ['today', 'publication_date'])
#df5 = pd.read_csv('datasets/db_waw_flats_27_7.csv', parse_dates = ['today', 'publication_date'])
#common_df = pd.concat([df1,df2,df3,df4,df5], ignore_index=True)
#gr_df = pd.DataFrame(common_df.groupby(by=['today'], as_index=False)['cena_m'].mean())
#gr_df.rename(columns={'today':'date','cena_m':'price_m2'}, inplace=True)
#gr_df.to_sql(name='price_metric', con=engine, index_label='id', if_exists='append')
import sqlite3
con = sqlite3.connect("instance/test_flat.db")
#con.execute("DELETE FROM price_metric")
#con.commit()
res = con.execute("SELECT * FROM price_metric ORDER BY id DESC").fetchone()
print(res[0] == 4)