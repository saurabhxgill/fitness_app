from .extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    meals = db.relationship("MealEntry", backref="user", lazy=True)


class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    calories_per_unit = db.Column(db.Float, nullable=False)
    proteins_per_unit = db.Column(db.Float, nullable=False)
    carbs_per_unit = db.Column(db.Float, nullable=False)
    fats_per_unit = db.Column(db.Float, nullable=False)
    fiber_per_unit = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10), nullable=False)  # grams, ml, pieces


class MealEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    food_items = db.relationship("MealFoodItem", backref="meal", lazy=True)


class MealFoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey("meal_entry.id"))
    food_item_id = db.Column(db.Integer, db.ForeignKey("food_item.id"))
    quantity = db.Column(db.Float, nullable=False)
    food_item = db.relationship("FoodItem", backref="meal_food_items")
