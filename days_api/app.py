"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime

from flask import Flask, Response, request, jsonify

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
    """Returns an API welcome messsage."""
    return jsonify({"message": "Welcome to the Days API."})


@app.route("/between", methods=["POST"])
def post_for_days_between():
    """Returns the days between two posted dates"""
    data = request.json
    if not ("first" in data or "last" in data):
        return jsonify({"error": "Missing required data."}), 400
    try:
        first = convert_to_datetime(data["first"])
        last = convert_to_datetime(data["last"])
    except ValueError:
        return jsonify({"error": "Unable to convert value to datetime."}), 400
    days = get_days_between(first, last)
    return jsonify({"days": days}), 200


if __name__ == "__main__":
    app.run(port=8080, debug=True)
