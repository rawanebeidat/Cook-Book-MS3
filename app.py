import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# MongoDB Collections variables
users_coll = mongo.db.users
recipes_coll = mongo.db.recipes
cuisines_coll = mongo.db.cuisines
diets_coll = mongo.db.diets
meals_coll = mongo.db.meals


@app.route('/')
@app.route("/home")
def home():
    '''
    Main home page.
    Allows users to view 4 random featured recipes
    from the database as clickable cards, located bellow the hero image.
    '''
    # Generate 4 random recipes from the DB
    featured_recipes = ([recipe for recipe in recipes_coll.aggregate
                        ([{"$sample": {"size": 4}}])])
    return render_template('home.html', featured_recipes=featured_recipes,
                           title='Home')


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
