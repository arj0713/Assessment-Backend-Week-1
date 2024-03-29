"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime

from flask import Flask, request, jsonify

from date_functions import convert_to_datetime, get_day_of_week_on, get_days_between

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


@app.get("/")
def index():
    """Returns an API welcome message."""

    return jsonify({"message": "Welcome to the Days API."})


@app.route("/between", methods=["POST"])
def between():
    """Returns the days between two posted dates"""

    data = request.json
    if not all(k in data for k in ["first", "last"]):
        return jsonify({"error": "Missing required data."}), 400
    try:
        first = convert_to_datetime(data["first"])
        last = convert_to_datetime(data["last"])
        days = get_days_between(first, last)
    except (ValueError, TypeError):
        return jsonify({"error": "Unable to convert value to datetime."}), 400
    add_to_history(request)
    return jsonify({"days": days}), 200


@app.route("/weekday", methods=["POST"])
def weekday():
    """Returns the day of the week for a given date string"""

    data = request.json
    if "date" not in data:
        return jsonify({"error": "Missing required data."}), 400
    try:
        date = convert_to_datetime(data["date"])
        day = get_day_of_week_on(date)
    except (ValueError, TypeError):
        return jsonify({"error": "Unable to convert value to datetime."}), 400
    add_to_history(request)
    return jsonify({"weekday": day})


@app.route("/history", methods=["GET", "DELETE"])
def history():
    """
    Returns a history list if given a GET request
    Clears history list if given a DELETE request
    """

    global app_history

    if request.method == "GET":
        if "number" in request.args:
            if request.args["number"].isdigit() and int(request.args["number"]) in range(1, 21):
                number = int(request.args["number"])
            else:
                return jsonify({"error": "Number must be an integer between 1 and 20."}), 400
        else:
            number = 5

        add_to_history(request)

        if number > len(app_history):
            number = len(app_history)

        filtered = app_history[-number:]

        return jsonify(filtered[::-1])

    if request.method == "DELETE":
        app_history = []
        return jsonify({"status": "History cleared"})


if __name__ == "__main__":
    app.run(port=8080, debug=True)
