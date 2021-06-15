from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Create an instance of Flask
app = Flask(__name__)


# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_hw")



@app.route('/')
def home():


    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", listings=destination_data)


@app.route("/scrape")
def scrape():

	#Store the return value in Mongo as a Python dictionary.

	# Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True) #This will push to the mongodb. 
    #The update function will update if the collection does not exist or it will overwrite it

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)