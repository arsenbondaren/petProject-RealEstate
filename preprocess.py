import pandas as pd

def cut_numbers(street):
    numbers = '1234567890'
    end = street.split(' ')[-1]
    for i in end:
        if i in numbers:
            return ' '.join(street.split(' ')[:-1])
    return street


# test
#print(cut_numbers('ul. ks. jerzego popiełuszki 17c'))


def clean_area(value):
    if len(value) > 25:
        value = value.split('}')[1]
    try:
        clean_value = float(value.split(' ')[0].replace(',', '.'))
    except:
        return None
    return clean_value


# test
#print(clean_area('55,5 m2'))
#print(clean_area('102 m2'))
#print(clean_area('55\xa0500 m2'))


def clean_price(value):
    try:
        clean_value = int(value.replace('zł', '').replace(' ', ''))
    except:
        return None
    return clean_value


# test
#print(clean_price('570 000 zł'))
#print(clean_price('Zapytaj o cenie'))


def clean_rooms(value):
    try:
        clean_value = int(value)
    except:
        return None
    return clean_value


# test
#print(clean_rooms('4 '))
#print(clean_rooms('więcej niż 10 '))

def renovation(value):
    renovation_dict = {'do zamieszkania': 3, 'do wykończenia': 2, 'do remontu': 1, 'Zapytaj': 0}
    try:
        return renovation_dict[value]
    except:
        return 0


def floors_clean(value):
    """Function returns: 0 for flats on the first floor (parter), 1 for the last floor, 2 for other floors"""

    floor = value.split('/')[0].strip()
    if floor == 'parter':
        return 0
    if floor == 'poddasze':
        return 1

    try:
        amount_floors = int(value.split('/')[1])
        if int(floor) % amount_floors == 0:
            return 1
    except:
        return 2
    else:
        return 2


seller_type = {'biuro nieruchomości ': 1, 'prywatny': 2, 'deweloper': 3}

elevator_dict = {'tak': 1, 'nie': 0}

