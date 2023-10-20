from flask import Flask, render_template, request
from datetime import datetime, date
from contenthandler import ContentHandler
import os, json, uuid

contentHandler = ContentHandler(w3token=os.getenv("W3STORAGE_TOKEN"))
app = Flask(__name__)


@app.route("/")
def home():
    posts = contentHandler.get_homepage()
    return render_template("home.html", posts=posts)

@app.route("/ads")
def create_ads():
    return render_template("ads.html")

@app.route("/ads/basic")
def show_basic_plan():
    return render_template("pay.html")

@app.route("/ads/custom")
def show_custom_plan():
    return render_template("custom.html")

@app.route("/ads/data", methods=['POST'])
def get_ads_content():
    title = request.form['title']
    image = request.files['image']
    content = request.form['content']
    image.save(os.path.join("static/ads/images", image.filename))
    datajson = {}
    datajson['title'] = title
    datajson['content'] = content
    datajson['image'] = os.path.join("static/ads/images", image.filename)
    datajson['validTill'] = str(date(date.today().year + 1, date.today().month, date.today().day))
    with open(f"static/ads/{str(uuid.uuid4())}.json", "w") as f:
        json.dump(datajson, f)
    return "cool"


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/create")
def create_post():
    return render_template("create.html")


@app.route("/post/<cid>")
def view_post(cid):
    post_obj = contentHandler.view_single_post(cid)
    return render_template("singlepost.html", post=post_obj)


@app.route("/tag/<tag>")
def get_posts_by_tag(tag):
    return f"<p>testing: {tag}</p><br><p>tags are not implemented yet :)</p>"


@app.route("/api/submit", methods=["POST"])
def api_submit():
    post_obj = {}
    post_obj["title"] = request.form["title"].strip()
    post_obj["author"] = request.form["author"].strip()
    post_obj["content"] = request.form["content"].strip()
    post_obj["timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # sanitize tags
    tags = request.form["tags"].split(",")
    tags = [tag.strip() for tag in tags if tag.strip() != ""]
    post_obj["tags"] = tags

    post_obj["banner_url"] = request.form["banner"].strip()

    post_cid = contentHandler.create_post(post_obj)

    return f"your post is available at IPFS CID <code>{post_cid}</code>"


if __name__ == "__main__":
    app.run(debug=True)
