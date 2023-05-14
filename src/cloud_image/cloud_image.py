import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api
import random
import pdb

load_dotenv()


class CloudImage():
    def __init__(self) -> None:
        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=os.getenv('CLOUDINARY_API_KEY'),
            api_secret=os.getenv('CLOUDINARY_API_SECRET')
        )

    def meow(self):
        result = cloudinary.Search().expression('tags=cat').execute()
        return random.choice(result['resources'])['secure_url']

    def wang(self):
        result = cloudinary.Search().expression('tags=dog').execute()
        return random.choice(result['resources'])['secure_url']

    def upload(self, file_path, folder='undefined_species'):
        result = cloudinary.uploader.upload(file_path, folder=folder)
        return result['public_id']

    def move(self, file_public_id, folder, tags=[]):
        result = cloudinary.api.update(file_public_id, asset_folder=folder, tags=','.join(tags))
        pdb.set_trace()
        if 'cat' in tags:
            return '入住卯貓窩了🏠'
        elif 'dog' in tags:
            return '入住狗勾窩了🏠'
        else:
            return '入住未知物種窩了🏠'
