"""
KINETIX — Flask backend.

Serves the site's pages (rendered from the JSON exercise/pose libraries)
and two small JSON APIs used by the Calorie Meter page:

    GET  /api/exercises        -> full gym exercise library
    GET  /api/yoga             -> full yoga pose library
    POST /api/bmr              -> Mifflin-St Jeor BMR / TDEE calculation
    POST /api/burn             -> estimated calories burned for an activity
    GET  /api/history          -> the signed-in session's saved calorie entries
    POST /api/history          -> save a calorie-meter entry to history.json

The calorie math also ships in static/js/calorie.js so the calculator
still works if this file isn't running (e.g. opened straight from disk),
but running `python app.py` gives you the full experience, including the
saved-history log written to data/history.json.
"""

import json
import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

app = Flask(__name__)


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history_entry(entry):
    path = os.path.join(DATA_DIR, "history.json")
    history = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, OSError):
            history = []
    history.append(entry)
    # Keep the file from growing forever in a demo project.
    history = history[-200:]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


# ---------------------------------------------------------------- pages ----

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/gym")
def gym():
    exercises = load_json("exercises.json")
    categories = sorted({e["category"] for e in exercises})
    return render_template("gym.html", exercises=exercises, categories=categories)


@app.route("/yoga")
def yoga():
    poses = load_json("yoga.json")
    focuses = sorted({p["focus"] for p in poses})
    return render_template("yoga.html", poses=poses, focuses=focuses)


@app.route("/calorie-meter")
def calorie_meter():
    return render_template("calorie.html")


# ----------------------------------------------------------------- API -----

@app.route("/api/exercises")
def api_exercises():
    return jsonify(load_json("exercises.json"))


@app.route("/api/yoga")
def api_yoga():
    return jsonify(load_json("yoga.json"))


@app.route("/api/bmr", methods=["POST"])
def api_bmr():
    """Mifflin-St Jeor BMR + activity-scaled TDEE."""
    payload = request.get_json(force=True) or {}

    try:
        weight_kg = float(payload["weight_kg"])
        height_cm = float(payload["height_cm"])
        age = float(payload["age"])
        sex = payload.get("sex", "female").lower()
        activity = float(payload.get("activity_multiplier", 1.2))
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "weight_kg, height_cm and age are required numbers"}), 400

    if sex == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    tdee = bmr * activity

    return jsonify({
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "activity_multiplier": activity,
    })


@app.route("/api/burn", methods=["POST"])
def api_burn():
    """Calories burned = MET x weight(kg) x duration(hours)."""
    payload = request.get_json(force=True) or {}

    try:
        met = float(payload["met"])
        weight_kg = float(payload["weight_kg"])
        minutes = float(payload["minutes"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "met, weight_kg and minutes are required numbers"}), 400

    calories = met * weight_kg * (minutes / 60.0)
    return jsonify({"calories_burned": round(calories, 1)})


@app.route("/api/history", methods=["GET", "POST"])
def api_history():
    path = os.path.join(DATA_DIR, "history.json")

    if request.method == "GET":
        if not os.path.exists(path):
            return jsonify([])
        with open(path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))

    payload = request.get_json(force=True) or {}
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "label": payload.get("label", "Session"),
        "calories": payload.get("calories"),
    }
    save_history_entry(entry)
    return jsonify(entry), 201


if __name__ == "__main__":
    app.run(debug=True)
