# petProject-RealEstate
This is my pet-project about real estate market in Warsaw.
The main purpose of the project is to make calculation of flat prices in Warsaw simple and faster.
To calculate the price two models are used: AdaBoostRegressor and CatBoostRegressor. Each model calculate the price and the final result is linear regression built on their results.
To be relevant models needs regularly update. At least once a month data must be updated by parsing otodom.pl website with parse_data.py file. CatBoost model auto-updating during parsing. To update AdaBoost weights after parsing data jupyter notebook
is used (work_with_model.ipynb). Only one month old data is useful for model, so after each parsing AdaBoost model is manually learned in jupyter notebook.
The project is usable not only for predictions, but for observation the dynamic of mean price per m2 changing as well. 
On the project website you can see the list of available flats in Warsaw, the graph of dynamic mean price per m2, add your own flat to list and calculate the price for your desired flat.
