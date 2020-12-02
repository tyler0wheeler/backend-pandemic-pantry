import os
from peewee import *
import datetime
from flask_login import UserMixin
# from playhouse.postgres_ext import PostgresqlExtDatabase, ArrayField
from playhouse.db_url import connect


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
    class Meta:
        database = DATABASE

# class Ingredients(Model):
#     ingredient = CharField()
#     user = ForeignKeyField(User, backref="ingredients")
#     recipe = ForeignKeyField(Recipe, backref="ingredients")
#     class Meta:
#         database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Recipe], safe=True)
    print("tables created")
    DATABASE.close()