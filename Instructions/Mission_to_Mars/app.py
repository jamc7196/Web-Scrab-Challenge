from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_data_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()
    # Return template and data
    return render_template("index.html", mars_data=mars_data)
# Route that will trigger the scrape function

@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    # Run the scrape function
    marsdata = scrape_mars.scraper()
    # Update the Mongo database using update and upsert=True
    mars_data.update({}, marsdata, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)