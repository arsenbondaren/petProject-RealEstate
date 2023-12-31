import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime
import load_table
import pickle

today = datetime.date.today()
day = str(today.day)
month = str(today.month)
headers = {'User-Agent': 'Mozilla/5.0'}
links = []
for page in range(1, 400):
    answer = requests.get('https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?page=' + str(page),
                          headers=headers)
    soup = BeautifulSoup(answer.text, "html.parser")
    try:
        flats_str = soup.find('script', attrs={'id': '__NEXT_DATA__'}).text
    except:
        print(f'Error on page {page}')
        continue

    flats_dict = json.loads(flats_str)
    flats = flats_dict['props']['pageProps']['data']['searchAds']['items']
    for i in flats:
        links.append([i['slug'], i['dateCreatedFirst']])
print('All links collected')

flats_list = []
for link in links:
    flat_info = {}
    try:
        ans = requests.get('https://www.otodom.pl/pl/oferta/' + link[0],
                            headers=headers)
    except:
        print("Error occured during request in line 27")
        print(link[0])
        continue
    soup = BeautifulSoup(ans.content, "html.parser")
    try:
        soup.find('h1', attrs={'data-cy': 'adPageAdTitle'}).text
    except:
        print('Error during making soup in line 34')
        print(link[0])
        continue
    try:
        flat_info['adres'] = soup.find('a', attrs={'aria-label': 'Adres'}).text
        flat_info['cena'] = soup.find('strong', attrs={'aria-label': 'Cena'}).text
    except:
        print('Error in adress or price, line 46-47')
        print(link[0])
        continue
    try:
        frame = soup.find('div', attrs={'class': 'css-xr7ajr e10umaf20'}).find_all('div', attrs={'class': 'enb64yk1'})
    except:
        print('Occured error during find frame in line 40')
        print(link[0])
        continue
    if len(frame) != 10:
        continue
    for i in range(len(frame)):
        try:
            attr = frame[i].find_all('div', attrs={'class': 'css-rqy0wg enb64yk3'})[0].text
        except:
            continue
        try:
            value = frame[i].find_all('div', attrs={'class': 'css-1wi2w6s enb64yk5'})[0].text
        except:
            value = 'Zapytaj'
        flat_info[attr] = value

    try:
        add_frame = soup.find('div', attrs={'class': 'css-1utkgzv e10umaf20'}).find_all('div',
                                                                                        attrs={'class': 'enb64yk1'})
    except:
        continue

    if len(add_frame) != 12:
        continue

    for i in range(len(add_frame)):
        try:
            attr = add_frame[i].find_all('div', attrs={'class': 'css-rqy0wg enb64yk3'})[0].text
        except:
            continue
        try:
            value = add_frame[i].find_all('div', attrs={'class': 'css-1wi2w6s enb64yk5'})[0].text
        except:
            value = 'Zapytaj'
        flat_info[attr] = value

    flat_info['link'] = link[0]
    flat_info['data_dodania'] = link[1]
    flats_list.append(flat_info)

filename = 'flats_list'
pickle.dump(flats_list, open(filename, 'wb'))
flats_df = pd.DataFrame(flats_list)
flats_df['dzisiaj'] = today
table_name = f'waw_flats_{day}_{month}.csv'
try:
    cb_df = load_table.final_tables(flats_df, table_name=table_name)
except Exception as e:
    print(e)
    flats_df.to_csv(f'datasets/waw_flats_{day}_{month}.csv', index=False)
    print('Error during preprocessing df')
try:
    load_table.learn_catboost(cb_df)
except Exception as e:
    print(e)
#flats_df.to_csv(f'datasets/waw_flats_{day}_{month}.csv', index=False)