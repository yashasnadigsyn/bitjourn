import json
from dotenv import load_dotenv
import w3storage
import markdown


class ContentHandler:
    def __init__(self, w3token):
        self.w3 = w3storage.API(token=w3token)
        load_dotenv()

    def view_single_post(self, cid):
        post_obj = self.w3.get(cid)

    def create_post(self, post_obj):
        post_cid = self.w3.post_upload(json.dumps(post_obj))

        return post_cid
