from flask import Flask, render_template, request
import w3storage
from dotenv import load_dotenv
import os
from datetime import datetime
import json

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

    post_cid = w3.post_upload(json.dumps(post_obj))

    return f"your post is available is IPFS CID <code>{post_cid}</code>"


if __name__ == "__main__":
    app.run(debug=True)
