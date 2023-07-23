#!/usr/bin/python3
"""Starts a Flask web application"""
from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states_list")
def states_list():
    """Render template with states"""
    path = "7-states_list.html"
    states = storage.all(State)
    return render_template(path, states=states)


@app.teardown_appcontext
def app_teardown(arg=None):
    """Clean-up session"""
    storage.close()


if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host="0.0.0.0", port=5000)
