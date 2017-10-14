from flask import Flask,jsonify
import sys
import sqlalchemy as sa
import csv
import pandas as pd
import sqlite3
import json

# engine = sa.create_engine('sqlite:///database.db')
# Base.metadata.create_all(engine)

dept = {
  1 : 'Frozen',
  2 : 'Health',
  3 : 'Grains',
  4 : 'Fruits & Veggies',
  5 : 'Alcohol',
  6 : 'Foreign',            #asian and mexican
  7 : 'Beverages',
  8 : 'Pet Food',
  9 : 'Pasta & Rice',       #sauces, pasta, rice
  10: 'Fruits & Veggies',
  11: 'Toiletries',
  12: 'Meats',
  13: 'Condiments',         #biscuits
  14: 'Breakfast',          #granola and such
  15: 'Canned Foods',
  16: 'Dairy',
  17: 'Cleaning Supplies',
  18: 'Baby Food',
  19: 'Snacks',             #chips, crackers, craisins, etc
  20: 'Deli',               #deli stuff, salads, meat
  21: 'Misc'
}

# dept['1']  = 'Frozen'
# dept['2']  = 'Health'
# dept['3']  = 'Grains'
# dept['4']  = 'Fruits & Veggies'
# dept['5']  = 'Alcohol'
# dept['6']  = 'Foreign' #asian and mexican
# dept['7']  = 'Beverages'
# dept['8']  = 'Pet Food'
# dept['9']  = 'Pasta & Rice' #sauces, pasta, rice
# dept['10'] = 'Fruits & Veggies'
# dept['11'] = 'Toiletries'
# dept['12'] = 'Meats'
# dept['13'] = 'Condiments' #biscuits
# dept['14'] = 'Breakfast' #granola and such
# dept['15'] = 'Canned Foods'
# dept['16'] = 'Dairy'
# dept['17'] = 'Cleaning Supplies'
# dept['18'] = 'Baby Food'
# dept['19'] = 'Snacks' #chips, crackers, craisins, etc
# dept['20'] = 'Deli' #deli stuff, salads, meat
# dept['21'] = 'Misc'

def create_db():
  conn = sqlite3.connect('./db/database.db')
  conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
  c = conn.cursor()
  c.execute("DROP TABLE catalog")
  c.execute('''CREATE TABLE catalog
               (order_number int,
                product_id int,
                customer_id int,
                product_name text,
                department_id int,
                price real)''')

  file_name = '../10000_transactions.csv'
  f = open(file_name,'rt')
  reader = csv.reader(f)
  column_names = True
  for row in reader:
    # print(row)
    # print(c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='catalog'"))
    if column_names:
      column_names = False
    else:
      # print("INSERT INTO catalog VALUES ("+row[0]+","+row[1]+","+row[2]+",'"+row[3]+"',"+row[4]+","+row[5]+")")

      c.execute("INSERT INTO catalog VALUES (?,?,?,?,?,?)", row)
  conn.commit()
  f.close()

create_db()

app = Flask(__name__)
# app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:./db/database.db'
# db = sa(app)

@app.route("/")
def main():
  print('Python version ' + sys.version)
  conn = sqlite3.connect('./db/database.db')
  c = conn.cursor()
  d = dict()
  for x in range(1,21):
    orders = c.execute("SELECT COUNT(DISTINCT order_number) FROM catalog WHERE department_id = "+str(x))
    d[dept[x]]= json.dumps(c.fetchall()[0][0])#orders
  return jsonify(d)

@app.route("/city/<string:city>/")
def city(city):
  return city

if __name__ == "__main__":
  app.run()