districts = {
    'bemowo-lotnisko': 'bemowo', 'boernerowo': 'bemowo', 'chrzanów': 'bemowo', 'fort bema': 'bemowo',
    'fort radiowo': 'bemowo', 'górce': 'bemowo', 'groty': 'bemowo', 'jelonki': 'bemowo', 'cytadela': 'żoliborz',
    'lotnisko': 'bemowo', 'białołęka dworska': 'białołęka', 'brzeziny': 'białołęka', 'kąty grodziskie': 'białołęka',
    'choszczówka': 'białołęka', 'dąbrówka szlachecka': 'białołęka', 'grodzisk': 'białołęka', 'henryków': 'białołęka',
    'kobiałka': 'białołęka', 'nowodwory': 'białołęka', 'szamocin': 'białołęka', 'tarchomin': 'białołęka',
    'żerań': 'białołęka', 'lewandów': 'białołęka', 'chomiczówka': 'bielany', 'huta': 'bielany',
    'las bielański': 'bielany',
    'młociny': 'bielany', 'marymont': 'bielany', 'piaski': 'bielany', 'placówka': 'bielany', 'radiowo': 'bielany',
    'słodowiec': 'bielany', 'stare bielany': 'bielany', 'wólka węglowa': 'bielany', 'wawrzyszew': 'bielany',
    'wrzeciono': 'bielany', 'augustówka': 'mokotów', 'górny mokotów': 'mokotów', 'czerniaków': 'mokotów',
    'ksawerów': 'mokotów', 'służew': 'mokotów', 'służewiec': 'mokotów', 'sadyba': 'mokotów', 'siekierki': 'mokotów',
    'sielce': 'mokotów', 'stary mokotów': 'mokotów', 'stegny': 'mokotów', 'dolny mokotów': 'mokotów',
    'wierzbno': 'mokotów', 'wyględów': 'mokotów', 'królikarnia': 'mokotów', 'pole mokotowskie': 'ochota',
    'filtry': 'ochota', 'rakowiec': 'ochota', 'stara ochota': 'ochota', 'kępa tarchomińska': 'białołęka',
    'szczęśliwice': 'ochota', 'gocław': 'praga-południe', 'gocławek': 'praga-południe', 'grochów': 'praga-południe',
    'kamionek': 'praga-południe', 'olszynka grochowska': 'praga-południe', 'saska kępa': 'praga-południe',
    'nowa praga': 'praga-północ', 'pelcowizna': 'praga-północ', 'stara praga': 'praga-północ', 'centrum': 'śródmieście',
    'szmulowizna': 'praga-północ', 'kawęczyn-wygoda': 'rembertów', 'nowy rembertów': 'rembertów',
    'stary rembertów': 'rembertów', 'muranów': 'śródmieście', 'nowe miasto': 'śródmieście', 'powiśle': 'śródmieście',
    'solec': 'śródmieście', 'stare miasto': 'śródmieście', 'śródmieście północne': 'śródmieście',
    'śródmieście południowe': 'śródmieście', 'ujazdów': 'śródmieście', 'elsnerów': 'targówek', 'bródno': 'targówek',
    'bródno-podgrodzie': 'targówek', 'targówek fabryczny': 'targówek', 'targówek mieszkaniowy': 'targówek',
    'zacisze': 'targówek', 'utrata': 'targówek', 'czechowice': 'ursus', 'gołąbki': 'ursus', 'niedźwiadek': 'ursus',
    'skorosze': 'ursus', 'szamoty': 'ursus', 'dąbrówka': 'ursynów', 'grabów': 'ursynów', 'stokłosy': 'ursynów',
    'jeziorki północne': 'ursynów', 'jeziorki południowe': 'ursynów', 'kabaty': 'ursynów', 'natolin': 'ursynów',
    'pyry': 'ursynów', 'skarpa powsińska': 'ursynów', 'stary służew': 'ursynów', 'stary imielin': 'ursynów',
    'teren wydzielony rezerwat „las kabacki”': 'ursynów', 'ursynów-centrum': 'ursynów', 'imielin': 'ursynów',
    'ursynów północny': 'ursynów', 'wyczółki': 'ursynów', 'aleksandrów': 'wawer', 'anin': 'wawer', 'falenica': 'wawer',
    'las': 'wawer', 'marysin wawerski': 'wawer', 'miedzeszyn': 'wawer', 'międzylesie': 'wawer', 'nadwiśle': 'wawer',
    'radość': 'wawer', 'sadul': 'wawer', 'zerzeń': 'wawer', 'groszówka': 'wesoła', 'plac wojska polskiego': 'wesoła',
    'stara miłosna': 'wesoła', 'wesoła-centrum': 'wesoła', 'wola grzybowska': 'wesoła', 'zielona-grzybowa': 'wesoła',
    'wilanów wysoki': 'wilanów', 'wilanów niski': 'wilanów', 'wilanów królewski': 'wilanów', 'wiktoryn': 'włochy',
    'błonia wilanowskie': 'wilanów', 'powsinek': 'wilanów', 'zawady': 'wilanów', 'kępa zawadowska': 'wilanów',
    'powsin': 'wilanów', 'nowe włochy': 'włochy', 'okęcie': 'włochy', 'opacz wielka': 'włochy', 'paluch': 'włochy',
    'raków': 'włochy', 'salomea': 'włochy', 'stare włochy': 'włochy', 'załuski': 'włochy', 'czyste': 'wola',
    'koło': 'wola', 'młynów': 'wola', 'mirów': 'wola', 'nowolipki': 'wola', 'odolany': 'wola', 'powązki': 'wola',
    'ulrychów': 'wola', 'marymont-potok': 'żoliborz', 'stary żoliborz': 'żoliborz', 'sady żoliborskie': 'żoliborz'
}

cols_for_db = ['cena', 'powierzchnia', 'liczba pokoi', 'stan wykończenia', 'piętro', 'rynek', 'winda', 'ulica',
                'dzielnica', 'balkon', 'taras', 'ogródek', 'parking', 'ogrzewanie_miejskie', 'sprzedawca', 'blok',
                'cena_m', 'dzisiaj', 'link', 'data_dodania']

