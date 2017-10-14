from flask import Flask,jsonify
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

@app.route("/")
def main():
  conn = sqlite3.connect('./db/database.db')
  c = conn.cursor()
  d = {
    'Requests' : {
      '/totals' : 'List of transaction and revenue totals for each department',
      '/city/:city/' : 'List of transaction revenue totals for a specific city'
    }
  }
  create_db()
  return jsonify(d)

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


@app.route("/city/<string:city_name>/")
def city(city_name):
  print("Getting data for "+ city_name)
  conn = sqlite3.connect('./db/database.db')
  c = conn.cursor()
  d = dict()
  print("SELECT COUNT(DISTINCT order_number) FROM catalog WHERE city = "+city_name)
  orders = c.execute("SELECT COUNT(DISTINCT order_number) FROM catalog WHERE city = '"+city_name+"'")
  d[dept[0]] = {}
  d[dept[0]]['Transactions']= json.dumps(c.fetchall()[0][0])
  orders = c.execute("SELECT SUM(price) FROM catalog WHERE city = '"+city_name+"'")
  d[dept[0]]['Revenue'] = '$' + str(round(float(json.dumps(c.fetchall()[0][0])),2))
  for x in range(1,21):
    d[dept[x]] = {}
    orders = c.execute("SELECT COUNT(DISTINCT order_number) FROM catalog WHERE department_id = "+str(x)+" and city = '"+city_name+"'")
    d[dept[x]]['Transactions'] = json.dumps(c.fetchall()[0][0])
    orders = c.execute("SELECT SUM(price) FROM catalog WHERE department_id = "+str(x)+" and city = '"+city_name+"'")
    d[dept[x]]['Revenue'] = '$' + str(round(float(json.dumps(c.fetchall()[0][0])),2))
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


