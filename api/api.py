from flask import Flask,jsonify,render_template
from flask_cors import CORS
import sys
import csv
import sqlite3
import json
import math

# engine = sa.create_engine('sqlite:///database.db')
# Base.metadata.create_all(engine)

dept = {
  0 : 'All Orders',
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

app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
  conn = sqlite3.connect('./db/database.db')
  c = conn.cursor()
  d = {
    'Requests' : {
      '/totals' : 'List of transaction and revenue totals for each department',
      '/city/:city/' : 'List of transaction revenue totals for a specific city',
      'cities' : 'New York, Los Angeles, Chicago, Houston, Philadelphia, Phoenix,'+
                 'San Antonio, San Diego, Dallas, San Jose'
    }
  }
  create_db()
  return render_template("docs.html")

@app.route("/totals")
def totals():
  conn = sqlite3.connect('./db/database.db')
  c = conn.cursor()
  d = dict()
  orders = c.execute("SELECT COUNT(DISTINCT order_number) FROM catalog")
  d[dept[0]] = {}
  d[dept[0]]['Transactions']= json.dumps(c.fetchall()[0][0])
  orders = c.execute("SELECT SUM(price) FROM catalog")
  d[dept[0]]['Revenue'] = '$' + str(round(float(json.dumps(c.fetchall()[0][0])),2))
  for x in range(1,21):
    d[dept[x]] = {}
    print("SELECT COUNT(DISTINCT order_number) FROM catalog WHERE department_id = "+str(x))
    orders = c.execute("SELECT COUNT(DISTINCT order_number) FROM catalog WHERE department_id = "+str(x))
    d[dept[x]]['Transactions'] = json.dumps(c.fetchall()[0][0])
    orders = c.execute("SELECT SUM(price) FROM catalog WHERE department_id = "+str(x))
    d[dept[x]]['Revenue'] = '$' + str(round(float(json.dumps(c.fetchall()[0][0])),2))
  return jsonify(d)


@app.route("/city/<string:city_name>")
def city(city_name):
  create_db()
  print("Getting data for "+ city_name)
  conn = sqlite3.connect('./db/database.db')
  c = conn.cursor()
  d = dict()
  print("SELECT COUNT(DISTINCT order_number) FROM catalog WHERE city = "+city_name)
  orders = c.execute("SELECT COUNT(DISTINCT order_number) FROM catalog WHERE city = '"+city_name+"'")
  d[dept[0]] = {}
  d[dept[0]]['Transactions']= json.dumps(c.fetchall()[0][0])
  orders = c.execute("SELECT SUM(price) FROM catalog WHERE city = '"+city_name+"'")
  value = json.dumps(c.fetchall()[0][0])
  if value == "null":
    d[dept[0]]['Revenue'] = '$0.00'
  else:
    d[dept[0]]['Revenue'] = '$' + str(round(float(value),2))
  for x in range(1,21):
    d[dept[x]] = {}
    orders = c.execute("SELECT COUNT(DISTINCT order_number) FROM catalog WHERE department_id = "+str(x)+" and city = '"+city_name+"'")
    d[dept[x]]['Transactions'] = json.dumps(c.fetchall()[0][0])
    orders = c.execute("SELECT SUM(price) FROM catalog WHERE department_id = "+str(x)+" and city = '"+city_name+"'")
    value = json.dumps(c.fetchall()[0][0])
    if value == "null":
      d[dept[x]]['Revenue'] = '$0.00'
    else:
      d[dept[x]]['Revenue'] = '$' + str(round(float(value),2))
  return jsonify(d)

if __name__ == "__main__":
  app.run()

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
                price real,
                city text)''')
  file_name = '../10000_transactions.csv'
  f = open(file_name,'rt')
  reader = csv.reader(f)
  column_names = True
  for row in reader:
    if column_names:
      column_names = False
      print(row)
    else:
      c.execute("INSERT INTO catalog VALUES (?,?,?,?,?,?,?)", row)
  conn.commit()
  f.close()
