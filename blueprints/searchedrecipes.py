import models

from peewee import *

from flask import Blueprint, jsonify, request, g

from playhouse.shortcuts import model_to_dict

from flask_login import current_user

from flask_login import login_required

searchedrecipe = Blueprint('searchedrecipes', 'searchedrecipe')

@searchedrecipe.route('/savedrecipes/', methods=["GET"])
@login_required
def get_one_user():
    searched_recipes = [model_to_dict(recipe) for recipe in current_user.searchedrecipes]
    return jsonify(data={"searchedrecipes":searched_recipes}, status={"code": 200, "message": "Success"})

@searchedrecipe.route('/', methods =["POST"])
@login_required
def create_recipe():
    payload = request.get_json()
    # print(type(payload), payload)
    user_searched_recipe = models.SearchedRecipe.create(title=payload["title"], servings=payload["servings"], image=payload["image"], readyInMinutes=payload["readyInMinutes"], instructions="hello", owner=current_user.id, recipeId=payload["recipeId"], ingredients=str(payload["ingredients"]))
    searched_recipe_dict = model_to_dict(user_searched_recipe)
    print(payload["ingredients"])
    print(payload["title"])
    print(payload["servings"])
    print(payload["image"])
    print(payload["readyInMinutes"])
    print(payload["instructions"])
    print(payload["recipeId"])
    print(current_user)
    return jsonify(data={}, status={"code": 200, "message": "Success"})

# @searchedrecipe.route('/searchedingredient/<recipe_id>', methods=["POST"])
# @login_required
# def add_ingredient(recipe_id):
#     payload = request.get_json()
#     print(type(payload), 'ingredient payload')
#     add_ingredient_recipe_id = recipe_id
#     # with g.db.atomic():
#     for x in range(len(payload)): 
#         add_ingredient = models.SearchedIngredients.create(ingredient=[payload["ingredient"]], recipe=add_ingredient_recipe_id)
#         new_ingredient = model_to_dict(add_ingredient)
#         return jsonify(data=new_ingredient, status={"code": 200, "message": "Successfully added ingredient"})

@searchedrecipe.route('/<id>', methods=["DELETE"])
@login_required
def delete_recipe(id):
    delete_query = models.SearchedRecipe.delete().where(models.SearchedRecipe.id==id)
    num_of_rows_deleted = delete_query.execute()
    print(num_of_rows_deleted)
    # write logic -- if you have no rows deleted you will proabbly want some message telling you so
    return jsonify(
    data={},
    message="Successfully deleted {} post with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )

# @searchedrecipe.route('/delete-all-ingredients/<recipe_id>', methods=["DELETE"])
# @login_required
# def delete_all_ingredients(recipe_id):
#     # find_recipe_id = [recipe for recipe in models.Ingredients.recipe if recipe["id"]==recipe_id]
#     delete_all_ingredients_query= models.SearchedIngredients.delete().where(models.SearchedIngredients.recipe==recipe_id)
#     num_of_rows_ingredient_deleted = delete_all_ingredients_query.execute()
#     print(num_of_rows_ingredient_deleted)
#     return jsonify(data={}, message="Successfully deleted {} ingredients with id {}".format(num_of_rows_ingredient_deleted, recipe_id), status={"code":200}) 