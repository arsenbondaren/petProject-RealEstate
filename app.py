from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import sklearn
from sklearn.ensemble import AdaBoostRegressor
from sklearn.linear_model import LinearRegression
import datetime
from datetime import timedelta
from sqlalchemy import func
import pickle
from catboost import CatBoostRegressor, Pool
import pandas as pd
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure
from bokeh.embed import components
from pathlib import Path
THIS_FOLDER = Path(__file__).parent.resolve()

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_flat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


with app.app_context():
    db.reflect()
class Flat(db.Model):
    __tablename__ = "flats_load"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    district = db.Column(db.Text)
    street = db.Column(db.Text)
    price = db.Column(db.Float)
    area = db.Column(db.Float)
    rooms = db.Column(db.Integer)
    renovation = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    market = db.Column(db.Integer)
    elevator = db.Column(db.Integer)
    balcony = db.Column(db.Integer)
    terrace = db.Column(db.Integer)
    garden = db.Column(db.Integer)
    central_heating = db.Column(db.Integer)
    seller = db.Column(db.Integer)
    blok = db.Column(db.Integer)
    parking = db.Column(db.Integer)
    publication_date = db.Column(db.DateTime, default=datetime.datetime.now())

class PriceMetric(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date = db.Column(db.DateTime, nullable=False)
    price_m2 = db.Column(db.Float, nullable=False)

renovation_dict = {3: 'Do zamieszkania', 2: 'Do wykończenia', 1: 'Do remontu', 0: 'Zapytaj'}
floor_dict = {0: 'First floor (parter)', 1: 'Last floor', 2: 'Other floors (not first, not last)'}
market_dict = {1: 'New building', 2: 'Secondary housing market'}
binary_dict = {1: 'Yes', 0: 'No'}
seller_dict = {1: 'Real-Estate agency', 2: 'Private owner', 3: 'Developer'}


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/graph')
def graph():
    dates = []
    values = []
    res = db.session.execute(db.select(PriceMetric.date).order_by(PriceMetric.date)).all()
    for i in res:
        dates.append(i[0])
    res = db.session.execute(db.select(PriceMetric.price_m2).order_by(PriceMetric.date)).all()
    for i in res:
        values.append(i[0])
    plot = figure(title="Price graph", sizing_mode='stretch_width', x_range=(dates[0]-timedelta(days=15),dates[-1]+timedelta(days=15)),
                  x_axis_label='date', y_range=(14000,18000), y_axis_label='price_m2')
    plot.toolbar.logo = None
    plot.xaxis[0].formatter = DatetimeTickFormatter(days="%d/%b")
    plot.circle(dates, values, size=8)
    plot.line(dates, values, legend_label="Temp.", line_width=2)
    script, div = components(plot)
    print(dates)
    return render_template("graph.html", the_div=div, the_script=script)


@app.route('/del_graph')
def del_graph():
    obj_to_del = db.session.execute(db.select(PriceMetric)).all()
    #obj_to_del = db.session.execute(db.select(PriceMetric).where(PriceMetric.date == datetime.datetime(2023,8,3,00,00,00,00))).all()[0][0]
    for i, o in enumerate(obj_to_del):
        try:
            db.session.delete(obj_to_del[i][0])
            db.session.commit()
        except:
            return 'Error during delete'
    return redirect('/')


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        street = request.form['street']
        obj_to_del = db.session.execute(db.select(Flat).where(Flat.street == street)).first()[0]
        try:
            db.session.delete(obj_to_del)
            db.session.commit()
        except:
            return 'Error during delete'
        return redirect('/flats')
    else:
        return render_template('delete.html')


@app.route('/flats')
def show_flats():
    page = request.args.get('page', 1, type=int)
    flats = db.paginate(db.select(Flat).order_by(Flat.publication_date.desc()), page=page, per_page=10)
    return render_template('gpt_page.html', flats=flats, floor_dict=floor_dict)


@app.route('/flats/<flat_id>')
def flat_detail(flat_id):
    flat = db.session.execute(db.select(Flat).where(Flat.id == flat_id)).one()[0]
    return render_template('flat_info.html', flat=flat, renovation_dict=renovation_dict, floor_dict=floor_dict,
                           market_dict=market_dict, binary_dict=binary_dict, seller_dict=seller_dict)


@app.route('/')
@app.route('/home')
def home():
    flats = db.session.execute(db.select(Flat).order_by(Flat.publication_date.desc())).fetchmany(5)
    flats = [f[0] for f in flats]
    return render_template('main_page.html', flats=flats, floor_dict=floor_dict)


@app.route('/add_flat', methods=['GET', 'POST'])
@app.route('/predict_price', methods=['GET', 'POST'])
def add_flat():
    if request.method == 'POST':
        district = request.form['flat-district']
        street = request.form['street']
        area = request.form['area']
        rooms = request.form['room']
        renovation = request.form['flat-renovation']
        floor = request.form['floor']
        market = request.form['market-kind']
        elevator = request.form['elevator']
        balcony = request.form['balcony']
        terrace = request.form['terrace']
        garden = request.form['garden']
        central_heating = request.form['central-heating']
        seller = request.form['seller']
        blok = request.form['is-blok']
        parking = request.form['is-parking']
        if request.path == '/add_flat':
            id = db.session.execute(db.select(func.max(Flat.id))).one()[0] + 1
            price = request.form['price']
            new_flat = Flat(district=district, street=street, price=price, area=area, rooms=rooms, renovation=renovation,
                            floor=floor, market=market, elevator=elevator, balcony=balcony, terrace=terrace, garden=garden,
                            central_heating=central_heating, seller=seller, blok=blok, parking=parking, id=id)
            try:
                db.session.add(new_flat)
                db.session.commit()
                return redirect('/')
            except:
                return "Error during adding new flat"
        else:
            ada_regressor = pickle.load(open(THIS_FOLDER / 'adaboost_regressor.pkl', 'rb'))
            encoder = pickle.load(open(THIS_FOLDER / 'district_encode', 'rb'))
            lr_model = pickle.load(open(THIS_FOLDER / 'linear_regressor.pkl', 'rb'))
            district = encoder.transform([district])[0]
            cb_regressor = CatBoostRegressor().load_model(f"{THIS_FOLDER}/cb_model.cbm")
            cols_x = ['district', 'area', 'rooms', 'renovation', 'floor', 'balcony', 'terrace',
                      'garden', 'parking', 'central_heating', 'market', 'seller', 'blok', 'elevator']
            values = [district, area, rooms, renovation, floor, balcony, terrace, garden, parking, central_heating, market,
                      seller, blok, elevator]
            cat_features = [0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
            pool = Pool([values], cat_features=cat_features)
            ada_preds = ada_regressor.predict([values])
            cb_preds = cb_regressor.predict(pool)
            lr_df = pd.DataFrame(data=ada_preds.reshape(-1, 1), columns=['ada_preds'])
            lr_df['cb_preds'] = cb_preds
            pred_price = lr_model.predict(lr_df)
            return render_template('price_page.html', price=str(round(pred_price[0])))

    districts = db.session.execute(db.select(Flat.district)).unique()
    renovation_levels = db.session.execute(db.select(Flat.renovation)).unique()
    floors = db.session.execute(db.select(Flat.floor)).unique()
    market_kind = db.session.execute(db.select(Flat.market)).unique()
    elevator = db.session.execute(db.select(Flat.elevator)).unique()
    balcony = db.session.execute(db.select(Flat.balcony)).unique()
    terrace = db.session.execute(db.select(Flat.terrace)).unique()
    garden = db.session.execute(db.select(Flat.garden)).unique()
    heating_kind = db.session.execute(db.select(Flat.central_heating)).unique()
    sellers = db.session.execute(db.select(Flat.seller)).unique()
    blok = db.session.execute(db.select(Flat.blok)).unique()
    parking = db.session.execute(db.select(Flat.parking)).unique()

    if request.path == '/add_flat':
        return render_template('add_flat.html', districts=districts, renovation_levels=renovation_levels, floors=floors,
                               market_kind=market_kind, elevator=elevator, balcony=balcony, terrace=terrace, garden=garden,
                               heating_kind=heating_kind, sellers=sellers, renovation_dict=renovation_dict, floor_dict=floor_dict,
                               binary_dict=binary_dict, seller_dict=seller_dict, market_dict=market_dict, blok=blok,
                               parking=parking)

    else:
        return render_template('predict_price.html', districts=districts, renovation_levels=renovation_levels, floors=floors,
                                market_kind=market_kind, elevator=elevator, balcony=balcony, terrace=terrace,
                                garden=garden, heating_kind=heating_kind, sellers=sellers, renovation_dict=renovation_dict,
                                floor_dict=floor_dict, binary_dict=binary_dict, seller_dict=seller_dict,
                                market_dict=market_dict, blok=blok,parking=parking)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
