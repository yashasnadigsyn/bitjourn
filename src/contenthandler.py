import json
from dotenv import load_dotenv
import w3storage
import markdown
import shelve
from os import listdir
import requests
import random


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

        # merge ads list and post_objs list so that ads appear randomly
        ads = self.get_ads()
        print(ads)
        for i, _ in enumerate(post_objs):
            if i % 3 == 0:
                post_objs.insert(i, ads[random.randint(0, len(ads) - 1)])

        return post_objs

    def get_ads(self):
        ads = []
        for ad in listdir("src/static/ads"):
            if ad.endswith(".json"):
                with open(f"src/static/ads/{ad}") as f:
                    ads.append(json.load(f))
        return ads
