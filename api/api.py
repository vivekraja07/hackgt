from flask import Flask
import sys
import sqlalchemy as sa
import csv
import pandas as pd
import sqlite3

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
    # print("INSERT INTO catalog VALUES ("+', '.join(row)+")")
    else:
      c.execute("INSERT INTO catalog VALUES ("+', '.join(row)+")")

  # conn.commit()
  f.close()

create_db()
# df = pd.read_csv(file_name)
# pd.read_csv(file_name)
# df.to_sql(con=engine, index_label='id',name=catalog.__tablename__, if_exists='replace')





app = Flask(__name__)
# app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:./db/database.db'
# db = sa(app)

@app.route("/")
def hello():
  print('Python version ' + sys.version)
  print('Pandas version ' + pd.__version__)
  print('SQLAlchemy version ' + sa.__version__)
  return "This is our api"

@app.route("/city/<string:city>/")
def city(city):
  return city

if __name__ == "__main__":
  app.run()
