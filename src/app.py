from flask import Flask, render_template, request
import w3storage
from dotenv import load_dotenv
import os

load_dotenv()

w3 = w3storage.API(token=os.getenv("W3STORAGE_TOKEN"))
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/submit", methods=["POST"])
def submit():
    title = request.form.get("title")
    author = request.form.get("author")
    content = request.form.get("content")

    print(title, author, content)

    return "<p>submitted!</p>"


@app.route("/api/update")
def update():
    return "<p>updated!</p>"


if __name__ == "__main__":
    app.run(debug=True)
