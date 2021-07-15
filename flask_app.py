from flask import Flask, jsonify, render_template, redirect
from scrape_mars import scrape
from pymongo import MongoClient
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='template')
app.config["MONGO_URI"] = "mongodb://localhost:27017/MarsScrape"
mongo = PyMongo(app)

@app.route('/scrape')
def scrape_endpoint():
    hemispheres = mongo.db.Hemipsheres
    result = scrape()
    print(result)
    hemispheres.remove({})
    hemispheres.insert_many(result)
    return redirect("/", code=302)

@app.route('/')
def home():
    data_list = list(mongo.db.Hemispheres.find({}))
    print(data_list, flush=True)
    return render_template("index.html", hemisphere_list=data_list)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)

    
