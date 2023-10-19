from flask import Flask, render_template
import w3storage
from dotenv import load_dotenv
import os

load_dotenv()

w3 = w3storage.API(token=os.getenv("W3STORAGE_TOKEN"))
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/update")
def update():
    return "<p>updated!</p>"


if __name__ == "__main__":
    app.run(debug=True)
