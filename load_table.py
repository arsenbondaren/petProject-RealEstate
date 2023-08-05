from sqlalchemy import create_engine
import pandas as pd
import preprocess
import sqlite3

con = sqlite3.connect("instance/test_flat.db")
max_index = con.execute("SELECT id FROM price_metric ORDER BY id DESC").fetchone()[0]
con.close()

eng_cols = {'cena':'price', 'powierzchnia':'area', 'liczba pokoi':'rooms', 'stan wykończenia':'renovation',
            'piętro':'floor', 'rynek':'market', 'winda':'elevator', 'ulica':'street', 'dzielnica':'district',
            'balkon':'balcony', 'taras':'terrace', 'ogródek':'garden', 'ogrzewanie_miejskie':'central_heating',
            'sprzedawca':'seller', 'dzisiaj':'today', 'data_dodania':'publication_date'}

engine = create_engine('sqlite:///instance/test_flat.db', echo=False)
table_name = 'waw_flats_3_8.csv'
df = pd.read_csv('datasets/'+table_name, parse_dates=['dzisiaj', 'data_dodania'])
df = preprocess.preproc_data(df)
cols_for_db = ['cena', 'powierzchnia', 'liczba pokoi', 'stan wykończenia', 'piętro', 'rynek', 'winda', 'ulica',
                'dzielnica', 'balkon', 'taras', 'ogródek', 'parking', 'ogrzewanie_miejskie', 'sprzedawca', 'blok',
                'cena_m', 'dzisiaj', 'data_dodania']
df = df[cols_for_db]
df.rename(columns=eng_cols, inplace=True)
gr_df = pd.DataFrame(df.groupby(by=['today'], as_index=False)['cena_m'].mean())
df.to_csv('datasets/db_'+table_name, index=False)
df.to_sql(name='flats_load', con=engine, index_label='id', if_exists='replace')

gr_df.rename(columns={'today':'date','cena_m':'price_m2'}, inplace=True)
gr_df.rename(index={0:max_index+1}, inplace=True)
gr_df.to_sql(name='price_metric', con=engine, index_label='id', if_exists='append')