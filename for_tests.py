from app.py import Flat
flats = Flat.query.paginate(page=1, per_page=5)
print(flats.items)