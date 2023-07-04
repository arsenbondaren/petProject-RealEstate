from sqlalchemy import create_engine
import pandas as pd

eng_cols = {'cena':'price', 'powierzchnia':'area', 'liczba pokoi':'rooms', 'stan wykończenia':'renovation',
            'piętro':'floor', 'rynek':'market', 'winda':'elevator', 'ulica':'street', 'dzielnica':'district',
            'balkon':'balcony', 'taras':'terrace', 'ogródek':'garden', 'ogrzewanie_miejskie':'central_heating',
            'sprzedawca':'seller', 'dzisiaj':'today', 'data_dodania':'publication_date'}

engine = create_engine('sqlite:///instance/test_flat.db', echo=False)
df = pd.read_csv('db_waw_flats.csv', parse_dates=['dzisiaj', 'data_dodania'])
df.rename(columns=eng_cols, inplace=True)
df.to_sql(name='flats_load', con=engine, index_label='id', if_exists='replace')