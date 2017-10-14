from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "This is our api"

@app.route("/city/<string:city>/")
def city(city):
  return city

if __name__ == "__main__":
  app.run()
