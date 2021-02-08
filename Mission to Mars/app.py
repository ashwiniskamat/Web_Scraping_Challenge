from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Create a connection to the mongodb
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create the / route. 
# Query the mongodb and display on the template
@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars=mars_info)

# Create the /scrape route. It scrapes new data, insets into
# the mongodb and then redirects to the / route to be displayed
@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

# the main function
if __name__ == "__main__":
    app.run(debug=True)