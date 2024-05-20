from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from .models import FoodItem, MealEntry, MealFoodItem, User
from .extensions import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def index():
    today = datetime.today()
    week_ago = today - timedelta(days=7)
    meal_entries = MealEntry.query.filter(
        MealEntry.date <= today,
        MealEntry.date >= week_ago,
        MealEntry.user_id == current_user.id,
    ).all()
    return render_template("index.html", meal_entries=meal_entries)


@bp.route("/add-meal", methods=["GET", "POST"])
@login_required
def add_meal():
    if request.method == "POST":
        date_str = request.form.get("date")
        if not date_str:
            return "Missing data!", 400

        meal_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        new_meal = MealEntry(date=meal_date, user_id=current_user.id)
        db.session.add(new_meal)
        db.session.commit()

        return redirect(url_for("main.add_food_to_meal", meal_id=new_meal.id))

    return render_template("meal_entry.html")


@bp.route("/add-food-to-meal/<int:meal_id>", methods=["GET", "POST"])
@login_required
def add_food_to_meal(meal_id):
    meal = MealEntry.query.get_or_404(meal_id)
    if request.method == "POST":
        food_item_id = request.form.get("food_item_id")
        quantity = request.form.get("quantity")

        if not food_item_id or not quantity:
            return "Missing data!", 400

        new_meal_food_item = MealFoodItem(
            meal_id=meal.id, food_item_id=food_item_id, quantity=quantity
        )
        db.session.add(new_meal_food_item)
        db.session.commit()

        return redirect(url_for("main.add_food_to_meal", meal_id=meal.id))

    food_items = FoodItem.query.all()
    print("Food items fetched for dropdown:")
    for item in food_items:
        print(f"{item.id}: {item.name}")
    return render_template("add_food_to_meal.html", meal=meal, food_items=food_items)


@bp.route("/add-food", methods=["GET", "POST"])
@login_required
def add_food():
    if request.method == "POST":
        name = request.form["name"]
        calories = request.form["calories"]
        proteins = request.form["proteins"]
        carbs = request.form["carbs"]
        fats = request.form["fats"]
        fiber = request.form["fiber"]
        unit = request.form["unit"]

        new_food = FoodItem(
            name=name,
            calories_per_unit=calories,
            proteins_per_unit=proteins,
            carbs_per_unit=carbs,
            fats_per_unit=fats,
            fiber_per_unit=fiber,
            unit=unit,
        )
        db.session.add(new_food)
        db.session.commit()

        return redirect(url_for("main.index"))

    return render_template("add_food.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user:
            flash("Username already exists", "error")
            return redirect(url_for("main.register"))

        new_user = User(
            username=username,
            password=generate_password_hash(password, method="sha256"),
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("main.index"))

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials", "error")
            return redirect(url_for("main.login"))

        login_user(user)
        return redirect(url_for("main.index"))

    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))
