import json
from dotenv import load_dotenv
import w3storage
import markdown
import shelve
from os import listdir
import requests


class ContentHandler:
    def __init__(self, w3token):
        self.w3 = w3storage.API(token=w3token)
        load_dotenv()

        temp = shelve.open("homepage")
        self.homepage = dict(temp.items())
        temp.close()

    def __update_homepage(self):
        temp = shelve.open("homepage")
        temp.update(self.homepage)
        temp.close()

    def view_single_post(self, cid):
        post_obj = requests.get(f"https://ipfs.io/ipfs/{cid}").json()
        post_obj["content"] = markdown.markdown(post_obj["content"])

        return post_obj

    def create_post(self, post_obj):
        post_cid = self.w3.post_upload(json.dumps(post_obj))

        self.homepage[post_cid] = post_obj
        self.__update_homepage()

        return post_cid

    def get_homepage(self):
        posts = self.homepage.items()
        print(list(posts))
        post_objs = [item[1] | {"cid": item[0]} for item in list(posts)]
        for obj in post_objs:
            obj["content"] = markdown.markdown(obj["content"])

        # sort post_objs using timestamp
        post_objs = sorted(post_objs, key=lambda k: k["timestamp"], reverse=True)

        return post_objs
