from sqlalchemy import create_engine
from catboost import CatBoostRegressor, Pool
import pandas as pd
import preprocess
import sqlite3
import pickle
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, mean_absolute_error

con = sqlite3.connect("instance/test_flat.db")
max_index = con.execute("SELECT id FROM price_metric ORDER BY id DESC").fetchone()[0]
con.close()

#eng_cols = {'cena':'price', 'powierzchnia':'area', 'liczba pokoi':'rooms', 'stan wykończenia':'renovation',
#            'piętro':'floor', 'rynek':'market', 'winda':'elevator', 'ulica':'street', 'dzielnica':'district',
#            'balkon':'balcony', 'taras':'terrace', 'ogródek':'garden', 'ogrzewanie_miejskie':'central_heating',
#            'sprzedawca':'seller', 'dzisiaj':'today', 'data_dodania':'publication_date'}

def final_tables(df, table_name):
    engine = create_engine('sqlite:///instance/test_flat.db', echo=False)
    #table_name = 'waw_flats_4_9.csv'
    #df = pd.read_csv('datasets/'+table_name, parse_dates=['dzisiaj', 'data_dodania'])
    df = preprocess.preproc_data(df)
#cols_for_db = ['cena', 'powierzchnia', 'liczba pokoi', 'stan wykończenia', 'piętro', 'rynek', 'winda', 'ulica',
#                'dzielnica', 'balkon', 'taras', 'ogródek', 'parking', 'ogrzewanie_miejskie', 'sprzedawca', 'blok',
#                'cena_m', 'dzisiaj', 'data_dodania']
#df = df[cols_for_db]
#df.rename(columns=eng_cols, inplace=True)
    df.to_csv('datasets/db_'+table_name, index=False)
    df.to_sql(name='flats_load', con=engine, index_label='id', if_exists='replace')
# Calculate mean price per m2
    gr_df = pd.DataFrame(df.groupby(by=['today'], as_index=False)['cena_m'].mean())
    gr_df.rename(columns={'today':'date','cena_m':'price_m2'}, inplace=True)
    gr_df.rename(index={0:max_index+1}, inplace=True)
    gr_df['date'] = gr_df['date'].values.astype('datetime64[us]')
    gr_df.to_sql(name='price_metric', con=engine, index_label='id', if_exists='append')
    print('Two tables successful loaded')
    return df


def print_errors(y_true, preds):
    print('percentage error', mean_absolute_percentage_error(y_true, preds))
    print('absolute error', mean_absolute_error(y_true, preds))
    print('root squared error', mean_squared_error(y_true, preds, squared=False))
    return None


# learning catboost regressor (from existing model)
def learn_catboost(df):
    cb_regressor = CatBoostRegressor().load_model("cb_model.cbm")
    le = pickle.load(open('district_encode', 'rb'))
    df.drop(columns=['today'], inplace=True)

    cols_x = ['district', 'area', 'rooms', 'renovation', 'floor', 'balcony', 'terrace',
            'garden', 'parking', 'central_heating', 'market', 'seller', 'blok', 'elevator']

    cat_cols = ['district', 'renovation', 'floor', 'balcony', 'terrace', 'garden', 'parking',
                'central_heating', 'market', 'seller', 'blok', 'elevator']

    col_y = ['price']
    model_df = df[cols_x + col_y].dropna()
    model_df['district'] = le.transform(model_df['district'])
    pool = Pool(model_df[cols_x], cat_features=cat_cols)
    old_preds = cb_regressor.predict(pool)
    print('Before fit')
    print_errors(model_df['price'], old_preds)
    train_pool = Pool(model_df[cols_x], model_df['price'], cat_features=cat_cols)
    cb_regressor.fit(train_pool, init_model=cb_regressor, silent=True)
    new_preds = cb_regressor.predict(pool)
    print('After fit')
    print_errors(model_df['price'], new_preds)
    cb_regressor.save_model('cb_model.cbm')
    print("The catboost's weights successfully updated")
    return None

if __name__ == '__main__':
    print('Manually load tables')
    table_name = 'waw_flats_14_9.csv'
    df = pd.read_csv('datasets/' + table_name, parse_dates=['dzisiaj', 'data_dodania'])
    final_tables(df, table_name)