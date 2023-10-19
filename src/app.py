from flask import Flask, render_template, request
import w3storage
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

w3 = w3storage.API(token=os.getenv("W3STORAGE_TOKEN"))
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/create")
def create_post():
    return render_template("create.html")


@app.route("/api/submit", methods=["POST"])
def api_submit():
    post_obj = {}
    post_obj["title"] = request.form["title"]
    post_obj["author"] = request.form["author"]
    post_obj["content"] = request.form["content"]
    post_obj["timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    print(title, author, content)

    return "<p>submitted!</p>"


@app.route("/api/update")
def update():
    return "<p>updated!</p>"


if __name__ == "__main__":
    app.run(debug=True)