eng_cols = {'cena':'price', 'powierzchnia':'area', 'liczba pokoi':'rooms', 'stan wykończenia':'renovation',
            'piętro':'floor', 'rynek':'market', 'winda':'elevator', 'ulica':'street', 'dzielnica':'district',
            'balkon':'balcony', 'taras':'terrace', 'ogródek':'garden', 'ogrzewanie_miejskie':'central_heating',
            'sprzedawca':'seller', 'dzisiaj':'today', 'data_dodania':'publication_date'}

def waw_districts(value):
    try:
        return districts[value]
    except:
        return value


def preproc_data(flats_df):
    new_cols = []
    flag = False
    for i in flats_df.columns:
        if len(i) < 25:
            new_cols.append(i)
        else:
            new_cols.append('Powierzchnia')
            flag = True
    if flag:
        flats_df.columns = new_cols
    flats_df.rename(lambda x: x.lower(), axis=1, inplace=True)
    flats_df['ulica'] = flats_df['adres'].apply(lambda x: x.split(',')[0].strip())
    flats_df['dzielnica'] = flats_df['adres'].apply(lambda x: x.split(',')[-3].strip() if len(x.split(','))>2 else None)
    #mask = flats_df['ulica'] == 'Warszawa'
    #flats_df.loc[mask, 'dzielnica'] = flats_df['adres'].apply(lambda x: x.split(',')[0].strip())
    #mask2 = flats_df['adres'].str.startswith(('al.', 'ul.'))
    #flats_df.loc[mask2, 'ulica'] = flats_df.loc[mask2, 'dzielnica']
    #flats_df['ulica'] = flats_df['ulica'].apply(lambda x: 'unknown' if x == 'Warszawa' else x)
    flats_df['ulica'] = flats_df['ulica'].str.lower()
    flats_df['dzielnica'] = flats_df['dzielnica'].str.lower()
    flats_df['ulica'] = flats_df['ulica'].apply(cut_numbers)
    flats_df['powierzchnia'] = flats_df['powierzchnia'].apply(clean_area)
    flats_df['cena'] = flats_df['cena'].apply(clean_price)
    flats_df['liczba pokoi'] = flats_df['liczba pokoi'].apply(clean_rooms)
    flats_df['stan wykończenia'] = flats_df['stan wykończenia'].apply(renovation)
    flats_df['piętro'] = flats_df['piętro'].apply(floors_clean)
    flats_df['balkon'] = flats_df['balkon / ogród / taras'].apply(lambda x: 1 if 'balkon' in x else 0)
    flats_df['taras'] = flats_df['balkon / ogród / taras'].apply(lambda x: 1 if 'taras' in x else 0)
    flats_df['ogródek'] = flats_df['balkon / ogród / taras'].apply(lambda x: 1 if 'ogródek' in x else 0)
    flats_df['parking'] = flats_df['miejsce parkingowe'].apply(lambda x: 1 if 'miejsce' in x else 0)
    flats_df['ogrzewanie_miejskie'] = flats_df['ogrzewanie'].apply(lambda x: 1 if x == 'miejskie' else 0)
    flats_df['rynek'] = flats_df['rynek'].apply(lambda x: 1 if x == 'pierwotny' else 2)
    flats_df['sprzedawca'] = flats_df['typ ogłoszeniodawcy'].map(seller_type)
    flats_df['blok'] = flats_df['rodzaj zabudowy'].apply(lambda x: 1 if x == 'blok' else 0)
    flats_df['winda'] = flats_df['winda'].map(elevator_dict)
    flats_df['dzielnica'] = flats_df['dzielnica'].apply(waw_districts)
    main_districts = flats_df['dzielnica'].value_counts().head(18).index
    flats_df['dzielnica'] = flats_df['dzielnica'].apply(lambda x: x if x in main_districts else None)
    flats_df['cena_m'] = flats_df['cena'] / flats_df['powierzchnia']
    flats_df['data_dodania'] = pd.to_datetime(flats_df['data_dodania'])
    flats_df = flats_df.loc[:, cols_for_db]
    flats_df.rename(columns=eng_cols, inplace=True)
    flats_df = flats_df.dropna().reset_index(drop=True)
    return flats_df
