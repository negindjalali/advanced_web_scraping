from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)



mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mars_info = mongo.db.mars_info 

@app.route("/")
def index():
    
    mars_mission_data=mongo.db.mars_info.find_one()
    
    return render_template("index.html", mars=mars_mission_data)

@app.route("/scrape")
def scrape():    
    
    
    results = scrape_mars.scrape()
    mars_info.update({},results,upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

