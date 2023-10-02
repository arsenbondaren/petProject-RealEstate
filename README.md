# [petProject-RealEstate](http://arsen2gunner.pythonanywhere.com)
This pet-project is a web service to observe the real estate market in Warsaw. The main purpose of the project is to make the calculation of apartment prices in Warsaw easier and faster. The service is available on http://arsen2gunner.pythonanywhere.com
# Data:
Information about apartments for sale in Warsaw is collected from otodom.pl with Python **requests** and **beautifulsoup** libraries (parse_data.py file). After parsing, data loads in the database and csv file. In the database, new data replaces old data. Old data is stored in csv files for fitting models. The list of apartments on the website is loaded from the database.
# Database:
**SQLite** database is used in project. The database consists of two tables: a table with currently available flats and a table with the dynamic of the average price per m2. 
To see flats for sale on the website, use the "Flats" button at the top of the page or the "/flats" route. 
To see a statistic graph of the mean price, use the button "Mean price" or route "/graph".
# Models:
In this project three models are used to calculate the price of the flat: [AdaBoostRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostRegressor.html#sklearn.ensemble.AdaBoostRegressor), [CatBoostRegressor](https://catboost.ai/en/docs/concepts/python-reference_catboostregressor) and **LinearRegression**.
AdaBoost and CatBoost separately predict their prices, and LinearRegression predicts the final price based on boosting's predictions.
To be relevant, models need to be updated regularly. CatBoost model automatically updates after each new parsing in parse_data.py file. 
To update AdaBoost and Linear regression, jupyter notebook is used (work_with_model.ipynb). Only one-month-old data is useful for the model, so after parsing, we need to manually fit AdaBoost on new data in jupyter notebook.
# Other
The project is usable not only for predictions but for observation of the dynamic of mean price per m2 changing as well. 
On the project website, you can: see the list of available apartments in Warsaw, the graph of dynamic mean price per m2, add your own flat to list and calculate the price of the desired flat.
