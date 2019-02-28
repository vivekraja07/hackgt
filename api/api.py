from flask import Flask,jsonify,render_template
from flask_cors import CORS
import sys
import csv
import sqlite3
import json
import math


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
  # create_db()
  return render_template("docs.html")

@app.route("/totals")
def totals():
  conn = sqlite3.connect('./db/database.db')
  c = conn.cursor()
  d = dict()
  orders = c.execute("SELECT COUNT(order_number) FROM catalog")
  d[dept[0]] = {}
  d[dept[0]]['Transactions']= json.dumps(c.fetchall()[0][0])
  orders = c.execute("SELECT SUM(price) FROM catalog")
  d[dept[0]]['Revenue'] = '$' + str(round(float(json.dumps(c.fetchall()[0][0])),2))
  for x in range(1,21):
    d[dept[x]] = {}
    # print("SELECT COUNT(DISTINCT order_number) FROM catalog WHERE department_id = "+str(x))
    orders = c.execute("SELECT COUNT(DISTINCT order_number) FROM catalog WHERE department_id = "+str(x))
    d[dept[x]]['Transactions'] = json.dumps(c.fetchall()[0][0])
    orders = c.execute("SELECT SUM(price) FROM catalog WHERE department_id = "+str(x))
    d[dept[x]]['Revenue'] = '$' + str(round(float(json.dumps(c.fetchall()[0][0])),2))
  return jsonify(d)


@app.route("/city/<string:city_name>")
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

@app.route("/city/<string:city_name>/dept/<string:dept_name>")
def deptartment(city_name,dept_name):
  conn = sqlite3.connect('./db/database.db')
  c = conn.cursor()
  department_id = -1
  for key,value in dept.items():
    if value == dept_name:
      department_id = key
  orders = c.execute("SELECT product_name,COUNT(*) FROM catalog WHERE product_name in ("+
    "SELECT distinct product_name FROM catalog WHERE department_id="+str(department_id)+" and city = '"+city_name+"') GROUP BY product_name")
  values = json.dumps(dict(c.fetchall()))
  # for value in values:
    # print(value)
  # print(d["Alaskan Salmon Burgers"])
  return values

@app.route("/store/<string:city_name>/<int:num_customers>/")
def store(city_name, num_customers):
  print("Getting data for store in " + city_name)
  conn = sqlite3.connect('./db/database.db')
  c = conn.cursor()
  d = dict()
  c.execute("SELECT DISTINCT order_number FROM catalog WHERE city = '" + city_name + "' limit '"+str(num_customers)+"'")
  orderNumbers = c.fetchall()
  i = 0
  for orderNumber in orderNumbers:
     d[i] = []
     orderNum = orderNumber[0]
     c.execute("select department_id from catalog where city = '" + city_name + "' and order_number = '" + str(orderNum) + "'")
     departments = c.fetchall()
     for department in departments:
       d[i].append(department[0])
     i += 1
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