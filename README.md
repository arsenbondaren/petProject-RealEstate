# petProject-RealEstate
This pet-project is a web-service to observe real estate market in Warsaw.
The main purpose of the project is to make calculation of apartments prices in Warsaw easier and faster.
The service available on http://arsen2gunner.pythonanywhere.com
# Data:
Information about apartmentss in sale in Warsaw is collected from otodom.pl with python requests and beautifulsoup libraries (parse_data.py file). After parsing, data loads in database and csv file.
In database new data replace old data. Old data stores in csv files for fitting models.
The list of apartments on website is loaded from database.
# Database:
SQLite database is used in project. Database consist of two tables: table with currently available flats and table with statistics of mean price per m2.
To see flats in sale on website use "Flats" button on the top of the page or "/flats" route.
To see statistic graph of mean price use button "Mean price" or route "/graph".
# Models:
In project three models are used to calculate the price of the flat: AdaBoostRegressor, CatBoostRegressor and LinearRegression.
AdaBoost and CatBoost separately predict their prices and LinearRegression predicts the final price based on boosting's predictions.
To be relevant models need to be updated regularly. CatBoost model automatically updates after each new parsing in parse_data.py file.
To update AdaBoost and Linear regression weights after parsing data jupyter notebook is used (work_with_model.ipynb). Only one month old data is useful for model, so after parsing we need to manually fit AdaBoost on new data in jupyter notebook.
# Other
The project is usable not only for predictions, but for observation the dynamic of mean price per m2 changing as well. 
On the project website you can: see the list of available apartments in Warsaw, the graph of dynamic mean price per m2, add your own flat to list and calculate the price of the desired flat.
