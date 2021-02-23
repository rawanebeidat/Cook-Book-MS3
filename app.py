import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import math
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


@app.route('/all_recipes')
def all_recipes():
    '''
    READ.
    Displays all the recipes from the database using pagination.
    The limit is set to 8 recipes per page.
    Also displayes the number of all recipes.
    '''
    # CREDITS: the idea of pagination used below is taken and modified
    # from the Shane Muirhead's project
    limit_per_page = 8
    current_page = int(request.args.get('current_page', 1))
    # get total of all the recipes in db
    number_of_all_rec = recipes_coll.count()
    pages = range(1, int(math.ceil(number_of_all_rec / limit_per_page)) + 1)
    recipes = recipes_coll.find().sort('_id', pymongo.ASCENDING).skip(
        (current_page - 1)*limit_per_page).limit(limit_per_page)

    return render_template("all_recipes.html", recipes=recipes,
                           title='All Recipes', current_page=current_page,
                           pages=pages, number_of_all_rec=number_of_all_rec)


# Single Recipe details display
@app.route('/recipe_details/<recipe_id>')
def single_recipe_details(recipe_id):
    '''
    READ.
    Displays detailed information about a selected recipe.
    If logged id user is an author of the selected recipe,
    there are buttons "edit" and "delete" displayed
    giving the oportunity to manipulate the recipe.
    '''
    # find the selected recipe in DB by its id
    selected_recipe = recipes_coll.find_one({"_id": ObjectId(recipe_id)})
    # Set the author of the recipe
    author = users_coll.find_one(
        {"_id": ObjectId(selected_recipe.get("author"))})["username"]
    return render_template("single_recipe_details.html",
                           selected_recipe=selected_recipe, author=author,
                           title='Recipe Details')


# My recipes
@app.route('/my_recipes/<username>')
def my_recipes(username):
    '''
    READ.
    Displays the recipes created by logged in user in session.
    If user has not created any recipes yet, there's a button "add recipe"
    giving an opportunity to create a new recipe.
    Pagination is in place diplaying 8 recipes per page.
    Also displays the total number of recipes created by the user.
    '''
    my_id = users_coll.find_one({'username': session['username']})['_id']
    my_username = users_coll.find_one({'username': session
                                      ['username']})['username']
    # finds all user's recipes by author id
    my_recipes = recipes_coll.find({'author': my_id})
    # get total number of recipes created by the user
    number_of_my_rec = my_recipes.count()
    # Pagination, displays 8 recipes per page
    # CREDITS: the idea of pagination used below is taken and modified
    # from the Shane Muirhead's project
    limit_per_page = 8
    current_page = int(request.args.get('current_page', 1))
    pages = range(1, int(math.ceil(number_of_my_rec / limit_per_page)) + 1)
    recipes = my_recipes.sort('_id', pymongo.ASCENDING).skip(
        (current_page - 1)*limit_per_page).limit(limit_per_page)

    return render_template("my_recipes.html", my_recipes=my_recipes,
                           username=my_username, recipes=recipes,
                           number_of_my_rec=number_of_my_rec,
                           current_page=current_page, pages=pages,
                           title='My Recipes')


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
