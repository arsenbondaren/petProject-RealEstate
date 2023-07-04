import sqlite3
con = sqlite3.connect('test_flat.db')
cur = con.cursor()
res = cur.execute("SELECT ulica FROM flats_load WHERE dzielnica == 'bemowo'")
print(res.fetchone())
