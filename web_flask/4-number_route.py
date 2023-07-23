#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, escape

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
    return "C " + escape(text).replace("_", " ")


@app.route("/python/", defaults={'text': 'is cool'})
@app.route("/python/<text>")
def python_is_cool(text):
    """
    Returns:
        str: A string with the formatted message.
    """
    return "Python " + escape(text).replace("_", " ")


@app.route("number/<int:n>")
def number(n):
    """
    Returns:
        str: A string is n is an integer.
    """
    return str(n) + ' is a number'


if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host="0.0.0.0", port=5000)
