#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_hbnb():
    """
    Returns:
        str: A string with the message "Hello HBNB!".
    """
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    """
    Returns:
        str: A string with the message "HBNB".
    """
    return "HBNB"


@app.route("/c/<text>")
def c_is_fun(text):
    """
    Returns:
        str: A string with the formatted message.
    """
    return "C " + text.replace("_", " ")


if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host="0.0.0.0", port=5000)
