import os
from peewee import *
import datetime
from flask_login import UserMixin
# from playhouse.postgres_ext import PostgresqlExtDatabase, ArrayField
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('pantry.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()
    class Meta:
        database = DATABASE

class Recipe(Model):
    title = CharField()
    servings = IntegerField()
    image = CharField()
    readyInMinutes = IntegerField()
    instructions = CharField()
    owner = ForeignKeyField(User, backref="recipes")
    shared = BooleanField(default=False)
    class Meta:
        database = DATABASE

class Ingredients(Model):
    ingredient = CharField()
    recipe = ForeignKeyField(Recipe, backref="ingredients")
    class Meta:
        database = DATABASE

class SearchedRecipe(Model):
    title = CharField()
    servings = IntegerField()
    image = CharField()
    readyInMinutes = IntegerField()
    instructions = TextField()
    owner = ForeignKeyField(User, backref="searchedrecipes")
    ingredients = TextField()
    recipeId = IntegerField()
    class Meta:
        database = DATABASE

class SearchedIngredients(Model):
    ingredient = CharField()
    recipe = ForeignKeyField(SearchedRecipe, backref="searchedingredients")
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Recipe, Ingredients, SearchedRecipe, SearchedIngredients], safe=True)
    print("tables created")
    DATABASE.close()