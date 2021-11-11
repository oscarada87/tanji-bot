import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api
import random

load_dotenv()

class CloudImage():
  def __init__(self) -> None:
      cloudinary.config(
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),  
        api_key = os.getenv('CLOUDINARY_API_KEY'),  
        api_secret = os.getenv('CLOUDINARY_API_SECRET')  
      )

  def meow(self):
    result = cloudinary.Search().expression('folder=miru/*').execute()
    return random.choice(result['resources'])['secure_url']

  def wang(self):
    result = cloudinary.Search().expression('folder=doggy/*').execute()
    return random.choice(result['resources'])['secure_url']
