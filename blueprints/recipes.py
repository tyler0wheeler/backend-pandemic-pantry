import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import current_user

from flask_login import login_required

recipe = Blueprint('recipes', 'recipe')

@recipe.route('/', methods =["GET"])
def get_all_recipes():
    try:
        ingredient_id = models.Ingredients.id
        ingredient = models.Ingredients.ingredient
        recipe_number = models.Ingredients.recipe
        ingredients = [model_to_dict(ingredients)for ingredients in models.Ingredients.select(ingredient_id, ingredient, recipe_number)]
        recipes = [model_to_dict(recipe) for recipe in models.Recipe.select() if recipe.shared == True]
        # print(recipes)
        return jsonify(data={"recipes":recipes, "ingredients":ingredients}, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting this data"})

@recipe.route('/', methods =["POST"])
@login_required
def create_recipe():
    payload = request.get_json()
    print(type(payload), 'payload')
    user_recipe = models.Recipe.create(title=payload["title"], servings=payload["servings"], image=payload["image"], readyInMinutes=payload["readyInMinutes"], instructions=payload["instructions"], owner=current_user.id, shared=payload["shared"])
    recipe_dict = model_to_dict(user_recipe)
    return jsonify(data=recipe_dict, status={"code": 200, "message": "Success"})

@recipe.route('/<id>', methods=["GET"])
def get_one_recipe(id):
    print(id, 'reserved word')
    recipe = models.Recipe.get_by_id(id)
    return jsonify(data=model_to_dict(recipe), status={"code": 200, "message": "Success"})

@recipe.route('/userrecipes/', methods=["GET"])
@login_required
def get_one_user():
    # payload = request.get_json()
    # owner = payload['owner']
    # print(owner)
    ingredient_id = models.Ingredients.id
    ingredient = models.Ingredients.ingredient
    recipe_number = models.Ingredients.recipe
    ingredients = [model_to_dict(ingredients)for ingredients in models.Ingredients.select(ingredient_id, ingredient, recipe_number)]
    recipes = [model_to_dict(recipe) for recipe in current_user.recipes]
    return jsonify(data={"recipes":recipes, "ingredients":ingredients}, status={"code": 200, "message": "Success"})

@recipe.route('/<id>', methods=["PUT"])
@login_required
def update_recipe(id):
    payload = request.get_json()
    # print(payload)
    query = models.Recipe.update(**payload).where(models.Recipe.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.Recipe.get_by_id(id)), status={"code": 200, "message": "Success"})

@recipe.route('/<id>', methods=["DELETE"])
@login_required
def delete_recipe(id):
    delete_query = models.Recipe.delete().where(models.Recipe.id==id)
    num_of_rows_deleted = delete_query.execute()
    print(num_of_rows_deleted)
    # write logic -- if you have no rows deleted you will proabbly want some message telling you so
    return jsonify(
    data={},
    message="Successfully deleted {} post with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )

@recipe.route('/ingredient/<recipe_id>', methods=["POST"])
@login_required
def add_ingredient(recipe_id):
    payload = request.get_json()
    print(type(payload), 'payload')
    add_ingredient_recipe_id = recipe_id
    # user_who_added_ingredient = current_user.id
    add_ingredient = models.Ingredients.create(ingredient=payload["ingredient"], recipe=add_ingredient_recipe_id)
    new_ingredient = model_to_dict(add_ingredient)
    return jsonify(data=new_ingredient, status={"code": 200, "message": "Successfully added ingredient"})

@recipe.route('/delete-ingredient/<recipe_id>', methods=["DELETE"])
@login_required
def delete_ingredient(recipe_id):
    delete_ingredient_query = models.Ingredients.delete().where(models.Ingredients.id==recipe_id)
    num_of_rows_ingredient_deleted = delete_ingredient_query.execute()
    print(num_of_rows_ingredient_deleted)
    return jsonify(data={}, message="Successfully deleted {} ingredient with id {}".format(num_of_rows_ingredient_deleted, recipe_id), status={"code":200})

@recipe.route('/delete-all-ingredients/<recipe_id>', methods=["DELETE"])
@login_required
def delete_all_ingredients(recipe_id):
    # find_recipe_id = [recipe for recipe in models.Ingredients.recipe if recipe["id"]==recipe_id]
    delete_all_ingredients_query= models.Ingredients.delete().where(models.Ingredients.recipe==recipe_id)
    num_of_rows_ingredient_deleted = delete_all_ingredients_query.execute()
    print(num_of_rows_ingredient_deleted)
    return jsonify(data={}, message="Successfully deleted {} ingredients with id {}".format(num_of_rows_ingredient_deleted, recipe_id), status={"code":200}) 