from flask import Flask,jsonify
import sys
import sqlalchemy as sa
import csv
import pandas as pd
import sqlite3
import json

# engine = sa.create_engine('sqlite:///database.db')
# Base.metadata.create_all(engine)

def create_db():
  conn = sqlite3.connect('./db/database.db')
  c = conn.cursor()
  # c.execute("DELETE FROM catalog")
  file_name = '../10000_transactions.csv'
  f = open(file_name,'rt')
  reader = csv.reader(f)
  column_names = True
  for row in reader:
    # print(row)
    # print(c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='catalog'"))
    if column_names:
      column_names = False
      # c.execute('''CREATE TABLE catalog
      #              (order_number int,
      #               product_id int,
      #               customer_id int,
      #               product_name text,
      #               department_id int,
      #               price real)''')

    else:
      # print("INSERT INTO catalog VALUES ("+row[0]+","+row[1]+","+row[2]+",'"+row[3]+"',"+row[4]+","+row[5]+")")
      c.execute("INSERT INTO catalog VALUES (?,?,?,?,?,?)", row)
      conn.commit()
  conn.commit()
  f.close()

create_db()

app = Flask(__name__)
# app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:./db/database.db'
# db = sa(app)

@app.route("/")
def hello():
  print('Python version ' + sys.version)
  conn = sqlite3.connect('./db/database.db')
  c = conn.cursor()
  orders = c.execute("SELECT * FROM catalog")
  json_string = json.dumps(c.fetchall())
  return jsonify(json_string)

@app.route("/city/<string:city>/")
def city(city):
  return city

if __name__ == "__main__":
  app.run()
