#!env/bin/python

from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world!!"

if __name__ == "__main__":
    app.run(debug=True)