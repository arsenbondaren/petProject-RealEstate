from sqlalchemy import create_engine
import pandas as pd
import preprocess

eng_cols = {'cena':'price', 'powierzchnia':'area', 'liczba pokoi':'rooms', 'stan wykończenia':'renovation',
            'piętro':'floor', 'rynek':'market', 'winda':'elevator', 'ulica':'street', 'dzielnica':'district',
            'balkon':'balcony', 'taras':'terrace', 'ogródek':'garden', 'ogrzewanie_miejskie':'central_heating',
            'sprzedawca':'seller', 'dzisiaj':'today', 'data_dodania':'publication_date'}

engine = create_engine('sqlite:///instance/test_flat.db', echo=False)
table_name = 'waw_flats_27_6.csv'
df = pd.read_csv('datasets/'+table_name, parse_dates=['dzisiaj', 'data_dodania'])
df = preprocess.preproc_data(df)
cols_for_db = ['cena', 'powierzchnia', 'liczba pokoi', 'stan wykończenia', 'piętro', 'rynek', 'winda', 'ulica',
                'dzielnica', 'balkon', 'taras', 'ogródek', 'parking', 'ogrzewanie_miejskie', 'sprzedawca', 'blok',
                'cena_m', 'dzisiaj', 'data_dodania']
df = df[cols_for_db]
df.rename(columns=eng_cols, inplace=True)
df.to_csv('datasets/db_'+table_name, index=False)
df.to_sql(name='flats_load', con=engine, index_label='id', if_exists='replace')